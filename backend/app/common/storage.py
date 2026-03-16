import shutil
from datetime import datetime, timezone
from pathlib import Path

from app.config import settings


def _base_dir() -> Path:
    return Path(settings.STORAGE_DIR)


def _date_prefix() -> str:
    now = datetime.now(timezone.utc)
    return f"{now.year}/{now.month:02d}"


def get_upload_dir(job_id: str) -> Path:
    path = _base_dir() / "uploads" / _date_prefix() / job_id
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_result_dir(job_id: str) -> Path:
    path = _base_dir() / "results" / _date_prefix() / job_id
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_markdown_dir(job_id: str) -> Path:
    path = _base_dir() / "markdown" / _date_prefix() / job_id
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_file(directory: Path, filename: str, data: bytes) -> Path:
    filepath = directory / filename
    filepath.write_bytes(data)
    return filepath


def delete_job_files(job_id: str) -> None:
    for subdir in ("uploads", "results", "markdown"):
        base = _base_dir() / subdir
        if not base.exists():
            continue
        for year_dir in base.iterdir():
            for month_dir in year_dir.iterdir():
                target = month_dir / job_id
                if target.exists():
                    shutil.rmtree(target)
