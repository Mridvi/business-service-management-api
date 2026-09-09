from app.database.base import Base
from app.database.session import engine
import app.models
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from pathlib import Path


from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.core.config import settings
from app.core.limiter import limiter

from app.api.v1.auth.router import router as auth_router
from app.api.v1.admin.router import router as admin_router
from app.api.v1.services.router import router as services_router
from app.api.v1.requests.router import router as requests_router


app = FastAPI(
    title="Business Service Management API",
    version="1.0.0",
    description=(
        "A RESTful API for managing business services and customer service requests. "
        "Provides JWT-based authentication, role-based access control, "
        "service catalog management, and service request lifecycle tracking."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
)


BASE_DIR = Path(__file__).resolve().parent
SWAGGER_CSS = "/frontend/css/swagger-custom.css"


@app.get("/custom-docs", include_in_schema=False)
async def custom_swagger_ui_html():
    response = get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - API Documentation",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    )

    html = response.body.decode("utf-8")

    html = html.replace(
        "</head>",
        '<link rel="stylesheet" href="/frontend/css/swagger-custom.css"></head>'
    )

    return HTMLResponse(content=html)

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"

app.mount(
    "/frontend",
    StaticFiles(directory=FRONTEND_DIR, html=True),
    name="frontend",
)



if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


if settings.cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app.include_router(
    auth_router,
    prefix="/api/v1",
    tags=["Authentication"],
)

app.include_router(
    admin_router,
    prefix="/api/v1",
    tags=["Administration"],
)

app.include_router(
    services_router,
    prefix="/api/v1",
    tags=["Services"],
)

app.include_router(
    requests_router,
    prefix="/api/v1",
    tags=["Service Requests"],
)

# Static files
Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

app.mount(
    settings.MEDIA_URL_PREFIX,
    StaticFiles(directory=settings.UPLOAD_DIR),
    name="media",
)


@app.get("/")
def health_check() -> dict:
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "ok",
    }