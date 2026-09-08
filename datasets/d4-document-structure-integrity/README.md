# Prompsit D4 - Document-structure Integrity

Translating a document should preserve its structure as well as its text. This dataset checks the arrangement of elements such as headings, paragraphs and lists, the structure of tables, and the destinations of links and images in translated HTML.

The documents are built from software translation examples placed in a small set of templates. Automated checks compare the original and translated structures and check that the document follows the required syntax. They do not assess visual appearance or translation accuracy. Moving translated text into the wrong paragraph or table cell can still pass if the structure stays the same.

Translations are from English into Catalan, Spanish, French, Italian, European Portuguese, German, Dutch, Polish and Russian.

Test document translation workflows that accept and return HTML. Use the structural results alongside checks of translation quality and visual appearance.

See [DATASHEET.md](DATASHEET.md) for scoring instructions, the exact checks, source credits and dataset contents. The scoring code is in `build/`. A passing result means that the implemented checks passed; it is not an overall translation-quality score.
