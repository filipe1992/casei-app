from fastapi import APIRouter

from app.routes import auth, users, guests, invitations, timeline, gift_shop, dashboard, photos, photo_challenge, schedule, configuration, menu

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(configuration.router, prefix="/configuration", tags=["configuration"])
api_router.include_router(guests.router, prefix="/guests", tags=["guests"])
api_router.include_router(invitations.router, prefix="/invitations", tags=["invitations"])
api_router.include_router(timeline.router, prefix="/timeline", tags=["timeline"])
api_router.include_router(gift_shop.router, prefix="/gift-shop", tags=["gift-shop"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(photos.router, prefix="/photos", tags=["photos"])
api_router.include_router(photo_challenge.router, prefix="/photo-challenge", tags=["photo-challenge"])
api_router.include_router(schedule.router, prefix="/schedule", tags=["schedule"])
api_router.include_router(menu.router, prefix="/menu", tags=["menu"])