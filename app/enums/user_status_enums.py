from enum import Enum

class UserStatusEnum(str,Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    BANNED = 'banned'