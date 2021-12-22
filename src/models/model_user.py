import uuid

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID

from src.models.model_base import ModelBase


class User(ModelBase):
    __tablename__ = 'user'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
