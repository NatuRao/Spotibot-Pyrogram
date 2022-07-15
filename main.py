from config import bot
from utils.spotify import spotify
from utils.starter import starter
from utils.youtube import youtube

try:
    print("Loading Spotify")
    spotify()
    starter()
    youtube()
except Exception as e:
    print(e)

bot.run()