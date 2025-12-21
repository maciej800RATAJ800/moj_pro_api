from enum import Enum

class SortBy(str, Enum):
    id = "id"
    name = "name"
    age = "age"

class SortDir(str, Enum):
    ASC = "ASC"
    DESC = "DESC"
