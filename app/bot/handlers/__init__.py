from aiogram import Router
from . import admin, general


def get_routers() -> list[Router]:
    return [admin.router, general.router]
