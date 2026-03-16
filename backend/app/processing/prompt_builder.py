"""Dynamic prompt generation from database document types."""

import json

from langchain_core.messages import HumanMessage, SystemMessage

ROUTER_TEMPLATE = """Ты — классификатор документов. По тексту документа в Markdown формате определи, к какой категории он относится.

КАТЕГОРИИ:

{categories}

Верни **только валидный JSON** с одним ключом `route` и значением — строго одним из допустимых slug-ов.
Без пояснений, без комментариев.

Пример ответа:
{{"route": "some_slug"}}
"""


def build_router_messages(markdown: str, active_types: list[dict]) -> list:
    categories = []
    for i, dt in enumerate(active_types, 1):
        categories.append(
            f"{i}. **{dt['name']}** (`{dt['slug']}`)\n"
            f"   {dt.get('description', '')}\n"
            f"   Признаки: {dt.get('router_hints', '')}"
        )
    categories.append(
        f"{len(active_types) + 1}. **Прочее** (`other`)\n"
        f"   Документ не относится ни к одной из категорий выше."
    )

    system_text = ROUTER_TEMPLATE.format(categories="\n\n".join(categories))
    user_text = (
        "Определи категорию документа по тексту ниже. "
        "Верни JSON с ключом route.\n\n"
        f"Текст документа:\n\n{markdown[:30000]}"
    )
    return [SystemMessage(content=system_text), HumanMessage(content=user_text)]


def build_extraction_messages(markdown: str, doc_type: dict) -> list:
    format_instructions = json.dumps(doc_type["json_schema"], ensure_ascii=False, indent=2)
    system_text = doc_type["system_prompt"].replace("{format_instructions}", format_instructions)
    user_text = doc_type["user_prompt"].replace("{report}", markdown)
    return [SystemMessage(content=system_text), HumanMessage(content=user_text)]
