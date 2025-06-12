from functools import wraps
from aiogram.types import Message

state = "user"

def admin(func):
    @wraps(func)
    async def wrapper(message: Message, *args, **kwargs):
        print("admin")
        if state == "admin":
            return await func(message, *args, **kwargs)
    return wrapper

def user(func):
    @wraps(func)
    async def wrapper(message: Message, *args, **kwargs):
        print("user")
        if state == "user":
            return await func(message, *args, **kwargs)
    return wrapper