from enum import Enum, unique


@unique
class ResponseCode(Enum):
    SUCCESS = 200
    ERROR = 500
    ALTH = 5001


@unique
class ResponseMsg(Enum):
    SUCCESS = 'SUCCESS'
    ERROR = 'ERROR'
    ALTH = 'Authentication failed'
