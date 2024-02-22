from aiogram import Router

from .main_menu import staff_main_router
from .books_functions import staff_main_references_router
from .references import staff_references_router
from .books import books_main_router
# from .book_instance import books_instance_router

staff_router = Router()

staff_router.include_routers(*[
    staff_main_router, staff_main_references_router, staff_references_router, books_main_router
])
