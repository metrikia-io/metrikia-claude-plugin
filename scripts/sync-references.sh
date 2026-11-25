#!/usr/bin/env bash
# =============================================================================
# sync-references.sh: copy the shared pages of references/ into every skill
#
# Usage:
#   ./scripts/sync-references.sh           write the copies
#   ./scripts/sync-references.sh --check   write nothing, exit 1 when a skill
#                                          does not stand on its own
#
# references/ is the only source. A chat on claude.ai loads the folder of a
# skill and nothing else, so each skill carries its own copy of these pages.
# =============================================================================
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

MODE="${1:-}"

if [[ -n "$MODE" && "$MODE" != "--check" ]]; then
    echo "Usage: $0 [--check]"
    exit 2
fi

pages_without_source() {
    local copy
    for copy in "$1"references/*; do
        if [[ ( -e "$copy" || -L "$copy" ) && ! -f "references/${copy##*/}" ]]; then
            echo "$copy"
        fi
    done
}

write_copies() {
    local skill page copy
    for skill in skills/*/; do
        mkdir -p "${skill}references"
        while IFS= read -r copy; do
            rm -- "$copy"
        done < <(pages_without_source "$skill")
        for page in references/*.md; do
            rm -f -- "${skill}${page}"
            cp -- "$page" "${skill}${page}"
        done
    done
}

check_copies() {
    local skill page copy
    for skill in skills/*/; do
        for page in references/*.md; do
            copy="${skill}${page}"
            if [[ -L "$copy" ]]; then
                echo "$copy is a link, not a file"
            elif [[ ! -f "$copy" ]]; then
                echo "$copy is missing"
            elif ! cmp -s "$page" "$copy"; then
                echo "$copy differs from $page"
            fi
        done
        while IFS= read -r copy; do
            echo "$copy has no source in references/"
        done < <(pages_without_source "$skill")
    done
}

check_texts() {
    local skill page line
    for skill in skills/*/; do
        for page in references/*.md; do
            grep -qF "\`$page\`" "${skill}SKILL.md" || echo "${skill}SKILL.md does not point to $page"
        done
    done
    while IFS= read -r line; do
        echo "a variable or a path out of the folder: $line"
    done < <(grep -rnE '\$\{|\.\./' references skills || true)
}

if [[ "$MODE" != "--check" ]]; then
    write_copies
    echo "The shared pages are copied into every skill."
    exit 0
fi

PROBLEMS="$(check_copies; check_texts)"

if [[ -n "$PROBLEMS" ]]; then
    echo "$PROBLEMS"
    echo "After a change in references/, run ./scripts/sync-references.sh."
    exit 1
fi

echo "Every skill stands on its own."
