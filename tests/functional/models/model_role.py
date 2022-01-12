import uuid

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from tests.functional.models.model_base import ModelBase


class Role(ModelBase):
    __tablename__ = 'role'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    role_name = Column(String, unique=True, nullable=False)
    role_weight = Column(Integer, unique=True, nullable=False)
    description = Column(String(255))

    def __repr__(self):
        return f'{self.role_name}'



class RoleUser(ModelBase):
    __tablename__ = 'role_user'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column("user_id", UUID(as_uuid=True), ForeignKey("user.id"))
    role_id = Column("role_id", UUID(as_uuid=True), ForeignKey("role.id"))
