from typing import Optional

from aiogram import F, Router, html
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
    Message,
)
from aiogram.types.inline_keyboard_button import InlineKeyboardButton

router = Router()


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(
        text="Получите список всех ивентов на неделю по команде /all\n\n"
        "Список ивентов на сегодня /today\n\n"
        # "Список ивентов на завтра /tomorrow"
        # "Только разговорные клубы /clubs"
        # "Встречи в барах /bars"
        # "Концерты и стэндапы /standup"
        "Только бесплатные /free\n\n"
        # "Платные ивенты (фильтр по цене) /paid"
        # "Напоминалка о событии /remind"
    )
