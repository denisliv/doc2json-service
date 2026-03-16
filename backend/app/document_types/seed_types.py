"""Built-in document types seeded on first startup."""

ACCOUNTING_STATEMENTS_SYSTEM_PROMPT = """Ты — эксперт в извлечении структурированных финансовых данных из форм бухгалтерской отчётности в Markdown формате.
Твоя задача — преобразовать текстовое (табличное) описание в строго валидный JSON формата AccountingStatementModel:

1. **Найди Бухгалтерский баланс и извлеки 4 компонента**:
   - `balance_head_table` — шапка баланса (если не указаны — ключ остается, значение - null):
        - организация,
        - учетный номер плательщика,
        - вид экономической деятельности,
        - организационно-правовая форма,
        - орган управления,
        - единица измерения,
        - адрес.
   - `balance_dates_table` (если не указаны — ключ остается, значение - null):
        - дата утверждения,
        - дата отправки,
        - дата принятия.
   - `balance_main_table_dates` — **две даты из заголовков колонок баланса**:
     *первая* — более поздняя (например, "30.06.2025"),
     *вторая* — более ранняя (например, "31.12.2024").
     Всегда выводи в порядке: **[более поздняя дата, более ранняя дата]** как строки в формате "ДД.ММ.ГГГГ".
   - `balance_main_table` — таблица из документа Бухгалтерский баланс: ключ — строковый код строки (например, "110", "470"), значение — **массив из двух элементов**:
     **[значение за более позднюю дату, значение за более раннюю дату]**. Если значения неизвестны или нечитаемы, выводи массив **[null, null]**.
3. **Найди Отчёт о прибылях и убытках и извлеки 1 компонент:**
   - `report_main_table` — таблица из документа Отчёт о прибылях и убытках: : ключ — строковый код строки (например, "010", "120"), значение — **массив из двух элементов**:
     **[значение за более позднюю дату, значение за более раннюю дату]**. Если значения неизвестны или нечитаемы, выводи массив **[null, null]**.

4. **Правила обработки значений**:
   - Любые пропуски, любые прочерки, тире ("—", "-", "—", "–") заменяй на `null`.
   - Если значение в ячейке отсутствует, используй null, а не "-", "—", пустую строку или любой другой символ.
   - Пробелы в числах (например, "9 044") удаляй, преобразуй в целое число `9044`.
   - Отрицательным считается ТОЛЬКО число, начинающееся с символа минуса (`-`), например: `-186`.
   - Все коды строк — **всегда строки**, даже если состоят из цифр (например, "110", а не 110).
   - Если значение отсутствует или нечитаемо — ставь `null`.
   - Не интерпретируй, не агрегируй, не исправляй логические ошибки — только извлекай то, что видишь.

5. **Формат выхода**:
   - Верни **только валидный JSON**, строго соответствующий Pydantic-схеме.
   - Без пояснений, без комментариев, без markdown.
   - Убедись, что:
     ✓ Все поля присутствуют (даже если null),
     ✓ Нет лишних ключей,
     ✓ JSON валиден (проверь кавычки, запятые, скобки),
     ✓ В JSON отсутствуют тире ("—", "-", "—", "–"),
     ✓ Поля `balance_main_table` и `report_main_table` содержат **все коды строк**, присутствующие в документе (включая те, где оба значения null).

ВАЖНО:
- Если в исходном документе значение отсутствует, нечитаемо или указан прочерк — выводи `null`, не используй "-1", "0".
- НИКОГДА не придумывай числовые значения.
- Не используй примеры из памяти — только то, что видишь в документе.


{format_instructions}"""

ACCOUNTING_STATEMENTS_USER_PROMPT = """Проанализируй следующий отчет и извлеки структурированные данные строго по правилам:

{report}"""

OFFICIAL_REQUEST_SYSTEM_PROMPT = """Ты — эксперт в извлечении структурированных данных из официальных обращений.
Твоя задача — проанализировать документ и извлечь из него данные **строго в соответствии с заданной схемой OfficialRequestModel**, используя только ту информацию, которая **присутствует в тексте**.

ОБЩИЕ ПРАВИЛА:
1. Возвращай ТОЛЬКО валидный JSON, соответствующий переданной Pydantic-схеме.
2. Структура JSON должна быть сохранена полностью, без удаления полей.
3. Извлекай ТОЛЬКО те данные, которые:
   - прямо и однозначно присутствуют в тексте,
   - могут быть подтверждены буквальным фрагментом документа.
4. Любые догадки, логические выводы, обобщения и «очевидные» предположения ЗАПРЕЩЕНЫ.

ПРАВИЛА ЗАПОЛНЕНИЯ ПОЛЕЙ:
- Если значение явно указано в тексте → заполни поле дословно.
- Если значение отсутствует или неочевидно → null.
- Для массивов:
  - если сущностей нет → []
  - если есть хотя бы одна → массив объектов.
- **Периоды времени** (например, «за последние три года») указывайте в поле `period` как есть. Если речь о «настоящем времени», считай текущей датой момент обработки.
- Разделяй сущности: если в запросе упомянуто несколько организаций или физических лиц — создай отдельные элементы в соответствующих массивах (`fizik`, `urik`).
- Не объединяй разные сущности в одно поле.
- Не перефразируй текст документа.

ЮРИДИЧЕСКИЕ СУЩНОСТИ:
- ФИО, наименования организаций, УНП, номера дел, даты, названия судов извлекай строго в том виде, как они указаны в тексте.
- При наличии ссылки на **ст. 106 Закона №227-З** — укажите `"ссылка на ст.106 есть"`, иначе — `"ссылки на ст.106 нет"`.
- Если в тексте есть упоминание арбитражного суда, банкротства, конкурсного управления — извлеките это в поле `sud`.

СПЕЦИАЛЬНЫЕ ОГРАНИЧЕНИЯ:
- Не интерпретируй цель письма, если она не оформлена заголовком.
- Не выводи тип запроса по содержанию — только по явной формулировке.
- Не догадывайся о сроках, периодах и объёмах данных.

ВЫХОД:
- Верни **только валидный JSON**, строго соответствующий Pydantic-схеме.
- Без пояснений, без комментариев.
- Убедись, что:
  ✓ Все поля присутствуют (даже если null),
  ✓ Нет лишних ключей,
  ✓ JSON валиден (проверь кавычки, запятые, скобки),

{format_instructions}"""

OFFICIAL_REQUEST_USER_PROMPT = """Проанализируй следующий оффициальный запрос и извлеки структурированные данные строго по правилам:

{report}"""

# JSON Schemas generated from existing Pydantic models (model_json_schema())
ACCOUNTING_STATEMENTS_SCHEMA = {
    "type": "object",
    "required": ["tables_data"],
    "properties": {
        "tables_data": {
            "type": "object",
            "required": [
                "balance_head_table",
                "balance_dates_table",
                "balance_main_table_dates",
                "balance_main_table",
                "report_main_table",
            ],
            "properties": {
                "balance_head_table": {
                    "type": "object",
                    "properties": {
                        "Организация": {"type": ["string", "null"]},
                        "Учетный номер плательщика": {"type": ["integer", "null"]},
                        "Вид экономической деятельности": {"type": ["string", "null"]},
                        "Организационно-правовая форма": {"type": ["string", "null"]},
                        "Орган управления": {"type": ["string", "null"]},
                        "Единица измерения": {"type": ["string", "null"]},
                        "Адрес": {"type": ["string", "null"]},
                    },
                },
                "balance_dates_table": {
                    "type": "object",
                    "properties": {
                        "Дата утверждения": {"type": ["string", "null"]},
                        "Дата отправки": {"type": ["string", "null"]},
                        "Дата принятия": {"type": ["string", "null"]},
                    },
                },
                "balance_main_table_dates": {
                    "type": "array",
                    "items": {"type": ["string", "null"]},
                    "description": "Даты двух столбцов основной таблицы баланса в формате ДД.ММ.ГГГГ",
                },
                "balance_main_table": {
                    "type": "object",
                    "description": "Коды строк баланса -> массивы из двух значений [newer, older]",
                    "additionalProperties": {
                        "type": "array",
                        "items": {"type": ["integer", "null"]},
                        "minItems": 2,
                        "maxItems": 2,
                    },
                },
                "report_main_table": {
                    "type": "object",
                    "description": "Коды строк отчёта о прибылях и убытках -> массивы из двух значений",
                    "additionalProperties": {
                        "type": "array",
                        "items": {"type": ["integer", "null"]},
                        "minItems": 2,
                        "maxItems": 2,
                    },
                },
            },
        }
    },
}

OFFICIAL_REQUEST_SCHEMA = {
    "type": "object",
    "properties": {
        "sender": {"type": ["string", "null"]},
        "dateNumber": {"type": ["string", "null"]},
        "title": {"type": ["string", "null"]},
        "deadline": {"type": ["string", "null"]},
        "auditorName": {"type": ["string", "null"]},
        "email": {"type": ["string", "null"]},
        "period": {"type": ["string", "null"]},
        "requestType": {"type": ["string", "null"]},
        "adress": {"type": ["string", "null"]},
        "adress_sender": {"type": ["string", "null"]},
        "podpisant": {"type": ["string", "null"]},
        "law": {"type": ["string", "null"]},
        "fizik": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "fullName": {"type": ["string", "null"]},
                    "identificationNumber": {"type": ["string", "null"]},
                    "seriesNumber": {"type": ["string", "null"]},
                    "government": {"type": ["string", "null"]},
                    "dateIssue": {"type": ["string", "null"]},
                    "registrationAddress": {"type": ["string", "null"]},
                    "dateBirth": {"type": ["string", "null"]},
                    "mobileNumber": {"type": ["string", "null"]},
                },
            },
        },
        "urik": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "nameOrganization": {"type": ["string", "null"]},
                    "unp": {"type": ["string", "null"]},
                },
            },
        },
        "bills": {"type": "object"},
        "transactions": {"type": "object"},
        "leftovers": {"type": ["string", "null"]},
        "cards": {"type": "object"},
        "credit": {"type": "object"},
        "garantii": {"type": "object"},
        "deposit": {"type": "object"},
        "informationSecurities": {"type": ["string", "null"]},
        "informationMetals": {"type": ["string", "null"]},
        "informationOwn": {"type": ["string", "null"]},
        "informationWallet": {"type": ["string", "null"]},
        "inoe": {"type": ["string", "null"]},
        "broni": {"type": ["string", "null"]},
        "ais": {"type": "object"},
        "arest": {"type": "object"},
        "sdbo": {"type": "object"},
        "customerInformation": {"type": "object"},
        "videoInformation": {"type": ["string", "null"]},
        "informationErip": {"type": ["string", "null"]},
        "other": {"type": ["string", "null"]},
        "sud": {"type": ["string", "null"]},
        "doverennost": {"type": ["string", "null"]},
        "closeForm": {"type": ["string", "null"]},
    },
}


BUILTIN_TYPES = [
    {
        "slug": "accounting_statements",
        "name": "Бухгалтерская отчётность",
        "description": "Бухгалтерский баланс и отчёт о прибылях и убытках",
        "json_schema": ACCOUNTING_STATEMENTS_SCHEMA,
        "system_prompt": ACCOUNTING_STATEMENTS_SYSTEM_PROMPT,
        "user_prompt": ACCOUNTING_STATEMENTS_USER_PROMPT,
        "router_hints": "Баланс, УНП, коды строк 110/120/470, финансовые показатели, две колонки с датами",
        "markdown_postprocessors": ["remove_parentheses", "truncate_eps"],
        "json_postprocessors": ["enrich_json"],
    },
    {
        "slug": "official_request",
        "name": "Официальные запросы",
        "description": "Обращения/запросы государственных органов",
        "json_schema": OFFICIAL_REQUEST_SCHEMA,
        "system_prompt": OFFICIAL_REQUEST_SYSTEM_PROMPT,
        "user_prompt": OFFICIAL_REQUEST_USER_PROMPT,
        "router_hints": "Запрос госоргана, суд, налоговая, ст. 106, закон 227-З, счета, карты",
        "markdown_postprocessors": [],
        "json_postprocessors": [],
    },
]
