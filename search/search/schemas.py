from enum import Enum

from pydantic import BaseModel


class ActionEnum(str, Enum):
    create = "create"
    update = "update"
    delete = "delete"


class SearchIndex(BaseModel):
    action: ActionEnum
    object: str
    current: dict
    previous: dict
    user: dict
