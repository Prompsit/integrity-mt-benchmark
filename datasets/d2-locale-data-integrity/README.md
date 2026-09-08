# Prompsit D2 - Locale-data Integrity

Numbers and dates can be written differently across languages and regions. For example, the English decimal number 12.5 is written as 12,5 in French. This dataset checks whether a translation uses an accepted format for the requested language and region.

Each example adds one number, date, currency amount or measurement in square brackets to a sentence from software translation catalogs. Expected formats come from Unicode CLDR, a collection of language and regional conventions. The check covers the bracketed value only. Amounts and units stay the same; currency and measurement conversions are outside the task.

Translations are from English into Catalan, Spanish, French, Italian, European Portuguese, German, Dutch, Polish and Russian.

Test whether translation tools format numbers, dates, currencies and units for the requested language and region. The tool must keep the bracketed value in its output.

See [DATASHEET.md](DATASHEET.md) for scoring instructions, the exact checks, source credits and dataset contents. The scoring code is in `build/`. A passing result means that the implemented checks passed; it is not an overall translation-quality score.
