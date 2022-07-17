from pytube import YouTube

import os
import gc

class youtubeapi:

    def get_video_streams(self, link):
        
        try:
            yt = YouTube(link)
        except:
            return "Error", "Error"

        resolution_list = []
        stream_list = []

        for stream in yt.streams.filter(type='video', file_extension='mp4', progressive='True'):

            temp = f'{stream.resolution} - {stream.fps}fps'

            resolution_list.append(temp)
            stream_list.append(stream)

            del stream
            del temp
            gc.collect()
        
        del yt
        del link
        gc.collect()

        return resolution_list, stream_list

    def get_audio_streams(self, link):

        try:
            yt = YouTube(link)
        except:
            return "Error", "Error"

        audio_quality = []
        stream_list = []

        for stream in yt.streams.filter(type='audio', file_extension='mp4'):
            audio_quality.append(stream.abr)
            stream_list.append(stream)

            del stream
            gc.collect()

        del yt
        del link
        gc.collect()
        
        return audio_quality, stream_list

    def download_video(self, stream_list, index):

        index = int(index)

        des = "res/ytvideo/"

        print("Dowloading...")

        out_file = stream_list[index].download(output_path=des)
        file_name = os.listdir(des)[0]
        new_file = new_file = des + file_name

        # try:
        #     os.rename(out_file, new_file)
        # except:
        #     print("Can't rename")

        print(file_name + " has been successfully downloaded.")

        del index
        del des
        del file_name
        del out_file
        del stream_list
        del index
        gc.collect()

        return new_file

    def download_audio(self, stream_list, index):

        index = int(index)
        
        des = 'res/ytaudio/'

        print("Downloading...")

        out_file = stream_list[index].download(output_path=des)
        file_name = os.listdir(des)[0][:-4]
        new_file = des + file_name + '.mp3'
        try:
            os.rename(out_file, new_file)
        except:
            pass

        # result of success
        print(file_name + " has been successfully downloaded.")

        try:
            os.remove(out_file)
        except:
            pass

        del index
        del stream_list
        del des
        del out_file
        del file_name
        gc.collect()

        return new_file

    def get_video_size(self, stream_list, index):
        file_size = stream_list[int(index)].filesize

        del stream_list
        del index
        gc.collect()

        return file_size


    def convert_bytes(self, bytes_number):
        tags = [ "B", "KB", "MB", "GB", "TB" ]
    
        i = 0
        double_bytes = bytes_number
    
        while (i < len(tags) and  bytes_number >= 1024):
            double_bytes = bytes_number / 1024.0
            i = i + 1
            bytes_number = bytes_number / 1024

        del i
        del bytes_number
        del tags
        gc.collect()
    
        return str(round(double_bytes, 2)) + " " + tags[i]
