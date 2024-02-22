from aiogram import Router

from .authors import authors_router
from .genre import genre_router
from .parallels import parallel_router
from .klasses import klasses_router
from .students import student_router

staff_references_router = Router()

staff_references_router.include_routers(*[
    authors_router, genre_router, parallel_router, klasses_router, student_router
])
