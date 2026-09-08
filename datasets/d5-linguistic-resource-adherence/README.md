# Prompsit D5 - Linguistic-resource Adherence

Translation workflows may receive a glossary of required terms or a translation memory: previously translated sentences provided for reuse. This dataset checks whether the output uses the prescribed term, repeats it when required, and avoids terms explicitly listed as disallowed.

The examples combine software translation sentences with added term fields and constructed glossary or translation-memory examples. Some cases include an outdated suggested term or conflicting instructions. Glossary and translation-memory results are reported separately. The checks assess term use, not reuse of an entire sentence or overall translation quality.

Translations are from English into Catalan, Spanish, French, Italian, European Portuguese, German, Dutch, Polish and Russian.

Test translation workflows that can receive a glossary or translation memory. Report the two types of result separately, and identify any resource type the workflow does not support.

See [DATASHEET.md](DATASHEET.md) for scoring instructions, the exact checks, source credits and dataset contents. The scoring code is in `build/`. A passing result means that the implemented checks passed; it is not an overall translation-quality score.
