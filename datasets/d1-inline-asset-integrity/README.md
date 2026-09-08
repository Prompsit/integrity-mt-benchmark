# Prompsit D1 - Inline Asset Integrity

Software text often contains more than words. It may include tags that mark bold text, placeholders such as {name}, or a web address that must stay unchanged. This dataset checks whether a translation preserves the supported elements and their syntax.

The examples come from software translation catalogs, with some markup added to cover more cases. The checks can detect missing or damaged elements. They do not determine whether every tag surrounds the right words or whether the translation itself is accurate.

Translations are from English into Catalan, Spanish, French, Italian, European Portuguese, German, Dutch, Polish and Russian.

Test translation tools used for software and other text containing tags or placeholders. Use the results alongside a separate assessment of translation quality.

See [DATASHEET.md](DATASHEET.md) for scoring instructions, the exact checks, source credits and dataset contents. The scoring code is in `build/`. A passing result means that the implemented checks passed; it is not an overall translation-quality score.
