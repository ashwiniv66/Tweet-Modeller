import logging
import os
import sys
from argparse import ArgumentParser
from time import time

sys.path.append("TwitterAPI")
sys.path.append("LDA")
sys.path.append("V2A")
sys.path.append("A2T")
sys.path.append("GraphicalRepresentation")


import base_tweet_parser as BaseParser
import threaded_tweet_parser as ThreadedParser
import get_handlers as GetHandlers

import topicModelling as topic_modeler

import videotoAudio as video_audio
import audiotoText as audio_text
import to_googleBucket as upload_audio_cloud
""" 
import ProjectOutput as outputGraph """



import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def main():
    arg_parser = ArgumentParser()
    arg_parser.add_argument(
        "--topic", type=str, help="Twitter account handle", default="Health"
    )
    arg_parser.add_argument(
        "--limit", type=int, default=3200, help="Number of media urls to download"
    )
    arg_parser.add_argument(
        "--scrape-link",
        dest="scrape",
        help="Store scraped links to file",
        action="store_true",
    )
    arg_parser.add_argument(
        "--threaded",
        help="Use a threaded approach to download media. By default spawns 10 threads",
        action="store_true",
    )
    args = arg_parser.parse_args()
    if args.threaded:
        logging.info("Using threads to download images and videos")
        parser = ThreadedParser.ThreadedTweetParser(100)
    else:
        parser = BaseParser.BaseTweetParser()

    twitter_handlers = GetHandlers.GetHandlers().get_twitter_handlers(args.topic)

    for tweeter_handle in twitter_handlers:

        path_to_video = os.path.join("Data\\Fetched", tweeter_handle, "videos")
        path_to_tweet = os.path.join("Data\\Fetched", tweeter_handle, "tweets")
        try:
            os.makedirs(path_to_video, exist_ok=False)
            os.makedirs(path_to_tweet, exist_ok=False)
        except Exception:
            logging.error("Twitter handler already extracted")
            continue

        parser.fetch(tweeter_handle, limit=args.limit)

        start = time()
        parser.download(parser.video_urls_textid, "videos", os.path.join(path_to_video))
        end = time()
        logging.info("Spent {} seconds downloading".format(end - start))
        logging.info("Fetched {} video files".format(len(parser.video_urls_textid)))

        logging.info("Saving tweets and video links to file")
        data_frame = pd.DataFrame(parser.tweet_text, columns=["Tweets"])
        data_frame.to_csv(path_to_tweet + "\\" + tweeter_handle + ".csv", index=False)

    video_audio.convert_to_audio(args.topic)
    upload_audio_cloud.upload_all_audios(args.topic)
    audio_text.transcribe_file(args.topic)
    topic_modeler.topicModel(args.topic)
    print("TEST")
    """ outputGraph.parse_data_to_output(args.topic) """

if __name__ == "__main__":
    main()
