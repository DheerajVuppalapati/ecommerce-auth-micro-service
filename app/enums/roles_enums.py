from enum import Enum

class RoleEnum(str, Enum):
    SUPER_ADMIN = 'super_admin'
    ADMIN = 'admin'
    USER = 'user'