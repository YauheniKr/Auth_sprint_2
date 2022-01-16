import datetime
from typing import Optional

import orjson
from pydantic import UUID4
from pydantic import BaseModel as PydanticBaseModel
from pydantic import Field


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseModel(PydanticBaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        allow_population_by_field_name = True


class RoleModel(BaseModel):
    id: UUID4
    role_weight: int
    role_name: str
    description: str = None


class RoleUserModel(BaseModel):
    role_weight: int
    role_name: str


class AuthHistoryBase(BaseModel):
    id: UUID4
    timestamp: datetime.datetime
    user_agent: str
    ipaddress: str
    device: str = None


class AuthHistoryModel(BaseModel):
    page: int
    limit: int
    count: int
    previous: str = ''
    next: str = ''
    results: Optional[list[AuthHistoryBase]] = Field(default_factory=list)
