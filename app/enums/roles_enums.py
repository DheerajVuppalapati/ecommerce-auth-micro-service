from enum import Enum

class RoleEnum(str, Enum):
    super_admin = 'super_admin'
    admin = 'admin'
    user = 'user'