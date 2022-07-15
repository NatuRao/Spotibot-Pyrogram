from config import bot
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from API.googlesheetsapi import googlesheetsapi as gsapi
from Pagination.pagination import pagination as pagi
from API.youtubeapi import youtubeapi as ytapi

import os

pagi_obj = pagi()
ytapi_obj = ytapi()

class youtube:

    @bot.on_message(filters=filters.command(['yt']))
    async def event_handler_youtube(client: Client, message: Message):

        if '/yt' == message.text:
            await bot.send_message(
                chat_id=message.chat.id,
                text="𝖢𝗈𝗆𝗆𝖺𝗇𝖽 𝗆𝗎𝗌𝗍 𝖻𝖾 𝗎𝗌𝖾𝖽 𝗅𝗂𝗄𝖾 𝗍𝗁𝗂𝗌\nyt <Youtube video link>\nexample: `/yt https://www.youtube.com/watch?v=GPbG4mIgKAw`"
            )

        elif '<' in message.text or '>' in message.text:
            await bot.send_message(
                chat_id=message.chat.id,
                text="Link shouldn't contain angle brackets '<' '>'... Try again"
            )

        elif '/yt' in message.text:

            first_name = message.chat.first_name
            link = message.text.split()
            link.pop(0)
            link = "".join(link)

            pagi_obj.link = link

            gsapi.add_data(first_name, link)

            button = []
            button.append([InlineKeyboardButton('Video Stream', "video:")])
            button.append([InlineKeyboardButton('Audio Stream', "audio:")])

            button = InlineKeyboardMarkup(button)

            await bot.send_message(
                chat_id=message.chat.id,
                text="Select Streams:",
                reply_markup=button
            )

    @bot.on_callback_query(filters=filters.regex(r"^video:"))
    async def callback_handler_video(client: Client, callback: CallbackQuery):
        
        resolution_list, stream_list = ytapi_obj.get_video_streams(pagi_obj.link)

        pagi_obj.resolution_list = resolution_list
        pagi_obj.stream_list = stream_list

        resolution_button = []
        count = 0

        for i in resolution_list:
            resolution_button.append([InlineKeyboardButton(i, f"dlvid:{count}")])
            count += 1

        resolution_button.reverse()

        resolution_button.append([InlineKeyboardButton('Back', 'back:')])

        resolution_button = InlineKeyboardMarkup(resolution_button)

        await callback.message.edit(
            text="Select Video Resolution: ",
            reply_markup=resolution_button
        )

    @bot.on_callback_query(filters=filters.regex(r"^audio:"))
    async def callback_handler_audio(client: Client, callback: CallbackQuery):
        audio_quality, stream_list = ytapi_obj.get_audio_streams(pagi_obj.link)

        pagi_obj.audio_quality = audio_quality
        pagi_obj.stream_list = stream_list

        audio_quality_button = []
        count = 0

        for i in audio_quality:
            audio_quality_button.append([InlineKeyboardButton(i, f"dlaudio:{count}")])
            count += 1

        audio_quality_button.reverse()

        audio_quality_button.append([InlineKeyboardButton('Back', 'back:')])

        audio_quality_button = InlineKeyboardMarkup(audio_quality_button)

        await callback.message.edit(
            "Select Audio Quality",
            reply_markup=audio_quality_button
        )

    @bot.on_callback_query(filters=filters.regex(r"^dlvid:"))
    async def callback_download_video(client: Client, callback: CallbackQuery):
        index = callback.data
        index = index.split(':')
        index.pop(0)
        index = ''.join(index)
        
        file_size = ytapi_obj.get_video_size(pagi_obj.stream_list, index)
        
        # if file_size < 500000000:
        file_size = ytapi_obj.convert_bytes(file_size)
        file_path = ytapi_obj.download_video(pagi_obj.stream_list, index)
        file_name = file_path.split('/')[-1]

        print("Sending...")

        await bot.send_message(
            chat_id=callback.from_user.id,
            text=f"Downloading {file_name}, File Size: **{file_size}**\n\nMight take a while depends on the file size."
        )

        try:
            await bot.send_audio(
                chat_id=callback.from_user.id,
                audio=file_path
            )

            os.remove(file_path)

        except Exception as e:
            print(e)
            await bot.send_message(
                chat_id=callback.from_user.id,
                text="Something went wrong, the video can't download..."
            )

        # else:
        #     await bot.send_message(
        #         chat_id=callback.from_user.id,
        #         text=
        #     )

    @bot.on_callback_query(filters=filters.regex(r"^dlaudio:"))
    async def callback_handler_download(client: Client, callback: CallbackQuery):
        index = callback.data
        index = index.split(":")
        index.pop(0)
        index = "".join(index)

        file_path = ytapi_obj.download_audio(pagi_obj.stream_list, index)
        file_name = file_path.split('/')[-1]

        print("Sending...")

        await bot.send_message(
            chat_id=callback.from_user.id,
            text=f"Downloading __**{file_name}**__\n\nMight take a while depends on file size..."
        )

        try:
            await bot.send_audio(
                chat_id=callback.from_user.id,
                audio=file_path
            )

            os.remove(file_path)

        except:
            await bot.send_message(
                chat_id=callback.from_user.id,
                text="Something went wrong, the video can't download..."
            )

    @bot.on_callback_query(filters=filters.regex(r"^back:"))
    async def callback_for_back(client: Client, callback: CallbackQuery):
        button = []
        button.append([InlineKeyboardButton('Video Stream', "video:")])
        button.append([InlineKeyboardButton('Audio Stream', "audio:")])

        button = InlineKeyboardMarkup(button)

        await callback.message.edit(
            text="Select Streams:",
            reply_markup=button
        )
