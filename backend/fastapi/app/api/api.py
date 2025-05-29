from fastapi import APIRouter

from app.routes import auth, users, guests, invitations, timeline, gift_shop, dashboard

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(guests.router, prefix="/guests", tags=["guests"])
api_router.include_router(invitations.router, prefix="/invitations", tags=["invitations"])
api_router.include_router(timeline.router, prefix="/timeline", tags=["timeline"])
api_router.include_router(gift_shop.router, prefix="/gift-shop", tags=["gift-shop"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])