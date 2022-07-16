from config import sp
from pytube import YouTube
from pytube import Search

# from selenium import webdriver
# from selenium.webdriver import EdgeOptions
# from selenium.webdriver.common.by import By

from sys import platform
from moviepy.editor import *

import os
import re
import re
import gc
import eyed3

class spotifyapi:

    def get_playlist_tracks(playlist_link):
        playlist_URI = playlist_link.split('/')[-1].split('?')[0]
        total_tracks = sp.playlist_tracks(playlist_URI)['total']

        off_set = 0
        tracks_name = []
        tracks_id = []

        while off_set <= total_tracks:
            for track in sp.playlist_tracks(playlist_URI, limit=100, offset=off_set)['items']:

                track_id = track['track']['id']
                track_name = track['track']['name']
                artist_name = track['track']['artists'][0]['name']

                tracks_name.append(f'{track_name} - {artist_name}')
                tracks_id.append(track_id)

            off_set += 100

        del off_set
        del playlist_URI
        del playlist_link
        gc.collect()
        
        return tracks_name, tracks_id, total_tracks

    def get_album_tracks(album_link):
        
        album_URI = album_link.split('/')[-1].split('?')[0]
        total_tracks = sp.album_tracks(album_URI)['total']

        tracks_name = []
        tracks_id = []

        for track in sp.album_tracks(album_URI)['items']:

            track_id = track['id']
            track_name = track['name']
            artist_name = track['artists'][0]['name']

            tracks_name.append(f'{track_name} - {artist_name}')
            tracks_id.append(track_id)

            del track
            gc.collect()

        del album_link
        del album_URI
        gc.collect()

        return tracks_name, tracks_id, total_tracks


    def get_track(track_link):
        track_URI = track_link.split('/')[-1].split('?')[0]
        track_info = sp.track(track_id=track_URI)
        track_name = track_info['name']
        album_name = track_info['album']['name']
        track_date = track_info['album']['release_date']
        track_image = track_info['album']['images'][0]['url']
        track_artist = ""

        for i in track_info['album']['artists']:
            track_artist = track_artist + i['name'] + ', '

            del i
            gc.collect()
        
        track_artist = track_artist[:-2]

        del track_URI
        del track_info
        gc.collect()

        return track_name, track_artist, track_date, track_image, album_name


# def config_selenium():
    # For Server that supports selenium

    # if platform == "linux" or platform == "linux2":
    #     edge_driver_path = f"msedgewebdriver/msedgedriver"
    # else:
    #     edge_driver_path = f"edgedriver_win64\\msedgedriver.exe"
    # options = EdgeOptions()
    # options.add_argument('--log-level=3')
    # options.add_argument('--headless')
    # options.add_argument("--user-agent=Mozilla...")
    # driver = webdriver.Edge(edge_driver_path, options=options)
    # driver.implicitly_wait(0.5)

    # For Heroku

    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--no-sandbox")

    # driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

    # return driver


# Downloading Music from youtube

class spotiYT:

    def get_videoid(track_name):
        # request = yt_service.search().list(part='snippet', q=track_name)
        # video_id = request.execute()['items'][0]['id']['videoId']
        # # yt_track_name = request.execute()['items'][0]['snippet']['title']

        try:
            # Getting Video ID from Selenium 

            # url = f"https://www.youtube.com/results?search_query={track_name}"
            # driver = config_selenium()
            # driver.get(url)
            # print(track_name)
            # print("Waiting for 2 seconds...")
            # sleep(2)
            # video_url = driver.find_element(By.XPATH, "//a[@id='video-title']").get_attribute('href')
            # video_id = video_url.split('=')[-1]

            # Getting Video ID from PyTube
            
            s = Search(track_name)
            results = s.results
            video_id = results[0].video_id

            del s
            del results
            gc.collect()

            return video_id
        except:
            return "No Download"

    def download_audio(video_id, track_name):

        try:
            track_name = re.sub(r":", "_",track_name)
            track_name = re.sub(r"/", "_",track_name)
            track_name = re.sub("\"", "_", track_name)

            des = os.path.join("res","spotitrack")
            source = os.path.join("res", "spotitrack", f"{track_name}.mp3")
            url = f'https://www.youtube.com/watch?v={video_id}'
            try:
                yt = YouTube(url)
            except:
                print("Connection Error")

            stream = yt.streams.filter(type="video", progressive=True, res="360p")[0]
            mp4_file = stream.download(output_path=des)
            if platform == "linux" or platform == "linux2":
                yt_file_name = mp4_file.split('/')[-1]
            else:
                yt_file_name = mp4_file.split('\\')[-1]

            try:
                video = VideoFileClip(os.path.join(des, yt_file_name))
                video.audio.write_audiofile(source)
                video.close()
            except Exception as e:
                print(e)

            try:
                print(f"Removing: {os.path.join(des, yt_file_name)}")
                os.remove(mp4_file)
            except Exception as e:
                print(e)

            # try:
                
            # except Exception as e:
            #     print(e)
            # base, ext = os.path.splitext(out_file)
            # new_file = des + track_name + '.mp3'
            # try:
            #     os.rename(out_file, new_file)
            # except:
            #     pass

            # # result of success
            # print(track_name + " has been successfully downloaded.")

            del track_name
            del des
            del source
            del url
            del yt
            del stream
            del mp4_file
            del yt_file_name
            del video
            gc.collect()

            return source
        
        except:
            return "Error"

    def setting_metadata(file_path, track_name):
        audiofile = eyed3.load(file_path)
        audiofile.tag.title = track_name.split("-")[0]
        audiofile.tag.artist = track_name.split("-")[-1]
        audiofile.tag.save()

        del audiofile
        del file_path
        del track_name
        gc.collect()
