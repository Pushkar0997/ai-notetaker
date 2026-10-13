"""Small dependency-free consistency check for the project specification."""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    "AGENTS.md", "CONTRACT.md", "BRIEF.md", "AGENT_LOG.md",
    "spec/product.md", "spec/architecture.md", "spec/plan.md",
    "spec/tasks.md", "spec/evals.md", "spec/smoke.md", "spec/decisions.md",
)


def main() -> int:
    errors = []
    contents = {}
    for relative in REQUIRED:
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"Missing required spec file: {relative}")
            continue
        contents[relative] = path.read_text(encoding="utf-8-sig")
        if re.search(r"\b(?:TODO|TBD|PLACEHOLDER)\b|<[^>]+>", contents[relative], re.I):
            errors.append(f"Unresolved placeholder found in {relative}")

    contract = contents.get("CONTRACT.md", "")
    evals = contents.get("spec/evals.md", "")
    for invariant in re.findall(r"^### (C-\d+)\b", contract, re.M):
        if invariant not in evals:
            errors.append(f"Contract invariant {invariant} has no evaluation entry")
    architecture = contents.get("spec/architecture.md", "")
    for phrase in ("## Capability register", "## Performance budget", "## Security/privacy"):
        if phrase not in architecture:
            errors.append(f"Architecture is missing section: {phrase}")
    if errors:
        print("Spec lint failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Spec lint passed: {len(REQUIRED)} required files; contract invariants map to evaluations.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
