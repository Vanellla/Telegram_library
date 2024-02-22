from aiogram import Router

from .staff import staff_router

handlers_router = Router()

handlers_router.include_routers(
    staff_router
)
