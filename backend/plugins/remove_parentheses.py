"""Убирает скобки вокруг чисел в Markdown."""

import re

PLUGIN_TYPE = "markdown"


def process(data, **context):
    if not isinstance(data, str):
        return data

    def replace_match(m):
        inner = m.group(1)
        if re.fullmatch(r"[\d\s]+", inner.strip()):
            return inner
        return m.group(0)

    return re.sub(r"\(([^)]+)\)", replace_match, data)
