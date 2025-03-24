from datetime import datetime

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from supabase import Client, create_client

from config_reader import config

router = Router()
supabase: Client = create_client(config.supabase_url, config.supabase_key)

DAYS_ORDER = ['Monday', 'Tuesday', 'Wednesday',
              'Thursday', 'Friday', 'Saturday', 'Sunday']


@router.message(Command("all"))
async def cmd_all(message: Message):
    try:
        # Fetch all events from Supabase
        response = supabase.table("english_events").select("*").execute()
        events = response.data

        if not events:
            await message.answer("No events found.")
            return

        # Group events by day
        events_by_day = {}
        for event in events:
            day = event['day_of_week']
            if day not in events_by_day:
                events_by_day[day] = []
            events_by_day[day].append(event)

        # Sort days according to DAYS_ORDER
        sorted_days = sorted(
            events_by_day.keys(),
            key=lambda x: DAYS_ORDER.index(
                x) if x in DAYS_ORDER else len(DAYS_ORDER)
        )

        # Build the message
        message_text = ""
        for day in sorted_days:
            message_text += f"\n<b>{day}</b>\n" + "\n"
            for event in sorted(events_by_day[day], key=lambda x: x['time']):
                price = f" | {event['price']}" if event.get('price') else ""
                message_text += (
                    f"• {event['time']} | "
                    f"<a href='{event['link']}'>{event['name']}</a> | "
                    f"<a href='{event['geo_link']}'>{event['geo_name']}</a>"
                    f"{price}\n"
                )

        await message.answer(
            text=message_text,
            parse_mode="HTML",
            disable_web_page_preview=True
        )

    except Exception as e:
        await message.answer(f"An error occurred: {str(e)}")
        print(f"Error in cmd_all: {str(e)}")
