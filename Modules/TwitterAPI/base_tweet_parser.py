import json
import os
import shutil
import logging

import tweepy
import wget
from tweepy import OAuthHandler

from os.path import expanduser

home = expanduser("~")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


class BaseTweetParser(object):
    global_tweet_count = 0

    def __init__(self):
        self.video_urls_textid = []
        self.tweet_text = []
        self.api = None
        consumer_key, consumer_secret = self._fetch_credentials()
        auth = OAuthHandler(consumer_key, consumer_secret)
        self.api = tweepy.API(auth)

    def _fetch_credentials(self):
        consumer_key = os.getenv("CONSUMER_KEY")
        consumer_secret = os.getenv("CONSUMER_SECRET")
        data = None
        if not all([consumer_secret, consumer_key]):
            with open(os.path.join(home, ".twitter.json"), "r") as f:
                data = json.loads(f.read())
        consumer_key = data["consumer_key"]
        consumer_secret = data["consumer_secret"]
        return consumer_key, consumer_secret

    def download(self, urls, file_type, destination):
        self._download_from_urls("MAIN", list(urls), file_type, destination)

    def _download_from_urls(self, name, batch, file_type, dest_dir):
        for [url, index] in batch:
            logging.info("Thread: {} downloading {} to {}".format(name, url, dest_dir))
            path = os.path.join(dest_dir, str(index))
            wget.download(url, path)

    def process_tweet_video(self, tweet):
        try:
            extended = tweet.extended_entities
            if not extended:
                return []
            rv = []
            if "media" in extended:
                for x in extended["media"]:
                    if x["type"] == "photo":
                        return []
                    elif x["type"] in ["video", "animated_gif"]:
                        variants = x["video_info"]["variants"]
                        variants.sort(key=lambda x: x.get("bitrate", 0))
                        url = variants[-1]["url"].rsplit("?tag")[0]
                        rv.append(url)
            logging.debug("Video: true")
            return rv
        except AttributeError:
            logging.debug("Video: false")
            return []

    def process_tweet_text(self, tweet):
        try:
            text = tweet.full_text
            if not text:
                return ""
            return text
        except AttributeError:
            logging.error("Text not present in tweet")
            return ""

    def fetch(self, account, tweet_mode="extended", limit=None):
        dir_name = account
        api = self.api

        tweet_id = 0
        video_urls_textid = []
        tweets_text = []

        for tweet in tweepy.Cursor(
            api.user_timeline, id=account, tweet_mode=tweet_mode
        ).items(limit):
            print("Tweet ID: {}".format(tweet_id))
            rt = self.process_tweet_text(tweet)
            rv = self.process_tweet_video(tweet)
            tweets_text.append(rt)
            for r in rv:
                video_urls_textid.append([r, tweet_id])
            tweet_id += 1
            self.global_tweet_count += 1

        self.video_urls_textid = video_urls_textid
        self.tweet_text = tweets_text