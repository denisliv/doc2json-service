import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine
from app.seed import seed_initial_data

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting doc2json-service...")
    await seed_initial_data()
    yield
    await engine.dispose()
    logger.info("doc2json-service shut down.")


app = FastAPI(
    title="Doc2JSON Service",
    description="PDF document processing: OCR, routing, structured data extraction",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.auth.router import router as auth_router  # noqa: E402
from app.documents.router import router as documents_router  # noqa: E402
from app.document_types.router import router as doc_types_router  # noqa: E402
from app.validation.router import router as validation_router  # noqa: E402
from app.admin.router import router as admin_router  # noqa: E402
from app.processing.ocr_router import router as ocr_router  # noqa: E402

app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(documents_router, prefix="/api/v1/documents", tags=["Documents"])
app.include_router(doc_types_router, prefix="/api/v1/document-types", tags=["Document Types"])
app.include_router(validation_router, prefix="/api/v1/validate", tags=["Validation"])
app.include_router(admin_router, prefix="/api/v1/admin", tags=["Admin"])
app.include_router(ocr_router, prefix="/api/v1/ocr", tags=["OCR"])
