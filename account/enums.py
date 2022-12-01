from enum import Enum


class UserRoles(Enum):
    director = 'director'
    vendor = 'vendor'
    manager = 'manager'
    client = 'client'

    @classmethod
    def choices(cls):
        return ((i.name, i.value) for i in cls)

