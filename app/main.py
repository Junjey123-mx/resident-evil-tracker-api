from fastapi import FastAPI

from app.core.config import get_settings
from app.core.constants import API_VERSION_FALLBACK, PROJECT_DESCRIPTION, PROJECT_NAME
from app.core.cors import configure_cors
from app.core.exceptions import register_exception_handlers
from app.core.response_models import HealthResponse
from app.modules.activity_logs.activity_router import router as activity_router
from app.modules.archive_entries.archive_entry_router import router as archive_router
from app.modules.cover_assets.cover_router import router as cover_router
from app.modules.dashboard.dashboard_router import router as dashboard_router
from app.modules.personal_ratings.rating_router import router as rating_router

settings = get_settings()

app = FastAPI(
    title=PROJECT_NAME,
    description=PROJECT_DESCRIPTION,
    version=getattr(settings, "app_version", API_VERSION_FALLBACK),
    docs_url="/docs",
    openapi_url="/openapi.json",
)

configure_cors(app)
register_exception_handlers(app)

app.include_router(archive_router)
app.include_router(rating_router)
app.include_router(cover_router)
app.include_router(activity_router)
app.include_router(dashboard_router)


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service=PROJECT_NAME,
        environment=settings.app_env,
        version=settings.app_version,
    )
