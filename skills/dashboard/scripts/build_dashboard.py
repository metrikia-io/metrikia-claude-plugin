#!/usr/bin/env python3
"""Build the Metrikia dashboard page from a data file.

Usage:
    python3 build_dashboard.py data.json dashboard.html
    python3 build_dashboard.py --check data.json

The page is the template of the skill plus the data, nothing else. A figure with
no source, or that does not add up with the ones beside it, stops the build: go
back to the result of the tool, never adjust a figure to make it pass.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Callable, Iterator, Optional

Json = dict

TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "dashboard.html"
DATA_SLOT = "__METRIKIA_DATA__"

FORMATS = ("money", "number", "percent", "ratio")
BETTER = ("down", "none", "up")
LEVELS = ("broken", "ok", "watch")
TONES = ("bad", "good", "neutral", "watch")
KINDS = ("fix", "lower", "make", "pause", "raise", "start")
KINDS_THAT_ADD_SPEND = ("raise", "start")

NUMBER_IN_A_TEXT = re.compile(r"\d[\d\s\u00a0\u202f]*(?:[.,]\d+)?")
SIZE_WORDS = re.compile(r"\b(half|third|quarter|double|twice|triple|moitié|tiers|quart|fois)\b", re.IGNORECASE)

ROUNDING = 0.005
MONEY_SLACK = 0.5


@dataclass(frozen=True)
class Division:
    """A figure a tool gave, and the two it is the division of."""

    where: str
    result: Any
    top: Any
    bottom: Any
    how: str

    def is_readable(self) -> bool:
        return all(map(is_number, (self.result, self.top, self.bottom))) and self.bottom > 0

    def bounds(self) -> tuple[float, float]:
        low = (self.top - ROUNDING) / (self.bottom + ROUNDING)
        high = (self.top + ROUNDING) / max(self.bottom - ROUNDING, ROUNDING)
        return low - 2 * ROUNDING, high + 2 * ROUNDING

    def adds_up(self) -> bool:
        low, high = self.bounds()
        return low <= self.result <= high


@dataclass(frozen=True)
class DailyMoney:
    """What an action may add to the spend of a day, from the least to the most."""

    least: float
    most: float

    def as_json(self) -> Json:
        return {"min": self.least, "max": self.most}


NOTHING_MOVES = DailyMoney(0, 0)


@dataclass
class Report:
    problems: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    figures: int = 0
    cross_checks: int = 0

    def problem(self, where: str, what: str) -> None:
        self.problems.append(f"{where}: {what}")

    def require(self, where: str, holder: Json, *names: str) -> None:
        missing = [name for name in names if holder.get(name) in (None, "")]
        if missing:
            self.problem(where, f"{', '.join(missing)} missing")

    def one_of(self, where: str, value: Any, allowed: tuple[str, ...]) -> bool:
        if value in allowed:
            return True
        self.problem(where, f"{value!r} is not one of {', '.join(allowed)}")
        return False

    def divides(self, division: Division) -> None:
        if not division.is_readable():
            return
        self.cross_checks += 1
        if division.adds_up():
            return
        low, high = division.bounds()
        self.problem(
            division.where,
            f"{division.result} does not add up, {division.how} gives {low:.2f} to {high:.2f}",
        )


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def listed(data: Json, name: str) -> Iterator[tuple[str, Json]]:
    for index, item in enumerate(data.get(name) or []):
        title = item.get("name") or item.get("label") or item.get("object") or item.get("title") or ""
        yield f"{name}[{index}] {title}".strip(), item


def check_source(report: Report, data: Json, where: str, holder: Json) -> None:
    if holder.get("source") not in (data.get("sources") or {}):
        report.problem(where, "its source is missing, or is not listed in sources")
        return
    report.figures += 1


def check_head(report: Report, data: Json) -> None:
    report.require("page", data, "account", "currency", "readOn")
    report.require("period", data.get("period") or {}, "start", "end")
    report.require("headline", data.get("headline") or {}, "sentence")
    for name in ("period", "comparedWith"):
        check_days(report, name, data.get(name) or {})
    for name, source in (data.get("sources") or {}).items():
        report.require(f"sources.{name}", source, "tool", "reads")


def check_days(report: Report, where: str, period: Json) -> None:
    days = [period[name] for name in ("start", "end") if period.get(name)]
    if not all(re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(day)) for day in days):
        report.problem(where, "start and end are days, as YYYY-MM-DD")
        return
    if days != sorted(days):
        report.problem(where, "it ends before it starts")


def check_kpis(report: Report, data: Json) -> None:
    for where, kpi in listed(data, "kpis"):
        check_source(report, data, where, kpi)
        report.require(where, kpi, "label", "field")
        report.one_of(f"{where} format", kpi.get("format"), FORMATS)
        report.one_of(f"{where} better", kpi.get("better", "none"), BETTER)
    for side in ("value", "previous"):
        check_kpi_divisions(report, side, by_key(data, side))


def by_key(data: Json, side: str) -> Json:
    return {kpi["key"]: kpi.get(side) for _, kpi in listed(data, "kpis") if kpi.get("key")}


def check_kpi_divisions(report: Report, side: str, known: Json) -> None:
    divisions = (
        ("mer", "sales", "spend"),
        ("onlineMer", "onlineSales", "spend"),
        ("costPerSale", "spend", "salesCount"),
        ("onlineCostPerSale", "spend", "onlineCount"),
    )
    for result, top, bottom in divisions:
        report.divides(
            Division(f"kpis {result} ({side})", known.get(result), known.get(top), known.get(bottom), f"{top} / {bottom}")
        )


def check_campaigns(report: Report, data: Json) -> None:
    check_rows(report, data, "campaigns")
    total = by_key(data, "value").get("spend")
    spends = [row["spend"] for _, row in listed(data, "campaigns") if is_number(row.get("spend"))]
    if not is_number(total) or not spends:
        return
    report.cross_checks += 1
    if sum(spends) > total + ROUNDING * (len(spends) + 1):
        report.problem("campaigns", f"their spend adds up to {sum(spends):.2f}, more than the {total:.2f} of the account")


def check_creatives(report: Report, data: Json) -> None:
    check_rows(report, data, "creatives")


def check_rows(report: Report, data: Json, name: str) -> None:
    for where, row in listed(data, name):
        check_source(report, data, where, row)
        report.require(where, row, "name")
        report.one_of(f"{where} tone", row.get("tone", "neutral"), TONES)
        if row.get("verdict") and not row.get("verdictBy"):
            report.problem(where, "a verdict names the agent who gave it, in verdictBy")
        report.divides(Division(f"{where} roas", row.get("roas"), row.get("revenue"), row.get("spend"), "revenue / spend"))
        report.divides(Division(f"{where} costPerSale", row.get("costPerSale"), row.get("spend"), row.get("sales"), "spend / sales"))


def check_platforms(report: Report, data: Json) -> None:
    for where, row in listed(data, "platforms"):
        check_source(report, data, where, row)
        if not all(is_number(row.get(name)) for name in ("claimed", "credited")):
            report.problem(where, "claimed and credited are numbers, or the row is left out")


def check_trend(report: Report, data: Json) -> None:
    for where, series in listed(data, "trend"):
        check_source(report, data, where, series)
        points = series.get("points") or []
        if len(points) < 3:
            report.problem(where, "a trend needs three points, or it is left out")
        if not all(point.get("label") and is_number(point.get("value")) for point in points):
            report.problem(where, "each point has a label and a value")


def check_sentences(report: Report, data: Json) -> None:
    """A sentence of the page is written by hand: its figures are the ones of the page, or the words of an agent."""
    known = figures_of(data)
    for name in ("headline", "creativeHeadline"):
        headline = data.get(name) or {}
        if headline.get("wordsOf") in (data.get("sources") or {}):
            continue
        for part in ("sentence", "lead"):
            check_sentence(report, f"{name}.{part}", headline.get(part) or "", known)


def check_sentence(report: Report, where: str, sentence: str, known: list[float]) -> None:
    for word in SIZE_WORDS.findall(sentence):
        report.problem(where, f"{word!r} is a size nobody read: write the figure")
    for number in map(number_of, NUMBER_IN_A_TEXT.findall(sentence)):
        report.cross_checks += 1
        if not any(rounds_to(number, figure) for figure in known):
            report.problem(where, f"{number:g} is not a figure of the page, use one, or name the agent in wordsOf")


def number_of(written: str) -> float:
    return float(re.sub(r"[\s\u00a0\u202f]", "", written).replace(",", "."))


def rounds_to(number: float, figure: float) -> bool:
    return any(abs(round(abs(figure), digits) - number) < 1e-9 for digits in (0, 1, 2))


def figures_of(data: Json) -> list[float]:
    """Every figure of the page, the change of each one, and the numbers of its dates."""
    changes = [
        (kpi["value"] - kpi["previous"]) / abs(kpi["previous"]) * 100
        for _, kpi in listed(data, "kpis")
        if is_number(kpi.get("value")) and is_number(kpi.get("previous")) and kpi["previous"]
    ]
    dates = " ".join(str(value) for name in ("period", "comparedWith") for value in (data.get(name) or {}).values())
    return list(numbers_in(data)) + changes + [float(part) for part in re.findall(r"\d+", dates)] + [float(len(data.get("actions") or []))]


def numbers_in(value: Any) -> Iterator[float]:
    if is_number(value):
        yield float(value)
    parts = value.values() if isinstance(value, dict) else value if isinstance(value, list) else ()
    for part in parts:
        yield from numbers_in(part)


def check_reliability(report: Report, data: Json) -> None:
    for where, item in listed(data, "reliability"):
        check_source(report, data, where, item)
        report.require(where, item, "text")
        report.one_of(f"{where} level", item.get("level"), LEVELS)


def check_briefs(report: Report, data: Json) -> None:
    for where, brief in listed(data, "briefs"):
        check_source(report, data, where, brief)
        report.require(where, brief, "title", "hook", "copy", "judgedOn")


def check_actions(report: Report, data: Json) -> None:
    for where, action in listed(data, "actions"):
        check_source(report, data, where, action)
        report.require(where, action, "object", "what", "why", "by")
        if not report.one_of(f"{where} kind", action.get("kind"), KINDS):
            continue
        if action["kind"] in KINDS_THAT_ADD_SPEND:
            report.require(where, action, "stopWhen")
        money = daily_money(report, where, action)
        action["dailyChange"] = money.as_json() if money else None


def daily_money(report: Report, where: str, action: Json) -> Optional[DailyMoney]:
    """Worked out from the budgets of the action, never a figure typed by hand."""
    rules: dict[str, Callable[[Report, str, Json], Optional[DailyMoney]]] = {
        "raise": money_of_a_new_budget,
        "lower": money_of_a_new_budget,
        "pause": money_of_a_pause,
        "start": money_of_a_start,
    }
    rule = rules.get(action["kind"])
    return rule(report, where, action) if rule else NOTHING_MOVES


def money_of_a_new_budget(report: Report, where: str, action: Json) -> Optional[DailyMoney]:
    before, after = action.get("fromDaily"), action.get("toDaily")
    if not (is_number(before) and is_number(after)):
        report.problem(where, "fromDaily and toDaily are needed")
        return None
    if (action["kind"] == "raise") != (after > before):
        report.problem(where, f"{action['kind']} goes from {before} to {after}")
    return DailyMoney(round(after - before, 2), round(after - before, 2))


def money_of_a_pause(report: Report, where: str, action: Json) -> Optional[DailyMoney]:
    if action.get("insideBudget") is True:
        return NOTHING_MOVES
    if not is_number(action.get("fromDaily")):
        report.problem(where, "fromDaily is needed, or insideBudget when it spends the budget of its campaign")
        return None
    return DailyMoney(-action["fromDaily"], -action["fromDaily"])


def money_of_a_start(report: Report, where: str, action: Json) -> Optional[DailyMoney]:
    if is_number(action.get("unlocksDaily")):
        return DailyMoney(0, action["unlocksDaily"])
    if not action.get("moneyUnknown"):
        report.problem(where, "what it starts can spend: give unlocksDaily, the budget it unlocks, or moneyUnknown and the reason")
    return None


def check_plan_total(report: Report, data: Json) -> None:
    announced = (data.get("planTotal") or {}).get("daily")
    actions = data.get("actions") or []
    if not is_number(announced) or not actions:
        return
    report.cross_checks += 1
    changes = [action.get("dailyChange") for action in actions]
    least = sum(change["min"] for change in changes if change)
    most = sum(change["max"] for change in changes if change)
    agrees = None not in changes and abs(announced - least) <= MONEY_SLACK and abs(announced - most) <= MONEY_SLACK
    if agrees:
        return
    data["planMismatch"] = {"announced": announced, "by": data["planTotal"].get("by", ""), "min": least, "max": most}
    report.warnings.append(
        f"the plan announced is {announced:+g} a day, its lines move from {least:+g} to {most:+g}: "
        "the page shows both, ask the agent before anything is applied"
    )


CHECKS = (
    check_head,
    check_sentences,
    check_kpis,
    check_campaigns,
    check_creatives,
    check_platforms,
    check_trend,
    check_reliability,
    check_briefs,
    check_actions,
    check_plan_total,
)


def check(data: Json) -> Report:
    report = Report()
    for run in CHECKS:
        run(report, data)
    return report


def page(data: Json, report: Report) -> str:
    shown = {
        **data,
        "spendPerDay": spend_per_day(data),
        "checks": {"figures": report.figures, "crossChecks": report.cross_checks},
    }
    payload = json.dumps(shown, ensure_ascii=False)
    for character in "&<>":
        payload = payload.replace(character, f"\\u{ord(character):04x}")
    template = TEMPLATE.read_text(encoding="utf-8")
    if template.count(DATA_SLOT) != 1:
        sys.exit("The template does not hold its data slot once.")
    return template.replace(DATA_SLOT, payload)


def spend_per_day(data: Json) -> Optional[float]:
    spend = by_key(data, "value").get("spend")
    if not is_number(spend):
        return None
    start, end = (date.fromisoformat(data["period"][name]) for name in ("start", "end"))
    return round(spend / ((end - start).days + 1), 2)


def read(path: str) -> Json:
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        sys.exit(f"The data file cannot be read: {error}")


def main(arguments: list[str]) -> int:
    only_check = arguments[:1] == ["--check"]
    paths = arguments[1:] if only_check else arguments
    if len(paths) != (1 if only_check else 2):
        print(__doc__)
        return 2
    data = read(paths[0])
    report = check(data)
    for warning in report.warnings:
        print(f"WARNING {warning}")
    if report.problems:
        print("\n".join(report.problems))
        print("Read the result of the tool again. Never adjust a figure to make it pass.")
        return 1
    if not only_check:
        Path(paths[1]).write_text(page(data, report), encoding="utf-8")
    print(f"{report.figures} figures with a source, {report.cross_checks} cross-checks right.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
