from config import bot
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery

from API.googlesheetsapi import googlesheetsapi as gsapi
from API.spotifyapi import spotifyapi as spapi
from API.spotifyapi import spotiYT as spytapi
from Pagination.pagination import pagination as pagi

from itertools import islice

import requests
import os
import uuid
import gc

pagi_obj = pagi()

class spotify:

    # When user type /spoti
    @bot.on_message(filters=filters.command(["spoti"]))
    async def event_handler_spotify(client: Client, message: Message):
        print("Entered /spoti")
        if message.text == "/spoti":
            await bot.send_message(
                chat_id=message.chat.id,
                text="𝖢𝗈𝗆𝗆𝖺𝗇𝖽 𝗆𝗎𝗌𝗍 𝖻𝖾 𝗎𝗌𝖾𝖽 𝗅𝗂𝗄𝖾 𝗍𝗁𝗂𝗌\n/spoti <Spotify playlist link>\nexample: `/spoti https://open.spotify.com/playlist/7DpdRmaNmqevW1yoxdG5Uz?si=9CU2umnnSVCg4fQm-UNJHg`"
            )
        
        elif '>' in message.text or '<' in message.text:
            await bot.send_message(
                chat_id=message.chat.id,
                text="Link shouldn't contain angle brackets '<' '>'... Try again"
            )

        elif '/spoti' in message.text:

            first_name = message.chat.first_name
            username = message.chat.username
            link = message.text.split()
            link.pop(0)
            link = "".join(link)

            gsapi.add_data(first_name, username, link)

            # Getting Track Info

            if link.split('/')[-2].lower() == "playlist":
                try:
                    tracks_name, tracks_id, total_tracks = spapi.get_playlist_tracks(link)
                    choice = "P/A"
                except:
                    await bot.send_message(
                        chat_id=message.chat.id,
                        text="Something went wrong! Check your playlist/album/track link and try again."
                    )
            
            elif link.split('/')[-2].lower() == "album":
                try:
                    tracks_name, tracks_id, total_tracks = spapi.get_album_tracks(link)
                    choice = "P/A"
                except:
                    await bot.send_message(
                        chat_id=message.chat.id,
                        text="Something went wrong! Check your playlist/album/track link and try again."
                    )

            elif link.split('/')[-2].lower() == "track":
                try:
                    track_name, track_artist, track_date, track_image, album_name = spapi.get_track(link)
                    image = requests.get(track_image).content

                    # Saving the image file
                    image_name = str(uuid.uuid4())
                    try:    
                        os.makedirs(os.path.join("res", "image"))
                    except:
                        pass
                    image_path = os.path.join("res", "image", f"{image_name}.png")
                    with open(image_path, "wb") as file:
                        file.write(image)

                    track_name = f"{track_name} - {track_artist}"
                    pagi_obj.tracks_name_id_list = []
                    pagi_obj.tracks_name_id_list.append(track_name)

                    choice = "T"

                    await bot.send_photo(
                        chat_id=message.chat.id,
                        caption=f"**Name:** `{track_name}`\n**Artist:** `{track_artist}`\n**Album:** `{album_name}`\n**Release Date:** `{track_date}`\n\nDownloading...",
                        photo=image_path
                    )
                    os.remove(image_path)
                
                except Exception as e:
                    print(e)
                    await bot.send_message(
                        chat_id=message.chat.id,
                        text="Something went wrong! Check the playlist/album/track link and try again.",
                    )
            
            # Downloading Process

            if choice == "P/A":
                pagi_obj.total_tracks = total_tracks
                tracks_name_id = []
                ch_perrow = pagi_obj.perrow
                count = 0
                if len(tracks_name) == len(tracks_id):
                    while count <= len(tracks_id):
                        temp = {}
                        for i in islice(range(len(tracks_name)), count, count + ch_perrow):
                            temp[tracks_id[i]] = tracks_name[i]
                        tracks_name_id.append(temp)
                        count += ch_perrow

                        pagi_obj.tracks_name_id = tracks_name_id

                    button = pagi_obj.show_buttons()

                    await bot.send_message(
                        chat_id=message.chat.id,
                        text=f'**Select the track(s) you want to download**\n__Arrow Buttons will not function while the tracks are downloading.__\n\n**Total Track Found: __{pagi_obj.total_tracks}__**',
                        reply_markup=button
                    )

                    del button
                    del link
                    del first_name
                    del tracks_name
                    del tracks_id
                    del tracks_name_id
                    del total_tracks
                    del ch_perrow
                    gc.collect()
            
            elif choice == "T":
                video_id = spytapi.get_videoid(pagi_obj.tracks_name_id_list[0])
                if video_id == "No Download":
                    await bot.send_message(
                        chat_id=message.chat.id,
                        text=f"Can't Download the track..."
                    )
                
                elif video_id != "No Download":
                    file_path = spytapi.download_audio(video_id, pagi_obj.tracks_name_id_list[0])
                    spytapi.setting_metadata(file_path, pagi_obj.tracks_name_id_list[0])

                    if file_path == "Error":
                        await bot.send_message(
                            chat_id=message.chat.id,
                            text="Something went wrong while downloading the audio"
                        )

                    elif file_path != "Error":
                        print("Sending...")
                        await bot.send_audio(
                            chat_id=message.chat.id,
                            audio=file_path
                        )

                del file_path
                del video_id
                gc.collect()
            
            else:
                print("Length not Matching...")

    @bot.on_callback_query(filters=filters.regex(r"^trckdl:"))
    async def callback_for_download_track(client: Client, callback: CallbackQuery):

        text = callback.data
        track_id = text.split(':')[-1]
        video_id = spytapi.get_videoid(pagi_obj.tracks_name_id[pagi_obj.current_page - 1][track_id])

        if video_id == "No Download":
            await bot.send_message(
                chat_id=callback.from_user.id,
                text="Can't Download the track..."
            )

        elif video_id != "No Download":
            file_path = spytapi.download_audio(video_id, pagi_obj.tracks_name_id[pagi_obj.current_page - 1][track_id])
            print(f"File Path: {file_path}")
            spytapi.setting_metadata(file_path, pagi_obj.tracks_name_id[pagi_obj.current_page - 1][track_id])

            if file_path == "Error":
                await bot.send_message(
                    chat_id=callback.from_user.id,
                    text="Something went wrong while downloading the audio"
                )

            elif file_path != "Error":
                print("Sending...")

                await bot.send_audio(
                    chat_id=callback.from_user.id,
                    audio=file_path
                )

                os.remove(file_path)

        del text
        del track_id
        del video_id
        del file_path
        gc.collect()

    @bot.on_callback_query(filters=filters.regex(r"^spdlpg:"))
    async def callback_for_download_page(client: Client, callback: CallbackQuery):

        await bot.send_message(
            chat_id=callback.from_user.id,
            text="The Page is Downloading, Please Wait."
        )

        for id, name in pagi_obj.tracks_name_id[pagi_obj.current_page - 1].items():

            video_id = spytapi.get_videoid(name)

            if video_id == "No Download":
                await bot.send_message(
                chat_id=callback.from_user.id,
                text=f"Can't Download the track... {name}"
            )

            elif video_id != "No Download":
                file_path = spytapi.download_audio(video_id, name)
                spytapi.setting_metadata(file_path, name)

                if file_path == "Error":
                    await bot.send_message(
                        chat_id=callback.from_user.id,
                        text="Something went wrong while downloading the video" 
                    )
                
                elif file_path != "Error":

                    print('Sending...')

                    await bot.send_audio(
                        chat_id=callback.from_user.id,
                        audio=f'{file_path}'
                    )

                    try:
                        os.remove(file_path)
                    except:
                        pass

                del video_id
                del file_path
                gc.collect()

        del id
        del name
        gc.collect()
    
    @bot.on_callback_query(filters=filters.regex(r"^spdlall:"))
    async def callback_for_download_all(client: Client, callback: CallbackQuery):

        print("Download All")

        await callback.message.edit(
            f'Sit back and relax, the tracks are downloading...\n\n__Total Tracks to Download:__ __**{pagi_obj.total_tracks}**__'
        )

        count = 0

        for dic in pagi_obj.tracks_name_id:
            for id, name in dic.items():
                count += 1
                video_id = spytapi.get_videoid(name)

                if video_id == "No Download":
                    await bot.send_message(
                    chat_id=callback.from_user.id,
                    text=f"Can't Download the track... {name}"
                )

                elif video_id != "No Download":

                    file_path = spytapi.download_audio(video_id, name)
                    spytapi.setting_metadata(file_path, name)

                    if file_path == "Error":
                        await bot.send_message(
                            chat_id=callback.from_user.id,
                            text="Something went wrong while downloading the video" 
                        )

                    elif file_path != "Error":

                        print('Sending...')

                        await bot.send_audio(
                            chat_id=callback.from_user.id,
                            audio=file_path
                        )

                        try:
                            os.remove(file_path)
                        except:
                            pass

                del file_path
                del video_id
                gc.collect()
            
            del id
            del name
            gc.collect()

        del dic
        gc.collect()

    @bot.on_callback_query(filters=filters.regex(r"next_"))
    async def callback_for_next(client: Client, callback: CallbackQuery):

        try:
            button = pagi_obj.next_button()
        except:
            await bot.send_message(
            chat_id=callback.from_user.id,
            text="No more pages available."
        )

        await callback.message.edit(
            text=f'**Select the track(s) you want to download**\n__Arrow Buttons will not function while the tracks are downloading.__\n\n**Total Track Found: __{pagi_obj.total_tracks}__**',
            reply_markup=button
        )

        del button
        gc.collect()


    @bot.on_callback_query(filters=filters.regex(r"prev_"))
    async def callback_for_prev(client: Client, callback: CallbackQuery):

        try:
            button = pagi_obj.prev_button()
        except:
            await bot.send_message(
            chat_id=callback.from_user.id,
            text="No more pages available."
        )

        await callback.message.edit(
            text=f'**Select the track(s) you want to download**\n__Arrow Buttons will not function while the tracks are downloading.__\n\n**Total Track Found: __{pagi_obj.total_tracks}__**',
            reply_markup=button
        )

        del button
        gc.collect()

    @bot.on_callback_query(filters=filters.regex(r"first_"))
    async def callback_for_first(client: Client, callback: CallbackQuery):

        try:
            button = pagi_obj.first_button()
        except:
            await bot.send_message(
            chat_id=callback.from_user.id,
            text="No more pages available."
        )

        await callback.message.edit(
            text=f'**Select the track(s) you want to download**\n__Arrow Buttons will not function while the tracks are downloading.__\n\n**Total Track Found: __{pagi_obj.total_tracks}__**',
            reply_markup=button
        )

        del button
        gc.collect()

    @bot.on_callback_query(filters=filters.regex(r"last_"))
    async def callback_for_last(client: Client, callback: CallbackQuery):

        try:
            button = pagi_obj.last_button()
        except:
            await bot.send_message(
            chat_id=callback.from_user.id,
            text="No more pages available."
        )

        await callback.message.edit(
            text=f'**Select the track(s) you want to download**\n__Arrow Buttons will not function while the tracks are downloading.__\n\n**Total Track Found: __{pagi_obj.total_tracks}__**',
            reply_markup=button
        )

        del button
        gc.collect()