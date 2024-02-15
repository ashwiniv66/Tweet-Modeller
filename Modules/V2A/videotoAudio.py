import logging
import os.path
import os
from moviepy.editor import *
from os import *

import get_handlers as GetHandlers


def convert_to_audio(selectedTopic):

    twitter_handlers = GetHandlers.GetHandlers().get_twitter_handlers(selectedTopic)

    for tweeter_handle in twitter_handlers:

        path_to_converted_text = os.path.join("Data\\Audios_converted", tweeter_handle)
        try:
            os.makedirs(path_to_converted_text, exist_ok=False)
        except Exception:
            logging.error("Twitter handler already extracted")
            continue

        print("________FETCHING VIDEO RESOURCES___________")
        videoList = list(listdir(f".\\Data\\Fetched\\{tweeter_handle}\\videos"))
        if len(videoList) == 0:
            continue
        for video in videoList:
            os.rename(
                f".\\Data\\Fetched\\{tweeter_handle}\\videos\\{video}",
                f".\\Data\\Fetched\\{tweeter_handle}\\videos\\{video}.mp4",
            )
        videoList = list(listdir(f".\\Data\\Fetched\\{tweeter_handle}\\videos"))
        print(videoList)
        print("________FINISHED FETCHING VIDEO RESOURCES___________")

        print("________CONVERTING VIDEO RESOURCES___________")
        for videoName in videoList:
            print(f"_____________CONVERTING {videoName} RESOURCES___________")
            video = VideoFileClip(
                os.path.join(f".\\Data\\Fetched\\{tweeter_handle}\\videos\\{videoName}")
            )
            try:    
                video.audio.write_audiofile(
                    f".\\Data\\Audios_converted\\{tweeter_handle}\\{videoName[:-4]}.wav",
                    fps=16000,
                    codec="pcm_s16le",
                )
            except:
                print("AUDIO DOESNT EXISIT")
            finally:
                print(f"__________FINISHED CONVERTING {videoName} RESOURCES___________")
            print("__________FINISHED VIDEO RESOURCES___________")
