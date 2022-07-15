from pyrogram import Client
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

import os
import spotipy

load_dotenv()

# Setting up Spotify Client
# CLIENT_ID = os.getenv('CLIENT_ID')
# CLIENT_SECRET = os.getenv('CLIENT_SECRET')
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


# Setting up Telethon Client
# API_ID = os.getenv('API_ID')
# API_HASH = os.getenv('API_HASH')
# BOT_TOKEN = os.getenv('BOT_TOKEN')
API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)