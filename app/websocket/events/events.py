from pydantic import BaseModel,Field,model_validator,field_validator
from enum import Enum
import re


class JoinResult(str,Enum):
    SUCCESS='success'
    ROOM_NOT_FOUND='room_not_found'
    ALREADY_JOINED='already_joined'


class LeaveResult(str,Enum):
    SUCCESS='success'
    ROOM_NOT_FOUND='room_not_found'
    NOT_A_MEMBER='not_a_member'
