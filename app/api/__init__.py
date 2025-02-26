from fastapi import APIRouter
from .auth import auth_router
from .books import books_router

api_router = APIRouter(prefix="/api")

api_routers_tuple = (
    auth_router,
    books_router
)

for router in api_routers_tuple:
    api_router.include_router(router)

__all__ = ["api_router"]
