from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove
from supabase import Client, create_client

from config_reader import config

router = Router()
supabase: Client = create_client(config.supabase_url, config.supabase_key)

admin_ids = [7202518092, 5754845226]


class AddEvent(StatesGroup):
    name = State()
    link = State()
    geo_name = State()
    geo_link = State()
    day_of_week = State()
    time = State()
    description = State()

# Admin command to start adding new event


@router.message(Command("admin"))
async def cmd_admin(message: Message):
    if message.from_user.id not in admin_ids:
        await message.answer("You are not authorized to use this command.")
        return
    await message.answer(
        "Admin commands:\n"
        "/add_new - Add new event\n"
        "/cancel - Cancel current operation",
        reply_markup=ReplyKeyboardRemove()
    )

# Start adding new event


@router.message(Command("add_new"))
async def cmd_add_new(message: Message, state: FSMContext):
    if message.from_user.id not in admin_ids:
        await message.answer("You are not authorized to use this command.")
        return

    await state.set_state(AddEvent.name)
    await message.answer(
        "Let's add a new English event!\n\n"
        "Send me the event name:",
        reply_markup=ReplyKeyboardRemove()
    )

# Event name


@router.message(AddEvent.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddEvent.link)
    await message.answer("Great! Now send me the event link:")

# Event link


@router.message(AddEvent.link)
async def process_link(message: Message, state: FSMContext):
    await state.update_data(link=message.text)
    await state.set_state(AddEvent.geo_name)
    await message.answer("Now send me the venue name:")

# Venue name


@router.message(AddEvent.geo_name)
async def process_geo_name(message: Message, state: FSMContext):
    await state.update_data(geo_name=message.text)
    await state.set_state(AddEvent.geo_link)
    await message.answer("Now send me the Yandex Maps link to the venue:")

# Venue link


@router.message(AddEvent.geo_link)
async def process_geo_link(message: Message, state: FSMContext):
    await state.update_data(geo_link=message.text)
    await state.set_state(AddEvent.day_of_week)
    await message.answer("What day of the week? (e.g., Monday, Tuesday, etc.):")

# Day of week


@router.message(AddEvent.day_of_week)
async def process_day(message: Message, state: FSMContext):
    await state.update_data(day_of_week=message.text)
    await state.set_state(AddEvent.time)
    await message.answer("What time? (e.g., 19:30):")

# Time


@router.message(AddEvent.time)
async def process_time(message: Message, state: FSMContext):
    await state.update_data(time=message.text)
    await state.set_state(AddEvent.description)
    await message.answer("Finally, send me the event description:")

# Description and save to database


@router.message(AddEvent.description)
async def process_description(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()

    # Insert into Supabase
    response = supabase.table("english_events").insert({
        "name": data["name"],
        "link": data["link"],
        "geo_name": data["geo_name"],
        "geo_link": data["geo_link"],
        "day_of_week": data["day_of_week"],
        "time": data["time"],
        "description": message.text
    }).execute()

    await message.answer(
        "✅ Event added successfully!\n\n"
        f"<b>{data['name']}</b>\n"
        f"<b>When:</b> {data['day_of_week']} at {data['time']}\n"
        f"<b>Where:</b> {data['geo_name']}\n"
        f"<b>Link:</b> {data['link']}\n\n"
        f"<b>Description:</b>\n{message.text}",
        parse_mode="HTML"
    )
