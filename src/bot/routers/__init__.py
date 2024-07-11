__all__ = ("router",)

from aiogram import Router

from .commands import router as commands_router
from .survey_currency import router as survey_router

router = Router(name=__name__)

router.include_routers(
    commands_router,
    survey_router,
)
