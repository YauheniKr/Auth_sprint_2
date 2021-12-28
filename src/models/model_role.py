import uuid

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates

from src.models.model_base import ModelBase


class Role(ModelBase):
    __tablename__ = 'role'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    role_name = Column(String, unique=True, nullable=False)
    role_weight = Column(Integer, unique=True, nullable=False)
    description = Column(String(255))

    def __repr__(self):
        return f'{self.role_name}'

    def to_json(self):
        return {
            'id': str(self.id),
            'role_name': self.role_name,
            'role_weight': self.role_weight,
        }

class Role_User(ModelBase):
    __tablename__ = 'role_user'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column("user_id", UUID(as_uuid=True), ForeignKey("user.id"))
    role_id = Column("role_id", UUID(as_uuid=True), ForeignKey("role.id"))
