import os
import logging
from time import time

import base_tweet_parser as BaseParser

import pandas as pd


def fetch_tweets(tweeter_handle):
    print("TEST", tweeter_handle)
    topic = "Health"
    limitOfTweet = 10

    parser = BaseParser.BaseTweetParser()

    path_to_video = os.path.join(".\\Data\\Fetched", tweeter_handle, "videos")
    path_to_tweet = os.path.join(".\\Data\\Fetched", tweeter_handle, "tweets")
    try:
        os.makedirs(path_to_video, exist_ok=False)
        os.makedirs(path_to_tweet, exist_ok=False)
    except Exception:
        logging.error("Twitter handler already extracted")
        return

    parser.fetch(tweeter_handle, limit=limitOfTweet)

    start = time()
    parser.download(parser.video_urls_textid, "videos", os.path.join(path_to_video))
    end = time()
    logging.info("Spent {} seconds downloading".format(end - start))
    logging.info("Fetched {} video files".format(len(parser.video_urls_textid)))

    logging.info("Saving tweets and video links to file")
    data_frame = pd.DataFrame(parser.tweet_text, columns=["Tweets"])
    data_frame.to_csv(path_to_tweet + "\\" + tweeter_handle + ".csv", index=False)
