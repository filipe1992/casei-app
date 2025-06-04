# Import base class for SQLAlchemy
from app.db.base_class import Base

# Import all models for Alembic
from app.models.user import User  # noqa
from app.models.guest import Guest  # noqa
from app.models.invitation import Invitation  # noqa
from app.models.timeline import Timeline, TimelineItem  # noqa
from app.models.gift_shop import GiftShop, GiftProduct, GiftShopBuyProduct  # noqa
from app.models.photo import Photo  # noqa
from app.models.photo_challenge import PhotoChallenge, ChallengeTask, CompletedChallengeTask  # noqa
from app.models.schedule import Schedule, ScheduleItem  # noqa

# Todos os modelos devem ser importados aqui para que o Alembic possa detectá-los
# O comentário noqa é usado para evitar warnings do linter sobre importações não utilizadas 