from enum import Enum


class SellType(Enum):
    offline = 'offline'
    online = 'online'
    all = 'all'

    @classmethod
    def choices(cls):
        return ((i.name, i.value) for i in cls)


class OrderStatus(Enum):
    wait_pay = 'wait_pay'
    cancelled = 'cancelled'
    paid = 'paid'

    @classmethod
    def choices(cls):
        return ((i.name, i.value) for i in cls)
