"""LLM service: routing, extraction, JSON repair. Synchronous, runs in Celery worker.
Логика _fix_json приведена к родительскому pipeline.py: валидация через схему (аналог parser.parse)."""

import json
import logging
import re

import jsonschema
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from tenacity import retry, stop_after_attempt, wait_fixed

from app.config import settings
from app.processing.prompt_builder import (
    FIX_JSON_SYSTEM_PROMPT,
    FIX_JSON_USER_PROMPT,
    build_extraction_messages,
    build_router_messages,
)

logger = logging.getLogger(__name__)


def _parse_and_validate(raw: str, schema: dict):
    """Парсинг JSON и валидация по схеме (аналог parser.parse в родительском pipeline)."""
    stripped = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw, flags=re.MULTILINE).strip()
    data = json.loads(stripped)
    jsonschema.Draft202012Validator(schema).validate(data)
    return data


class LLMService:
    def __init__(self):
        self.llm = ChatOpenAI(
            base_url=settings.LLM_API_URL,
            api_key=settings.LLM_API_KEY,
            model=settings.LLM_MODEL_NAME,
            temperature=settings.LLM_TEMPERATURE,
            top_p=settings.LLM_TOP_P,
            max_tokens=settings.LLM_MAX_TOKENS,
            reasoning_effort=settings.LLM_REASONING_EFFORT,
            timeout=settings.LLM_TIMEOUT,
        )

    def route(self, markdown: str, active_types: list[dict]) -> str:
        """Determine document type from markdown text using all active types."""
        messages = build_router_messages(markdown, active_types)
        result = self.llm.invoke(messages)
        raw = result.content.strip()
        raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw, flags=re.MULTILINE).strip()
        try:
            parsed = json.loads(raw)
            return parsed.get("route", "other")
        except json.JSONDecodeError:
            logger.warning("Router returned non-JSON: %s", raw[:200])
            return "other"

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
    def extract(self, markdown: str, doc_type: dict) -> dict:
        """Extract structured JSON from markdown. Как в родительском pipeline: parse + validate по схеме."""
        messages = build_extraction_messages(markdown, doc_type)
        result = self.llm.invoke(messages)
        raw = result.content

        try:
            return _parse_and_validate(raw, doc_type["json_schema"])
        except Exception as e:
            logger.warning("Primary parse failed: %s", e)
            fixed = self._fix_json(raw, doc_type["json_schema"], str(e))
            try:
                return _parse_and_validate(fixed, doc_type["json_schema"])
            except Exception as e3:
                logger.error(
                    "JSON repair pipeline failed. Original (truncated): %.500s | Fixed (truncated): %.500s | Error: %s",
                    raw, fixed, e3,
                )
                raise

    def _fix_json(self, broken: str, schema: dict, initial_error: str, max_attempts: int = 3) -> str:
        """Исправление невалидного JSON через LLM. Как в pipeline._fix_json_with_llm: валидация через схему."""
        format_instructions = json.dumps(schema, ensure_ascii=False, indent=2)
        fix_template = ChatPromptTemplate.from_messages([
            ("system", FIX_JSON_SYSTEM_PROMPT),
            ("user", FIX_JSON_USER_PROMPT),
        ])

        current_text = broken
        last_error = initial_error or "Неизвестная ошибка"

        for attempt in range(max_attempts):
            messages = fix_template.format_messages(
                broken_json_text=current_text,
                format_instructions=format_instructions,
                error_message=last_error,
            )
            resp = self.llm.invoke(messages)
            candidate = resp.content.strip()
            candidate = re.sub(r"^```(?:json)?\s*|\s*```$", "", candidate, flags=re.MULTILINE)
            candidate = candidate.strip()

            try:
                _parse_and_validate(candidate, schema)
                return candidate
            except Exception as e:
                last_error = f"Попытка {attempt + 1} неудачна. Ошибка: {str(e)}"
                logger.warning("JSON repair attempt %d failed: %s", attempt + 1, e)
                current_text = candidate

        return candidate
