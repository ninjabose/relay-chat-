from pydantic import BaseModel,Field,model_validator,field_validator
from enum import Enum
import re



#CLIENT -> SERVER


class ClientEventType(str,Enum):
    CREATE_ROOM='create_room'
    JOIN_ROOM='join_room'
    LEAVE_ROOM='leave_room'
    MESSAGE='message'


class InClientCommEvent(BaseModel):
    event_type:ClientEventType
    group_id:str|None=None
    message:str|None=None

    @model_validator(mode='after')
    def validate_events(self):
        if self.event_type in {
            ClientEventType.JOIN_ROOM,ClientEventType.LEAVE_ROOM,ClientEventType.MESSAGE
        }:
            if not self.group_id or not self.group_id.strip():
                raise ValueError('GroupId Invalid')

        #check message
        if self.event_type == ClientEventType.MESSAGE:
            if not self.message or not self.message.strip():
                raise ValueError('message can not be empty')
        return self

class InClientIdentifyEvent(BaseModel):
    username:str=Field(min_length=5,max_length=25)

    @field_validator('username',mode='after')
    @classmethod
    def validate_username(cls,value:str):

        if value!=value.strip():
            raise ValueError('Username can not be empty')

        if not re.fullmatch(r"[A-Za-z0-9]+(?:_[A-Za-z0-9]+)*", value):
            raise ValueError("Username contains invalid characters")

        return value