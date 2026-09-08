#!/usr/bin/env python3
"""D4 document oracle + validators (deterministic, parser-based).

Scoring rule at the DOCUMENT level: the element hierarchy is
preserved and the output is XML-well-formed; only the text is translated. The structure (block
sequence, table shape, links/images, segment map) is language-independent, so the
validator compares a hypothesis document's structural signature against the SOURCE
signature - reference-light. Text/translation quality is out of D4's scope.

Profile: rich HTML (headings, paragraphs, lists, a table, a link, an image).

Text comes from D1 catalog-derived pairs and generated additions (license inherited).
Complete documents are constructed using templates. ASCII-only.
"""
from __future__ import annotations

SCORER_VERSION = "1.1"

import re
from collections import Counter
import xml.etree.ElementTree as ET

LANGS = ["ca", "es", "fr", "it", "pt-PT", "de", "nl", "pl", "ru"]
SOURCE_LANG = "en"
VOID = {"img", "br", "hr"}
STRUCTURAL = {"h1", "h2", "p", "ul", "ol", "li", "table", "tr", "td", "th", "a", "img"}

ALL_CLASSES = ["lost_or_duplicated_node", "block_order_change",
               "table_cell_corruption", "broken_link_image", "roundtrip_failure"]
SEVERITY = {"lost_or_duplicated_node": "Major", "block_order_change": "Major",
            "table_cell_corruption": "Major", "broken_link_image": "Major",
            "roundtrip_failure": "Critical"}

LINK_HREF = "https://example.org/docs/guide"
IMG_SRC = "images/diagram.png"


def build_html(segs: list[str], href: str = LINK_HREF, src: str = IMG_SRC,
               variant: int = 0) -> str:
    """13 text segments -> a structurally rich HTML document.

    ``variant`` reorders the body blocks (the <h2>+<p> pair stays adjacent so the
    block-order corruption operator still has a target) to give the population a
    diversity of structural signatures instead of a single template; every variant
    keeps all five corruptible anchors (a <p>, a <li>, an <h2>+<p> pair, a 2x2
    <table>, a link and an image)."""
    s = [_esc(x) for x in segs]
    h1 = "<h1>%s</h1>" % s[0]
    p1 = "<p>%s</p>" % s[1]
    h2p = "<h2>%s</h2>\n<p>%s</p>" % (s[2], s[3])
    ul = "<ul>\n<li>%s</li>\n<li>%s</li>\n<li>%s</li>\n</ul>" % (s[4], s[5], s[6])
    table = ("<table>\n<tr><td>%s</td><td>%s</td></tr>\n"
             "<tr><td>%s</td><td>%s</td></tr>\n</table>") % (s[7], s[8], s[9], s[10])
    linkp = '<p><a href="%s">%s</a></p>' % (href, s[11])
    img = '<img src="%s" alt="%s"/>' % (src, s[12])
    orders = [
        [p1, h2p, ul, table, linkp, img],
        [h2p, p1, ul, table, linkp, img],
        [p1, h2p, table, ul, linkp, img],
        [p1, h2p, ul, linkp, table, img],
    ]
    body = "\n".join(orders[variant % len(orders)])
    return "<html><body>\n%s\n%s\n</body></html>\n" % (h1, body)


def _esc(t: str) -> str:
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;").replace("'", "&#39;"))


def _xml_ok(html: str) -> bool:
    """Strict well-formedness: the document must parse as XML (catches broken
    attributes / unclosed tags that the lenient html.parser would swallow)."""
    try:
        ET.fromstring(html)
        return True
    except Exception:
        return False


# --- structural signature -----------------------------------------------------

def signature(html: str) -> dict:
    """Signature for the benchmark's XML-well-formed HTML profile.

    Element paths preserve parentage and sibling order. Text positions exclude
    whitespace-only formatting. Translatable text and alt/title values are not
    compared. This is not a browser or document-extraction round trip.
    """
    try:
        root = ET.fromstring(html)
    except (ET.ParseError, ValueError):
        return {"ok": False}
    tree, seq, tags, targets, segments, tables = [], [], [], [], [], []

    def walk(node, path):
        tag = node.tag.lower()
        tree.append([list(path), tag])
        if tag in STRUCTURAL:
            tags.append(tag)
            if tag not in ("tr", "td", "th"):
                seq.append(tag)
        attrs = {k.lower(): v for k, v in node.attrib.items()}
        if tag in ("a", "img"):
            key = "href" if tag == "a" else "src"
            targets.append([list(path), key, attrs.get(key)])
        if tag == "table":
            rows = []
            def collect_rows(parent):
                for child in parent:
                    if child.tag.lower() == "table":
                        continue
                    if child.tag.lower() == "tr":
                        rows.append([[c.tag.lower(), c.get("rowspan", "1"),
                                      c.get("colspan", "1")]
                                     for c in child if c.tag.lower() in ("td", "th")])
                    else:
                        collect_rows(child)
            collect_rows(node)
            tables.append([list(path), rows])
        if (node.text or "").strip():
            segments.append([list(path), "text"])
        for i, child in enumerate(node):
            walk(child, path + (i,))
            if (child.tail or "").strip():
                segments.append([list(path + (i,)), "tail"])

    walk(root, ())
    return {"ok": True, "balanced": True, "signature_version": 2,
            "tree": tree, "multiset": dict(Counter(tags)), "sequence": seq,
            "tables": tables, "targets": targets, "segments": len(segments),
            "segment_positions": segments}


# --- hard-gate scorer (compare hypothesis to SOURCE structure) ---------------

def score_item(record: dict, hypothesis: str) -> dict:
    # Old records remain usable when they carry the source document.
    src = signature(record["source"]) if "source" in record else record["source_signature"]
    if src.get("signature_version") != 2:
        raise ValueError("D4 v1.1 requires source HTML or a version-2 source signature")
    hyp = signature(hypothesis)
    gates = {"roundtrip_valid": bool(hyp.get("ok") and hyp.get("balanced")
                                     and _xml_ok(hypothesis))}
    if not gates["roundtrip_valid"]:
        gates.update({"tree_match": False, "block_order": False,
                      "table_cells": False, "links_images": False, "segment_map": False, "pass": False,
                      "failure_class": "roundtrip_failure", "severity": "Critical"})
        return gates
    gates["tree_match"] = hyp["tree"] == src["tree"]
    gates["block_order"] = list(hyp["sequence"]) == list(src["sequence"])
    gates["table_cells"] = hyp["tables"] == src["tables"]
    gates["links_images"] = hyp["targets"] == src["targets"]
    gates["segment_map"] = hyp["segment_positions"] == src["segment_positions"]
    gates["pass"] = all(v for k, v in gates.items() if k != "pass")
    cls = None
    if not gates["table_cells"]:
        cls = "table_cell_corruption"
    elif not gates["block_order"] and hyp["multiset"] == src["multiset"]:
        cls = "block_order_change"
    elif not gates["tree_match"] or not gates["segment_map"]:
        cls = "lost_or_duplicated_node"
    elif not gates["links_images"]:
        cls = "broken_link_image"
    gates["failure_class"] = cls
    gates["severity"] = SEVERITY.get(cls) if cls else None
    return gates


# --- corruption operators -----------------------------------------------------

def corrupt(cls: str, ref_html: str):
    if cls == "roundtrip_failure":
        return ref_html.replace("</p>", "", 1)  # unclosed <p>
    if cls == "lost_or_duplicated_node":
        return re.sub(r"<li>.*?</li>\n", "", ref_html, count=1)  # drop a list item
    if cls == "block_order_change":
        # swap the <h2>..</h2> block with the following <p>..</p>
        m = re.search(r"(<h2>.*?</h2>)\n(<p>.*?</p>)", ref_html, re.S)
        if not m:
            return None
        return ref_html.replace(m.group(0), m.group(2) + "\n" + m.group(1), 1)
    if cls == "table_cell_corruption":
        # count-preserving shape change: 2x2 -> rows of 3 and 1 (cells moved, not lost)
        return re.sub(
            r"<tr><td>(.*?)</td><td>(.*?)</td></tr>\n<tr><td>(.*?)</td><td>(.*?)</td></tr>",
            r"<tr><td>\1</td><td>\2</td><td>\3</td></tr>\n<tr><td>\4</td></tr>",
            ref_html, count=1, flags=re.S)
    if cls == "broken_link_image":
        return ref_html.replace('href="%s"' % LINK_HREF,
                                'href="%s-broken"' % LINK_HREF, 1)
    return None


def scoreable_classes(record: dict, ref_html: str) -> list[str]:
    out = []
    for cls in ALL_CLASSES:
        c = corrupt(cls, ref_html)
        if c is not None and not score_item(record, c)["pass"]:
            out.append(cls)
    return out


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    segs = ["Title", "Intro paragraph", "Section", "Body text",
            "First item", "Second item", "Third item",
            "Cell A", "Cell B", "Cell C", "Cell D", "See the guide", "Diagram alt"]
    en = build_html(segs)
    rec = {"source_signature": signature(en)}
    print("ref pass:", score_item(rec, en)["pass"])
    print("scoreable:", scoreable_classes(rec, en))
    for c in ALL_CLASSES:
        bad = corrupt(c, en)
        r = score_item(rec, bad) if bad else {"pass": None}
        print(c, "->", "rejected" if bad and not r["pass"] else "MISS", "| class:", r.get("failure_class"))
