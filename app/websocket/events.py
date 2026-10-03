from pydantic import BaseModel,Field,model_validator,field_validator
from enum import Enum
import re



class Event(str,Enum):
    CREATE_ROOM='create_room'
    JOIN_ROOM='join_room'
    LEAVE_ROOM='leave_room'
    MESSAGE='message'
    DISCONNECT='disconnect'


    

class ClientEvents(BaseModel):
    event_type:Event
    group_id:str|None=None
    message:str|None=None

    @model_validator(mode='after')
    def validate_events(self):
        if self.event_type in {
            Event.JOIN_ROOM,Event.LEAVE_ROOM,Event.MESSAGE
        }:
            if not self.group_id or not self.group_id.strip():
                raise ValueError('GroupId Invalid')


        #check message
        if self.event_type == Event.MESSAGE:
            if not self.message.strip():
                raise ValueError('message can not be empty')
        return self

class IdentifyEvent(BaseModel):
    username:str=Field(min_length=5,max_length=25)

    @field_validator('username',mode='after')
    @classmethod
    def validate_username(cls,value:str):

        if value!=value.strip():
            raise ValueError('Username can not be empty')

        if not re.fullmatch(r"[A-Za-z0-9]+(?:_[A-Za-z0-9]+)*", value):
            raise ValueError("Username contains invalid characters")

        return value
    

        
        
            

        