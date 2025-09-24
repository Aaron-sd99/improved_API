from fastapi import FastAPI
from app.core.logging import setup_logging
from app.db.base import Base, engine
from app.middlewares.cors import apply_cors
from app.middlewares.request_id import RequestIDMiddleware
from app.routers import (
    auth_router, users_router, orgs_router, blogs_router,
    posts_router, comments_router, attachment_router, audit_router, health_router
)

def create_app():
    setup_logging()
    Base.metadata.create_all(bind=engine)
    app = FastAPI(title="Blog Enterprise (multi-tenant)")
    apply_cors(app)
    app.add_middleware(RequestIDMiddleware)

    app.include_router(auth_router.router)
    app.include_router(users_router.router)
    app.include_router(orgs_router.router)
    app.include_router(blogs_router.router)
    app.include_router(posts_router.router)
    app.include_router(comments_router.router)
    app.include_router(attachment_router.router)
    app.include_router(audit_router.router)
    app.include_router(health_router.router)
    return app

app = create_app()
