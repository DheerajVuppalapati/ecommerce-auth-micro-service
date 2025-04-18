from enum import Enum

class UserStatusEnum(str,Enum):
    active = 'active'
    inactive = 'inactive'
    banned = 'banned'