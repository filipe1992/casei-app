# Import all models here for Alembic
from app.models.user import User
from app.models.guest import Guest
from app.models.invitation import Invitation
from app.models.timeline import Timeline, TimelineItem
from app.models.gift_shop import GiftShop, GiftProduct

# Make sure all models are imported before initializing Alembic 