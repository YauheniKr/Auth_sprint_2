import uuid

from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql import func

from tests.functional.models.model_base import ModelBase


class User(ModelBase):
    __tablename__ = 'user'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    username = Column(String(50), unique=True)
    password = Column(String(128))
    email = Column(String(70), unique=True, nullable=False)

    role = relationship("Role", secondary="role_user", backref=backref("users", lazy="dynamic"), cascade='all, delete')


class AuthHistory(ModelBase):
    __tablename__ = "auth_history"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False
    )
    user_id = Column("user_id", UUID(as_uuid=True), ForeignKey("user.id", ondelete="cascade"))
    timestamp = Column(DateTime, server_default=func.now())
    user_agent = Column(Text, nullable=False)
    ip_address = Column(String(20))
    device = Column(Text)
