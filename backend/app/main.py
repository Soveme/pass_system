from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.config import settings
from app.routers import auth, passes, admin, scan, notifications, demo, visits
from app.middleware.security import SecurityHeadersMiddleware, RequestLoggingMiddleware, RateLimitMiddleware

app = FastAPI(
    title="Pass System API",
    description="Digital Access Control System with Pass Management",
    version="0.1.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    redoc_url="/api/redoc"
)

# Security middleware
# app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(RateLimitMiddleware, requests_per_minute=100)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins + ["http://localhost:5173", "http://localhost:5174", "http://localhost:5175"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(passes.router)
app.include_router(admin.router)
app.include_router(scan.router)
app.include_router(notifications.router)
app.include_router(demo.router)
app.include_router(visits.router)

# Custom OpenAPI schema for better Swagger UI
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Pass System API",
        version="0.1.0",
        description="Digital Access Control System - Complete API Documentation",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "0.1.0"}

@app.get("/")
async def root():
    return {
        "message": "Pass System API v0.1.0 - Digital Access Control System",
        "docs_url": "/api/docs",
        "openapi_url": "/api/openapi.json",
        "health_check": "/health",
        "demo_endpoint": "/api/demo/users",
        "create_demo_users": "/api/demo/create-demo-users"
    }
