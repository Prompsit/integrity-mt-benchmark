#!/usr/bin/env python3
"""D5 contrastive pack: verified minimal-pair resource-adherence corruptions (dev).
ASCII-only."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import lingres as L  # noqa: E402

PKG = Path(__file__).resolve().parent.parent
DEV = PKG / "data" / "dev.jsonl"
OUT = PKG / "data" / "contrastive.dev.jsonl"


def main():
    rows, by_class, skipped = [], Counter(), 0
    for line in open(DEV, encoding="utf-8"):
        r = json.loads(line)
        if not L.score_item(r, r["reference"])["pass"]:
            skipped += 1
            continue
        for cls in r["failure_opportunity_tags"]:
            c = L.corrupt(cls, r)
            if c is None or L.score_item(r, c)["pass"]:
                skipped += 1
                continue
            rows.append({"item_id": r["item_id"], "target_lang": r["target_lang"],
                         "reference": r["reference"], "hypothesis": c,
                         "kind": r["kind"], "failure_class": cls,
                         "severity": L.SEVERITY[cls], "validator_rejects_corrupt": True})
            by_class[cls] += 1
        if r.get("repeated"):
            bad = r["reference"].rsplit(" [", 1)[0] + " " + L.make_slot(r["ref_term"], False)
            assert not L.score_item(r, bad)["term_count"]
            rows.append({"item_id": r["item_id"], "target_lang": r["target_lang"],
                         "kind": r["kind"], "failure_class": "required_term_missing",
                         "mutation": "drop_repeated_term", "reference": r["reference"],
                         "hypothesis": bad, "severity": "Major",
                         "validator_rejects_corrupt": True})
            by_class["required_term_missing"] += 1
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(json.dumps({"contrastive_pairs": len(rows), "by_class": dict(by_class),
                      "skipped": skipped}, indent=2))


if __name__ == "__main__":
    main()
