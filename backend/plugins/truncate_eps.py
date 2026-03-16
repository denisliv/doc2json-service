"""Обрезка Markdown после строки «Разводненная прибыль (убыток) на акцию | 260 |»."""

PLUGIN_TYPE = "markdown"


def process(data, **context):
    if not isinstance(data, str):
        return data
    lines = data.splitlines(keepends=True)
    pattern = "| Разводненная прибыль (убыток) на акцию | 260 |"
    for i, line in enumerate(lines):
        if line.strip().startswith(pattern):
            return "".join(lines[: i + 1])
    return data
