from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("today"))
async def cmd_today(message: Message):
    await message.answer(
        "Пока здесь ничего нет. Воспользуйтесь /all, чтобы посмотреть все мероприятия."
    )
