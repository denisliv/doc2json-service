"""PaddleOCR-VL: PDF files -> Markdown text. Runs synchronously inside Celery worker."""

import gc
import logging

from bs4 import BeautifulSoup
from paddleocr import PaddleOCRVL

from app.config import settings

logger = logging.getLogger(__name__)


def _simple_html_table_to_markdown(table) -> str:
    rows = []
    for tr in table.find_all("tr"):
        cells = tr.find_all(["td", "th"])
        row = [cell.get_text(strip=True).replace("\n", " ") for cell in cells]
        rows.append(row)
    if not rows:
        return ""
    max_cols = max(len(row) for row in rows)
    for row in rows:
        while len(row) < max_cols:
            row.append("")
    lines = []
    for i, row in enumerate(rows):
        line = "| " + " | ".join(row) + " |"
        lines.append(line)
        if i == 0:
            separator = "| " + " | ".join(["---"] * max_cols) + " |"
            lines.append(separator)
    return "\n".join(lines)


def html_to_markdown_with_tables(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    output = []
    for element in soup.children:
        if element.name == "table":
            md_table = _simple_html_table_to_markdown(element)
            output.append(md_table)
            output.append("")
        else:
            text = element.get_text(strip=True)
            if text:
                output.append(text)
                output.append("")
    return "\n".join(output)


class OCRService:
    """PaddleOCR-VL: PDF -> Markdown. Synchronous, runs in Celery worker."""

    def process_files(self, pdf_paths: list[str]) -> str:
        """Process each PDF with a fresh PaddleOCR instance; release memory after each document."""
        all_markdown = []
        for path in pdf_paths:
            ocr = None
            try:
                ocr = PaddleOCRVL(
                    vl_rec_backend=settings.OCR_VL_BACKEND,
                    vl_rec_server_url=settings.OCR_VL_SERVER_URL,
                    vl_rec_model_name=settings.OCR_VL_MODEL_NAME,
                    layout_detection_model_name=settings.OCR_LAYOUT_MODEL_NAME,
                    layout_detection_model_dir=settings.OCR_LAYOUT_MODEL_DIR,
                    doc_orientation_classify_model_name=settings.OCR_ORIENTATION_MODEL_NAME,
                    doc_orientation_classify_model_dir=settings.OCR_ORIENTATION_MODEL_DIR,
                    doc_unwarping_model_dir=settings.OCR_UNWARPING_MODEL_DIR,
                    doc_unwarping_model_name=settings.OCR_UNWARPING_MODEL_NAME,
                    use_doc_orientation_classify=settings.OCR_USE_ORIENTATION,
                    use_doc_unwarping=settings.OCR_USE_UNWARPING,
                    use_layout_detection=settings.OCR_USE_LAYOUT,
                    use_ocr_for_image_block=settings.OCR_USE_OCR_FOR_IMAGE,
                    format_block_content=settings.OCR_FORMAT_BLOCK_CONTENT,
                    merge_layout_blocks=settings.OCR_MERGE_LAYOUT_BLOCKS,
                    layout_threshold=settings.OCR_LAYOUT_THRESHOLD,
                    layout_nms=settings.OCR_LAYOUT_NMS,
                    layout_merge_bboxes_mode=settings.OCR_LAYOUT_MERGE_MODE,
                    use_queues=settings.OCR_USE_QUEUES,
                )
                logger.info("PaddleOCRVL %s initialized for document", settings.OCR_VL_MODEL_NAME)

                output = ocr.predict(
                    input=path,
                    temperature=settings.OCR_TEMPERATURE,
                    top_p=settings.OCR_TOP_P,
                    repetition_penalty=settings.OCR_REPETITION_PENALTY,
                )
                pages = list(output)
                result = ocr.restructure_pages(
                    pages, merge_tables=True, relevel_titles=True, concatenate_pages=True
                )
                all_markdown.append(result[0].markdown["markdown_texts"])
            finally:
                if ocr is not None:
                    del ocr
                    gc.collect()
                    logger.info("PaddleOCRVL released")

        joined = "\n".join(all_markdown)
        return html_to_markdown_with_tables(joined)
