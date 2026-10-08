#!/usr/bin/env python3
"""
The end of each git-validate job (the draft/ flow): which recipes passed, which failed and
why, and the exit code.

A pull request may carry many drafts, and one bad draft must not hold back the others:
each job hands only what passed to the next one, and job 3 writes back only those. So a
job fails only when EVERY recipe it was given failed; a partial result is green, with one
`::warning::` per failure so it still shows on the run page. The same list goes to the
job summary ($GITHUB_STEP_SUMMARY) when the job runs in Actions.
"""
from __future__ import annotations

import os


def finish(job: str, passed: list[str], failed: list[tuple[str, str]]) -> int:
    """Print the PASSED / FAILED lists, write the job summary, and return the exit code:
    1 when something failed and nothing passed, else 0."""
    print(f"\n{job}: {len(passed)} passed, {len(failed)} failed")
    for name in passed:
        print(f"  PASSED  {name}")
    for name, why in failed:
        print(f"  FAILED  {name}  {why}")
    if failed and passed:
        for name, why in failed:
            print(f"::warning title={job} failed::{name}: {why}")
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if path:
        lines = [f"### {job}: {len(passed)} passed, {len(failed)} failed", ""]
        lines += [f"- ✅ `{name}`" for name in passed]
        lines += [f"- ❌ `{name}`: {why}" for name, why in failed]
        with open(path, "a", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n\n")
    return 1 if failed and not passed else 0
