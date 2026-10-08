from pydantic import BaseModel
from enum import Enum
from typing import Literal


class JoinResult(str,Enum):
    SUCCESS='success'
    ROOM_NOT_FOUND='room_not_found'
    ALREADY_JOINED='already_joined'

class LeaveResult(str,Enum):
    SUCCESS='success'
    ROOM_NOT_FOUND='room_not_found'
    NOT_A_MEMBER='not_a_member'


class ServerEventType(str,Enum):
    ROOM_CREATED='room_created'
    ROOM_JOINED='room_joined'
    ROOM_LEFT='room_left'
    MESSAGE='message'
    ERROR='error'


class OutRoomCreatedEvent(BaseModel):
    event_type:Literal[ServerEventType.ROOM_CREATED]=ServerEventType.ROOM_CREATED
    room_id:str

class OutRoomJoinedEvent(BaseModel):
    event_type:Literal[ServerEventType.ROOM_JOINED]=ServerEventType.ROOM_CREATED
    room_id:str
    username:str

class OutRoomLeftEvent(BaseModel):
    event_type: Literal[ServerEventType.ROOM_LEFT] = ServerEventType.ROOM_LEFT
    room_id: str
    username: str

class OutMessageEvent(BaseModel):
    event_type: Literal[ServerEventType.MESSAGE] = ServerEventType.MESSAGE
    room_id: str
    username: str
    message: str


class ErrorEvent(BaseModel):
    event_type: Literal[ServerEventType.ERROR] = ServerEventType.ERROR
    message: str






