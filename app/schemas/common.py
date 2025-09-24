from enum import Enum

class RoleEnum(str, Enum):
    admin="admin"
    author="author"
    client="client"

class PostStatus(str, Enum):
    draft ="draft"
    published="published"
    archived ="archived"

    