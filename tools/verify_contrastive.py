#!/usr/bin/env python3
"""Re-score both sides of every dev contrastive pair with current validators."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
MODULES = {"d1": "validators", "d2": "validators", "d3": "resources",
           "d4": "documents", "d5": "lingres"}


def verify_package(pkg: Path) -> list[str]:
    did = pkg.name.split("-", 1)[0]
    module = MODULES[did]
    sys.path.insert(0, str(pkg / "build"))
    try:
        spec = importlib.util.spec_from_file_location(did + "_contrastive_scorer", pkg / "build" / (module + ".py"))
        scorer = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(scorer)
    finally:
        sys.path.remove(str(pkg / "build"))
    records = [json.loads(line) for line in (pkg / "data/dev.jsonl").read_text(encoding="utf-8").splitlines()]
    by_key = {(r["item_id"], r["target_lang"]): r for r in records}
    errors = []
    manifest = json.loads((pkg / "manifest.json").read_text(encoding="utf-8"))
    if scorer.SCORER_VERSION != manifest.get("scorer_version"):
        errors.append(f"{pkg.name}: manifest/scorer version mismatch")
    for line in (pkg / "data/contrastive.dev.jsonl").read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        key = row["item_id"], row["target_lang"]
        rec = by_key.get(key)
        if rec is None:
            errors.append(f"{pkg.name}: contrastive pair is not from dev: {key}")
            continue
        if row.get("reference") != rec["reference"] or not isinstance(row.get("hypothesis"), str):
            errors.append(f"{pkg.name}: missing or mismatched pair text: {key}")
            continue
        context = rec["source"] if did == "d1" else rec
        good = scorer.score_item(context, row["reference"])
        bad = scorer.score_item(context, row["hypothesis"])
        if not good["pass"] or bad["pass"]:
            errors.append(f"{pkg.name}: pair not separated by current scorer: {key}")
        if row.get("expected_gate") and bad.get(row["expected_gate"], True):
            errors.append(f"{pkg.name}: expected gate did not fail: {key}")
    return errors


def main():
    errors = []
    for pkg in sorted((ROOT / "datasets").glob("d[1-5]-*")):
        errors.extend(verify_package(pkg))
    if errors:
        print("\n".join(errors[:20]))
        return 1
    print("CONTRASTIVE: PASS (all pairs rescored)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
