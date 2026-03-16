"""Celery tasks for document processing."""

import logging

from app.processing.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=3, default_retry_delay=10)
def process_job(self, job_id: str):
    """OCR -> Router -> Extract -> Postprocess -> Validate -> Save."""
    try:
        from app.processing.pipeline import run_pipeline
        run_pipeline(job_id)
    except Exception as exc:
        logger.exception("Task process_job failed for job %s", job_id)
        self.retry(exc=exc)
