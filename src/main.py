from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from src.core.config import settings
from src.auth.router import router as auth_router
from src.users.router import router as users_router

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize anything needed at startup
    yield
    # Clean up at shutdown


app = FastAPI(
    title=settings.APP_NAME,
    description="API Template for FastAPI with PostgreSQL and JWT Authentication",
    version="1.0.0",
    lifespan=lifespan,
)

# Set up CORS
logger.debug(f"CORS Configuration - Origins: {settings.CORS_ORIGINS}, Headers: {settings.CORS_HEADERS}")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=r"http:\/\/localhost:\d+",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=settings.CORS_HEADERS,
    expose_headers=["*"]
)

@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = ",".join(settings.CORS_HEADERS)
    return response

# Include routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint that redirects to API documentation."""
    return {
        "message": "Welcome to the API",
        "documentation": "/docs",
        "health_check": "/api/v1/health"
    }

@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "1.0.0"
    }
