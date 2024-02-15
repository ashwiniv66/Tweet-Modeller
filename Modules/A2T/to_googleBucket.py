import os
from os import *
from pprint import pprint
from google.cloud import storage

import get_handlers as GetHandlers

credential_path = r"C:\Users\calvi\OneDrive\PROJECTS\Final_year_project\project\Modules\A2T\speech-to-textv1-d01f952ee091.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

bucket_name = 'audio-files-final-year-project-act'

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )

def upload_all_audios(topic):
    twitter_handlers = GetHandlers.GetHandlers().get_twitter_handlers(topic)
    for tweeter_handle in twitter_handlers:
        path_to_audio = f"./Data/Audios_converted/{tweeter_handle}"
        audio_files = listdir(path_to_audio)
        if(len(audio_files) != 0):
            create_folder(bucket_name,f'{tweeter_handle}/')
            for audio_file in audio_files:
                upload_blob(bucket_name,f"{path_to_audio}/{audio_file}",f"{tweeter_handle}/{audio_file}")

def create_folder(bucket_name, destination_folder_name):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_folder_name)

    blob.upload_from_string('')

    print('Created {} .'.format(
        destination_folder_name))