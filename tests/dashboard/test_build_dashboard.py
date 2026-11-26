"""The build of the dashboard refuses what nobody read.

Run: python3 -m unittest discover -s tests/dashboard
The account below does not exist.
"""

import copy
import importlib.util
import json
import re
import sys
import unittest
from pathlib import Path
from types import ModuleType
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "skills" / "dashboard" / "scripts" / "build_dashboard.py"


def load_the_build() -> ModuleType:
    spec = importlib.util.spec_from_file_location("build_dashboard", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


build = load_the_build()

ACCOUNT = {
    "lang": "en",
    "account": "Example",
    "currency": "EUR",
    "readOn": "2026-01-15",
    "period": {"start": "2026-01-08", "end": "2026-01-14"},
    "sources": {"m": {"tool": "get_metrics", "reads": "8 to 14 January"}},
    "headline": {"sentence": "Online sales reached 1000 for 250 of spend."},
    "kpis": [
        {"key": "onlineSales", "label": "Online sales", "value": 1000.0, "previous": 800.0, "format": "money", "source": "m", "field": "a"},
        {"key": "spend", "label": "Spend", "value": 250.0, "format": "money", "source": "m", "field": "b"},
        {"key": "onlineMer", "label": "Online MER", "value": 4.0, "format": "ratio", "source": "m", "field": "c", "hero": True},
    ],
    "campaigns": [
        {"name": "One", "spend": 200.0, "sales": 4, "revenue": 500.0, "roas": 2.5, "costPerSale": 50.0, "source": "m"},
    ],
}


def account(**changes: Any) -> dict:
    return {**copy.deepcopy(ACCOUNT), **copy.deepcopy(changes)}


def action(**changes: Any) -> dict:
    line = {"kind": "raise", "object": "One", "what": "20 to 25", "why": "it sells", "by": "media buyer", "stopWhen": "two days", "fromDaily": 20, "toDaily": 25, "source": "m"}
    return {**line, **changes}


def problems(data: dict) -> list:
    return build.check(data).problems


class FiguresTest(unittest.TestCase):
    def test_a_page_whose_figures_add_up_is_built(self) -> None:
        self.assertEqual([], problems(account()))

    def test_a_figure_with_no_source_is_refused(self) -> None:
        data = account()
        del data["kpis"][0]["source"]
        self.assertIn("source is missing", problems(data)[0])

    def test_a_source_that_is_not_listed_is_refused(self) -> None:
        data = account()
        data["kpis"][0]["source"] = "x"
        self.assertIn("not listed", problems(data)[0])

    def test_an_amount_left_in_cents_is_refused(self) -> None:
        data = account()
        data["campaigns"][0]["spend"] = 20000
        self.assertTrue(any("roas" in problem for problem in problems(data)))

    def test_a_figure_copied_from_another_line_is_refused(self) -> None:
        data = account()
        data["kpis"][2]["value"] = 5.2
        self.assertTrue(any("onlineMer" in problem for problem in problems(data)))

    def test_campaigns_that_spend_more_than_the_account_are_refused(self) -> None:
        data = account()
        data["campaigns"].append({"name": "Two", "spend": 90.0, "source": "m"})
        self.assertTrue(any("adds up" in problem for problem in problems(data)))

    def test_a_division_rounded_by_the_tool_is_accepted(self) -> None:
        data = account(campaigns=[{"name": "One", "spend": 3197.7, "sales": 9.34, "revenue": 3155.22, "roas": 0.99, "costPerSale": 342.2, "source": "m"}])
        data["kpis"][1]["value"], data["kpis"][2]["value"] = 4000.0, 0.25
        data["headline"]["sentence"] = "Spend 4000"
        self.assertEqual([], problems(data))

    def test_a_verdict_nobody_gave_is_refused(self) -> None:
        data = account()
        data["campaigns"][0]["verdict"] = "Sells"
        self.assertTrue(any("verdictBy" in problem for problem in problems(data)))

    def test_a_period_that_is_not_made_of_days_is_refused(self) -> None:
        self.assertEqual(["period: start and end are days, as YYYY-MM-DD"], problems(account(period={"start": "1 January", "end": "2 January"})))

    def test_a_period_that_ends_before_it_starts_is_refused(self) -> None:
        self.assertEqual(["period: it ends before it starts"], problems(account(period={"start": "2026-01-14", "end": "2026-01-08"})))


class SentencesTest(unittest.TestCase):
    def test_a_number_that_is_not_on_the_page_is_refused(self) -> None:
        self.assertIn("1200", problems(account(headline={"sentence": "Sales reached 1200."}))[0])

    def test_the_change_of_a_figure_is_a_figure_of_the_page(self) -> None:
        self.assertEqual([], problems(account(headline={"sentence": "Sales rose by 25 %."})))

    def test_a_size_in_words_is_refused(self) -> None:
        self.assertIn("half", problems(account(headline={"sentence": "One ad takes half of the spend."}))[0])
        self.assertIn("moitié", problems(account(headline={"sentence": "Une pub prend la moitié."}))[0])

    def test_the_words_of_an_agent_stay_as_written(self) -> None:
        self.assertEqual([], problems(account(headline={"sentence": "From 643 to 386 a day.", "wordsOf": "m"})))


class MoneyTest(unittest.TestCase):
    def changes(self, **line: Any) -> tuple:
        data = account(actions=[action(**line)])
        return problems(data), data["actions"][0]["dailyChange"]

    def test_a_raise_moves_the_difference_of_its_budgets(self) -> None:
        self.assertEqual(([], {"min": 5, "max": 5}), self.changes())

    def test_a_raise_that_lowers_is_refused(self) -> None:
        self.assertTrue(self.changes(toDaily=10)[0])

    def test_a_start_can_spend_the_budget_it_unlocks(self) -> None:
        self.assertEqual(([], {"min": 0, "max": 625}), self.changes(kind="start", unlocksDaily=625))

    def test_a_start_whose_money_nobody_gave_is_refused(self) -> None:
        self.assertIn("unlocksDaily", self.changes(kind="start")[0][0])

    def test_a_start_may_say_its_money_is_not_known(self) -> None:
        self.assertEqual(([], None), self.changes(kind="start", moneyUnknown="no budget in the reading"))

    def test_a_pause_inside_a_budget_frees_nothing(self) -> None:
        self.assertEqual(([], {"min": 0, "max": 0}), self.changes(kind="pause", insideBudget=True))

    def test_a_pause_frees_its_own_budget(self) -> None:
        self.assertEqual(([], {"min": -20, "max": -20}), self.changes(kind="pause"))

    def test_an_action_that_adds_spend_says_when_to_stop(self) -> None:
        self.assertIn("stopWhen", self.changes(stopWhen="")[0][0])

    def test_a_total_that_is_not_the_one_of_the_lines_is_shown_beside_it(self) -> None:
        lines = [action(), action(kind="start", object="Sale", unlocksDaily=625)]
        data = account(actions=lines, planTotal={"daily": 5, "by": "The media buyer"})
        report = build.check(data)
        self.assertEqual([], report.problems)
        self.assertIn("ask the agent", report.warnings[0])
        self.assertEqual({"announced": 5, "by": "The media buyer", "min": 5, "max": 630}, data["planMismatch"])

    def test_a_total_that_is_the_one_of_the_lines_says_nothing(self) -> None:
        data = account(actions=[action()], planTotal={"daily": 5})
        self.assertEqual([], build.check(data).warnings)
        self.assertNotIn("planMismatch", data)


class PageTest(unittest.TestCase):
    def payload(self, html: str) -> dict:
        return json.loads(re.search(r'id="data">(.*?)</script>', html, re.DOTALL).group(1))

    def test_a_name_cannot_close_the_block_of_the_data(self) -> None:
        name = "</script><img src=x onerror=alert(1)>&"
        html = build.page(account(account=name), build.Report())
        self.assertNotIn("<img", html)
        self.assertEqual(name, self.payload(html)["account"])

    def test_the_spend_of_a_day_is_worked_out(self) -> None:
        self.assertEqual(35.71, self.payload(build.page(account(), build.Report()))["spendPerDay"])

    def test_the_page_never_reads_a_text_as_html_nor_loads_anything(self) -> None:
        template = build.TEMPLATE.read_text(encoding="utf-8")
        for forbidden in ("innerHTML", "outerHTML", "insertAdjacentHTML", "document.write", "eval(", "fetch(", "http://", "url("):
            found = template.replace("http://www.w3.org/2000/svg", "")
            self.assertNotIn(forbidden, found)
        self.assertIn("default-src 'none'", template)


if __name__ == "__main__":
    unittest.main()
