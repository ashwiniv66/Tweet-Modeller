"""Transcribe the given audio file."""
from google.cloud import speech
import io
from os import listdir
import os

import get_handlers as GetHandlers


def transcribe_file(topic):
    credential_path = r"C:\Users\calvi\OneDrive\PROJECTS\Final_year_project\project\Modules\A2T\speech-to-textv1-d01f952ee091.json"
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credential_path

    print("____INITIALIZE CLOUD SERVICES_____")
    client = speech.SpeechClient()

    twitter_handlers = GetHandlers.GetHandlers().get_twitter_handlers(topic)

    for tweeter_handle in twitter_handlers:
        path_to_audio = f"./Data/Audios_converted/{tweeter_handle}"
        try:
            os.mkdir(f".\\Data\\Text_translated\\{tweeter_handle}")
        except:
            print(f"folder for {tweeter_handle} already exist")
        finally:
            audio_files = listdir(path_to_audio)
            if len(audio_files) != 0:
                for audio_file in audio_files:
                    print(audio_file, audio_file[:-4])
                    audio = speech.RecognitionAudio(
                        uri=f"gs://audio-files-final-year-project-act/{tweeter_handle}/{audio_file}"
                    )
                    config = speech.RecognitionConfig(
                        language_code="en-US",
                        sample_rate_hertz=16000,
                        audio_channel_count=2,
                    )

                    operation = client.long_running_recognize(
                        config=config, audio=audio
                    )

                    print("Waiting for operation to complete...")
                    response = operation.result(timeout=90)

                    text = ""
                    print("____WRITING CONVERSION TO TEXT_____")
                    for result in response.results:
                        # The first alternative is the most likely one for this portion.
                        text += result.alternatives[0].transcript
                    file_name = audio_file[:-4]
                    with open(
                        f".\\Data\\Text_translated\\{tweeter_handle}\\{file_name}.txt",
                        "w",
                    ) as fhandle:
                        fhandle.write(text)
