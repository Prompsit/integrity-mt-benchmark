#!/usr/bin/env python3
"""D3 contrastive pack: verified minimal-pair corruptions over the dev split.

For every dev record and every scoreable failure class, emit a minimal pair
(reference resource vs one corruption) and verify the validator accepts the
reference and rejects the corruption (verify-or-skip). Output:
data/contrastive.dev.jsonl.
ASCII-only.
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import resources as R  # noqa: E402

PKG = Path(__file__).resolve().parent.parent
DEV = PKG / "data" / "dev.jsonl"
OUT = PKG / "data" / "contrastive.dev.jsonl"


def main():
    rows, by_class, skipped = [], Counter(), 0
    for line in open(DEV, encoding="utf-8"):
        r = json.loads(line)
        if not R.score_item(r, r["reference"])["pass"]:
            skipped += 1
            continue
        for cls in r["failure_opportunity_tags"]:
            c = R.corrupt(cls, r, r["reference"])
            if c is None or R.score_item(r, c)["pass"]:
                skipped += 1
                continue
            rows.append({"item_id": r["item_id"], "target_lang": r["target_lang"],
                         "reference": r["reference"], "hypothesis": c,
                         "format": r["format"], "failure_class": cls,
                         "severity": R.SEVERITY[cls],
                         "validator_rejects_corrupt": True})
            by_class[cls] += 1
        if r["format"] in ("json", "arb"):
            obj = json.loads(r["reference"])
            key = r["translatable_keys"][0]
            obj[key] = [obj[key]]
            bad = json.dumps(obj, ensure_ascii=False, indent=2)
            assert not R.score_item(r, bad)["schema_match"]
            rows.append({"item_id": r["item_id"], "target_lang": r["target_lang"],
                         "format": r["format"], "failure_class": "schema_changed",
                         "mutation": "string_to_array", "reference": r["reference"],
                         "hypothesis": bad, "severity": "Major",
                         "validator_rejects_corrupt": True})
            by_class["schema_changed"] += 1
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(json.dumps({"contrastive_pairs": len(rows), "by_class": dict(by_class),
                      "skipped": skipped}, indent=2))


if __name__ == "__main__":
    main()
