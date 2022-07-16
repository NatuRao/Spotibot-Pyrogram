import enum
from config import bot
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from Helper.helper import start_text, help_text

class starter:

    # When the user type /start command
    @bot.on_message(filters=filters.command(['start']))
    async def start_command(client: Client, message: Message):
        first_name = message.chat.first_name
        await bot.send_photo(
            chat_id=message.chat.id,
            caption=f"Hi **__{first_name}__**, {start_text}",
            parse_mode=enums.ParseMode.MARKDOWN,
            photo="https://telegra.ph/file/618567217c6733a205f95.jpg"
        )

    @bot.on_message(filters=filters.command(['help']))
    async def help_command(client: Client, message: Message):
        await bot.send_message(
            chat_id=message.chat.id,
            parse_mode=enums.ParseMode.MARKDOWN,
            text=help_text
        )