# SpotiBot

## Introduction

SpotiBot is a python based bot which is made on Pyrogram module for Telegram. It is used to download songs from your Spotify/Youtube playlist directly to your local machine.

### Commands

#### /spoti
/spoti takes a link of playlist, track, album, that a user wants to download.

```
/spoti https://open.spotify.com/playlist/7DpdRmaNmqevW1yoxdG5Uz?si=e5a9e043016440e1
```

#### /yt
/yt takes a link of video, that a user wants to download as mp4 or mp3.

```
/yt https://www.youtube.com/watch?v=-BCMqMJx4CE&list=RD-BCMqMJx4CE&start_radio=1
```
## Env Variables

### Spotify Client 

`CLIENT-ID` - Can be fetch from Spotify Developer: https://developer.spotify.com/

`CLIENT - SECRET` - Can be fetch from Spotify Developer https://developer.spotify.com/

### Telegram Config

`API_ID` - Get the value from [my.telegram.org](https://my.telegram.org/apps) here.

`API_HASH` - Get the value from [my.telegram.org](https://my.telegram.org/apps) here.

`BOT_TOKEN` - Make a bot from [@BotFather](https://t.me/BotFather) and enter token here.

`GSPREAD_JSON` - A link of google sheets API JSON file hosted in the cloud, configure it in https://console.cloud.google.com. For more help [watch this video.](https://www.youtube.com/watch?v=bu5wXjz2KvU)
