import uuid

from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.models.model_base import ModelBase


class Role(ModelBase):
    __tablename__ = 'role'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    role_name = Column(String, unique=True, nullable=False)
    role_weight = Column(Integer, unique=True, nullable=False)
    role_user = relationship('User', back_populates="user")

    def __repr__(self):
        return f'{self.role_name}'
