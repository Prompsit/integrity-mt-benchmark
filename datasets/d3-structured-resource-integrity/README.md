# Prompsit D3 - Structured-resource Integrity

Software stores text in resource files: files that pair an identifier with text shown to users. For example, save_button identifies a button, while Save is its label. When translating the label into Spanish as Guardar, the identifier must remain unchanged. This dataset checks these kinds of requirements.

The examples use Android software translations arranged into small XML, JSON, properties and ARB files. Checks cover file syntax, identifiers, whether values remain text and protected fields. They also flag unchanged source text where the reference translation uses different wording. Passing does not establish translation accuracy or guarantee that a complete application can load the file.

Translations are from English into Catalan, Spanish, French, Italian, European Portuguese, German, Dutch, Polish and Russian.

Test translation workflows that accept and return software resource files. The workflow should translate the permitted text while preserving the required file structure.

See [DATASHEET.md](DATASHEET.md) for scoring instructions, the exact checks, source credits and dataset contents. The scoring code is in `build/`. A passing result means that the implemented checks passed; it is not an overall translation-quality score.
