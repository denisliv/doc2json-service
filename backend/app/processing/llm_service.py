"""LLM service: routing, extraction, JSON repair. Synchronous, runs in Celery worker."""

import json
import logging
import re

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from tenacity import retry, stop_after_attempt, wait_fixed

from app.config import settings
from app.processing.prompt_builder import build_extraction_messages, build_router_messages

logger = logging.getLogger(__name__)


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
        """Extract structured JSON from markdown using doc_type prompts and schema."""
        messages = build_extraction_messages(markdown, doc_type)
        result = self.llm.invoke(messages)
        raw = result.content.strip()
        raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw, flags=re.MULTILINE).strip()

        try:
            return json.loads(raw)
        except json.JSONDecodeError as e:
            logger.warning("Primary parse failed: %s", e)
            fixed = self._fix_json(raw, doc_type["json_schema"], str(e))
            return json.loads(fixed)

    def _fix_json(self, broken: str, schema: dict, initial_error: str, max_attempts: int = 3) -> str:
        """Attempt to repair invalid JSON using LLM."""
        format_instructions = json.dumps(schema, ensure_ascii=False, indent=2)
        fix_template = ChatPromptTemplate.from_messages([
            ("system",
             "Ты — эксперт по данным. Исправь текст так, чтобы он стал ВАЛИДНЫМ JSON, "
             "строго соответствующим схеме.\n\nСхема:\n{format_instructions}\n\n"
             "Ошибка парсинга:\n{error_message}\n\nВАЖНО:\n"
             "1. Верни ТОЛЬКО чистый JSON без ```обёрток, комментариев или пояснений.\n"
             "2. Не добавляй полей, которых нет в схеме.\n"
             "3. Сохраняй типы данных (числа — без кавычек, строки — в двойных кавычках)."),
            ("user", "Исходный текст:\n{broken_json_text}"),
        ])

        current_text = broken
        last_error = initial_error

        for attempt in range(max_attempts):
            messages = fix_template.format_messages(
                broken_json_text=current_text,
                format_instructions=format_instructions,
                error_message=last_error,
            )
            resp = self.llm.invoke(messages)
            candidate = resp.content.strip()
            candidate = re.sub(r"^```(?:json)?\s*|\s*```$", "", candidate, flags=re.MULTILINE).strip()

            try:
                json.loads(candidate)
                return candidate
            except json.JSONDecodeError as e:
                last_error = f"Attempt {attempt + 1} failed: {e}"
                logger.warning("JSON repair attempt %d failed: %s", attempt + 1, e)
                current_text = candidate

        return current_text
