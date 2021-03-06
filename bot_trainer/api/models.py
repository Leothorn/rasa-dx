from pydantic import BaseModel, validator, ValidationError
from typing import List, Any
from enum import Enum
from bot_trainer.utils import Utility


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class User(BaseModel):
    email: str
    first_name: str
    last_name: str
    bot: str
    account: int
    status: bool
    alias_user: str = None
    is_integration_user: bool

    def get_bot(self):
        return self.bot

    def get_user(self):
        if self.is_integration_user:
            return self.alias_user
        return self.email


class Response(BaseModel):
    success: bool = True
    message: str = None
    data: Any
    error_code: int = 0


class RequestData(BaseModel):
    data: Any


class TextData(BaseModel):
    data: str


class ListData(BaseModel):
    data: List[str]


class StoryEventType(str, Enum):
    user = "user"
    action = "action"
    form = "form"
    slot = "slot"


class StoryEventRequest(BaseModel):
    name: str
    type: StoryEventType
    value: str = None


class StoryRequest(BaseModel):
    name: str
    events: List[StoryEventRequest]

    def get_events(self):
        return [event.dict() for event in self.events]


class RegisterAccount(BaseModel):
    email: str
    first_name: str
    last_name: str
    password: str
    confirm_password: str
    account: str
    bot: str

    @validator("confirm_password")
    def validate_password(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError("Password and Confirm Password does not match")
        return v


class EndPointBot(BaseModel):
    url: str
    token: str = None
    token_type: str = None


class EndPointAction(BaseModel):
    url: str


class EndPointTracker(BaseModel):
    type: str = "mongo"
    url: str
    db: str
    username: str = None
    password: str = None
    auth_source: str = None


class Endpoint(BaseModel):
    bot_endpoint: EndPointBot = None
    action_endpoint: EndPointAction = None
    tracker_endpoint: EndPointTracker = None