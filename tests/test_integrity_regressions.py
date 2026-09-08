"""Scoring regressions using synthetic examples; no dataset download required."""
import importlib.util
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(dimension, module):
    folder = next((ROOT / "datasets").glob(dimension + "-*")) / "build"
    sys.path.insert(0, str(folder))
    spec = importlib.util.spec_from_file_location(dimension + "_" + module, folder / (module + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


D1 = load("d1", "validators")
D2 = load("d2", "validators")
D3 = load("d3", "resources")
D4 = load("d4", "documents")
D5 = load("d5", "lingres")


class IntegrityRegressions(unittest.TestCase):
    def test_icu_select_keys_are_not_plural_categories(self):
        source = "{gender, select, male {He} female {She} other {They}}"
        self.assertTrue(D1.score_item(source, "{gender, select, female {Ella} male {El} other {Ellos}}")["pass"])
        for bad in ("{gender, select, other {Ellos}}", "{gender, select, male {El} other {Ellos}}"):
            self.assertFalse(D1.score_item(source, bad)["pass"])

    def test_icu_plural_adaptation_and_invalid_syntax(self):
        source = "{n, plural, one {One file} other {Files}}"
        self.assertTrue(D1.score_item(source, "{n, plural, one {Plik} few {Pliki} many {Plikow} other {Pliki}}")["pass"])
        for bad in ("{n, plural, one {Plik}}", "{n, plural, other {A} other {B}}",
                    "{n, plural, junk other {B}}", "{n, plural, offset:1 other {B}}"):
            self.assertFalse(D1.score_item(source, bad)["pass"])

    def test_icu_checks_every_message(self):
        source = "{n, plural, other {Files}} {x, select, yes {Yes} other {No}}"
        bad = "{n, plural, other {Fichiers}} {x, select, yes {Oui}}"
        self.assertFalse(D1.score_item(source, bad)["icu_syntax"])

    def test_icu_nested_keys_and_duplicate_blocks(self):
        block = "{x, select, yes {Yes} other {No}}"
        self.assertFalse(D1.score_item(block + " " + block, block)["pass"])
        source = "{n, plural, other {" + block + "}}"
        self.assertFalse(D1.score_item(source, "{n, plural, other {{x, select, other {No}}}}")["pass"])

    def test_d2_unknown_failure_has_a_diagnostic(self):
        entity = {"kind": "number", "semantic": {"value": 42}}
        result = D2.score_entity(entity, "es", "nonsense")
        self.assertFalse(result["pass"])
        self.assertEqual(result["failure_class"], "locale_form_mismatch")

    def resource(self, fmt):
        rec = {"format": fmt, "target_lang": "es", "src_keyvals": {"hello": "Hello", "code": "USB"},
               "translatable_keys": ["hello"], "nontrans_keys": ["code"]}
        rec["reference"] = D3.serialize(fmt, [("hello", "Hola"), ("code", "USB")], "es", ["code"])
        return rec

    def test_resource_types(self):
        for fmt in ("json", "arb"):
            rec = self.resource(fmt)
            self.assertTrue(D3.score_item(rec, rec["reference"])["pass"])
            for value in (["Hola"], {"nested": "Hola"}, 42, True, None):
                obj = json.loads(rec["reference"])
                obj["hello"] = value
                with self.subTest(fmt=fmt, value=value):
                    self.assertFalse(D3.score_item(rec, json.dumps(obj))["schema_match"])

    def test_duplicate_resource_keys(self):
        for fmt in D3.FORMATS:
            rec = self.resource(fmt)
            bad = {"json": '{"hello":"Bad","hello":"Hola","code":"USB"}',
                   "arb": '{"@@locale":"es","hello":"Bad","hello":"Hola","code":"USB"}',
                   "properties": "hello=Bad\nhello=Hola\ncode=USB\n",
                   "xml": '<resources><string name="hello">Bad</string><string name="hello">Hola</string><string name="code" translatable="false">USB</string></resources>'}[fmt]
            self.assertFalse(D3.score_item(rec, bad)["pass"])

    def test_xml_schema_and_dnt_marker(self):
        rec = self.resource("xml")
        for bad in (rec["reference"].replace(' translatable="false"', ''),
                    rec["reference"].replace('Hola', '<b>Hola</b>'),
                    rec["reference"].replace('</resources>', '<extra/></resources>')):
            self.assertFalse(D3.score_item(rec, bad)["pass"])
        self.assertTrue(D3.score_item(rec, rec["reference"].replace('  <', '\t<'))["pass"])
        self.assertTrue(D3.score_item(rec, rec["reference"].replace('name="hello"', 'name="hello" translatable="true"'))["pass"])

    def test_d4_parentage(self):
        src = '<html><body><ul><li>A</li><li>B</li></ul></body></html>'
        bad = '<html><body><ul><li>A<li>B</li></li></ul></body></html>'
        self.assertFalse(D4.score_item({"source": src}, bad)["tree_match"])
        self.assertTrue(D4.score_item({"source": src}, src.replace('A', 'Uno').replace('B', 'Dos'))["pass"])

    def test_d4_all_table_rows_and_spans(self):
        src = '<table><tr><td>A</td><td>B</td></tr><tr><td>C</td><td>D</td></tr><tr><td>E</td><td>F</td></tr></table>'
        bad = src.replace('<td>D</td></tr><tr>', '</tr><tr><td>D</td>')
        self.assertFalse(D4.score_item({"source": src}, bad)["table_cells"])
        self.assertFalse(D4.score_item({"source": src}, src.replace('<td>A', '<td colspan="2">A'))["table_cells"])

    def test_d4_link_binding_and_text_position(self):
        src = '<html><p><a href="a">A</a><a href="b">B</a></p><p>C</p></html>'
        swapped = src.replace('href="a"', 'href="z"').replace('href="b"', 'href="a"').replace('href="z"', 'href="b"')
        self.assertFalse(D4.score_item({"source": src}, swapped)["links_images"])
        self.assertFalse(D4.score_item({"source": src}, src.replace('>B</a>', '></a>').replace('<p>C', '<p>B<a/>C'))["pass"])
        result = D4.score_item({"source": src}, '<html>')
        self.assertIn("segment_map", result)
        self.assertFalse(result["pass"])

    def test_term_multiplicity(self):
        rec = {"ref_term": "mundo", "repeated": True, "kind": "glossary"}
        self.assertTrue(D5.score_item(rec, 'Texto [mundo | mundo]')["pass"])
        for bad in ('Texto [mundo]', 'Texto [mundo | mundo | mundo]', 'Texto [mundo | ]'):
            self.assertFalse(D5.score_item(rec, bad)["pass"])
        rec["repeated"] = False
        self.assertFalse(D5.score_item(rec, 'Texto [mundo | mundo]')["pass"])


if __name__ == "__main__":
    unittest.main()
