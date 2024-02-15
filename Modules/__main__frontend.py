import logging
import os
import sys
from argparse import ArgumentParser
from time import time

import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import requests


sys.path.append("TwitterAPI")
sys.path.append("LDA")
sys.path.append("V2A")
sys.path.append("A2T")
sys.path.append("GraphicalRepresentation")


import base_tweet_parser as BaseParser
import threaded_tweet_parser as ThreadedParser
import get_handlers as GetHandlers
import fetch_tweet_handler as fetch_tweets

import topicModelling as topic_modeler

import videotoAudio as video_audio
import audiotoText as audio_text
import to_googleBucket as upload_audio_cloud
import ProjectOutput as outputGraph


import pandas as pd
import threading

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

url = "http://localhost:8080/"

handle_thread_arr = [-1] * 7
handle_process_thread = [-1] * 3


def main(handle):
    fetch_tweets.fetch_tweets(handle)


def convert_video_audio():
    video_audio.convert_to_audio("Health")


def audio_to_text():
    upload_audio_cloud.upload_all_audios("Health")
    audio_text.transcribe_file("Health")


def cluster():
    topic_modeler.topicModel("Health")
    outputGraph.parse_data_to_output("Health")


def set_thread(thread, handle):
    if handle == "bbchealth":
        handle_thread_arr[0] = thread
    elif handle == "HarvardHealth":
        handle_thread_arr[1] = thread
    elif handle == "StanfordMed":
        handle_thread_arr[2] = thread
    elif handle == "NatureMedicine":
        handle_thread_arr[3] = thread
    elif handle == "healthmagazine":
        handle_thread_arr[4] = thread
    elif handle == "WHO":
        handle_thread_arr[5] = thread
    elif handle == "HarvardChanSPH":
        handle_thread_arr[6] = thread


def start_thread(handle):
    if handle == "bbchealth":
        handle_thread_arr[0].start()
    elif handle == "HarvardHealth":
        handle_thread_arr[1].start()
    elif handle == "StanfordMed":
        handle_thread_arr[2].start()
    elif handle == "NatureMedicine":
        handle_thread_arr[3].start()
    elif handle == "healthmagazine":
        handle_thread_arr[4].start()
    elif handle == "WHO":
        handle_thread_arr[5].start()
    elif handle == "HarvardChanSPH":
        handle_thread_arr[6].start()


def set_process(thread, process):
    if process == "convertVTA":
        handle_process_thread[0] = thread
    elif process == "convertATT":
        handle_process_thread[1] = thread
    elif process == "cluster":
        handle_process_thread[2] = thread


def start_process(process):
    if process == "convertVTA":
        handle_process_thread[0].start()
    elif process == "convertATT":
        handle_process_thread[1].start()
    elif process == "cluster":
        handle_process_thread[2].start()


def check_thread(handle):
    if handle == "bbchealth":
        if handle_thread_arr[0] == -1:
            return False
        return handle_thread_arr[0].is_alive()
    elif handle == "HarvardHealth":
        if handle_thread_arr[1] == -1:
            return False
        return handle_thread_arr[1].is_alive()
    elif handle == "StanfordMed":
        if handle_thread_arr[2] == -1:
            return False
        return handle_thread_arr[2].is_alive()
    elif handle == "NatureMedicine":
        if handle_thread_arr[3] == -1:
            return False
        return handle_thread_arr[3].is_alive()
    elif handle == "healthmagazine":
        if handle_thread_arr[4] == -1:
            return False
        return handle_thread_arr[4].is_alive()
    elif handle == "WHO":
        if handle_thread_arr[5] == -1:
            return False
        return handle_thread_arr[5].is_alive()
    elif handle == "HarvardChanSPH":
        if handle_thread_arr[6] == -1:
            return False
        return handle_thread_arr[6].is_alive()


def check_thread_process(process):
    if process == "convertVTA":
        if handle_process_thread[0] == -1:
            return False
        return handle_process_thread[0].is_alive()
    elif process == "convertATT":
        if handle_process_thread[1] == -1:
            return False
        return handle_process_thread[1].is_alive()
    elif process == "cluster":
        if handle_process_thread[2] == -1:
            return False
        return handle_process_thread[2].is_alive()


class Serv(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.path)

        if self.path == "/bbchealthresult?":
            self.path = (
                "./GraphicalRepresentation/assets/navigation/bbchealth/result.html"
            )
            try:
                file_to_open = open(self.path[:]).read()
                self.send_response(200)
            except:
                file_to_open = "File not found"
                self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes(file_to_open, "utf-8"))
            thread = threading.Thread(target=main, args=("bbchealth",))
            print(thread)
            set_thread(thread, "bbchealth")
            start_thread("bbchealth")
        elif self.path == "/getbbchealthresult":
            try:
                file_to_open = open(
                    file="./Data/Fetched/bbchealth/tweets/bbchealth.csv",
                    encoding="utf-8",
                ).read()
                print(file_to_open)
                self.send_response(200)
            except:
                file_to_open = "File not found"
                self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes(file_to_open, "utf-8"))
        elif self.path == "/bbchealthtest":
            if check_thread("bbchealth"):
                self.send_response(404)
                self.end_headers()
            else:
                self.send_response(200)
                self.end_headers()
        elif self.path == "/bbchealthnext?":
            self.path = (
                "./GraphicalRepresentation/assets/navigation/HarvardHealth/result.html"
            )
            try:
                file_to_open = open(self.path[:]).read()
                self.send_response(200)
            except:
                file_to_open = "File not found"
                self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes(file_to_open, "utf-8"))
            thread = threading.Thread(target=main, args=("HarvardHealth",))
            set_thread(thread, "HarvardHealth")
            start_thread("HarvardHealth")
        elif self.path == "/getHarvardHealthresult":
            try:
                file_to_open = open(
                    file="./Data/Fetched/HarvardHealth/tweets/HarvardHealth.csv",
                    encoding="utf-8",
                ).read()
                print(file_to_open)
                self.send_response(200)
            except:
                file_to_open = "File not found"
                self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes(file_to_open, "utf-8"))
        elif self.path == "/HarvardHealthtest":
            if check_thread("HarvardHealth"):
                self.send_response(404)
                self.end_headers()
            else:
                self.send_response(200)
                self.end_headers()
        elif self.path == "/HarvardHealthnext?":
            self.path = (
                "./GraphicalRepresentation/assets/navigation/StanfordMed/result.html"
            )
            try:
                file_to_open = open(self.path[:]).read()
                self.send_response(200)
            except:
                file_to_open = "File not found"
                self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes(file_to_open, "utf-8"))
            thread = threading.Thread(target=main, args=("StanfordMed",))
            set_thread(thread, "StanfordMed")
            start_thread("StanfordMed")
        elif self.path == "/getStanfordMedresult":
            try:
                file_to_open = open(
                    file="./Data/Fetched/StanfordMed/tweets/StanfordMed.csv",
                    encoding="utf-8",
                ).read()
                print(file_to_open)
                self.send_response(200)
            except:
                file_to_open = "File not found"
                self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes(file_to_open, "utf-8"))
        elif self.path == "/StanfordMedtest":
            if check_thread("StanfordMed"):
                self.send_response(404)
                self.end_headers()
            else:
                self.send_response(200)
                self.end_headers()
        elif self.path == "/StanfordMednext?":
            self.path = (
                "./GraphicalRepresentation/assets/navigation/NatureMedicine/result.html"
            )
            try:
                file_to_open = open(self.path[:]).read()
                self.send_response(200)
            except:
                file_to_open = "File not found"
                self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes(file_to_open, "utf-8"))
            thread = threading.Thread(target=main, args=("NatureMedicine",))
            set_thread(thread, "NatureMedicine")
            start_thread("NatureMedicine")
        elif self.path == "/getNatureMedicineresult":
            try:
                file_to_open = open(
                    file="./Data/Fetched/NatureMedicine/tweets/NatureMedicine.csv",
                    encoding="utf-8",
                ).read()
                print(file_to_open)
                self.send_response(200)
            except:
                file_to_open = "File not found"
                self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes(file_to_open, "utf-8"))
        elif self.path == "/NatureMedicinetest":
            if check_thread("NatureMedicine"):
                self.send_response(404)
                self.end_headers()
            else:
                self.send_response(200)
                self.end_headers()
        elif self.path == "/NatureMedicinenext?":
            self.path = (
                "./GraphicalRepresentation/assets/navigation/healthmagazine/result.html"
            )
            try:
                file_to_open = open(self.path[:]).read()
                self.send_response(200)
            except:
                file_to_open = "File not found"
                self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes(file_to_open, "utf-8"))
            thread = threading.Thread(target=main, args=("healthmagazine",))
            set_thread(thread, "healthmagazine")
            start_thread("healthmagazine")
        elif self.path == "/gethealthmagazineresult":
            try:
                file_to_open = open(
                    file="./Data/Fetched/healthmagazine/tweets/healthmagazine.csv",
                    encoding="utf-8",
                ).read()
                print(file_to_open)
                self.send_response(200)
            except:
                file_to_open = "File not found"
                self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes(file_to_open, "utf-8"))
        elif self.path == "/healthmagazinetest":
            if check_thread("healthmagazine"):
                self.send_response(404)
                self.end_headers()
            else:
                self.send_response(200)
                self.end_headers()
        elif self.path == "/healthmagazinenext?":
            self.path = "./GraphicalRepresentation/assets/navigation/WHO/result.html"
            try:
                file_to_open = open(self.path[:]).read()
                self.send_response(200)
            except:
                file_to_open = "File not found"
                self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes(file_to_open, "utf-8"))
            thread = threading.Thread(target=main, args=("WHO",))
            set_thread(thread, "WHO")
            start_thread("WHO")
        elif self.path == "/getWHOresult":
            try:
                file_to_open = open(
                    file="./Data/Fetched/WHO/tweets/WHO.csv", encoding="utf-8"
                ).read()
                print(file_to_open)
                self.send_response(200)
            except:
                file_to_open = "File not found"
                self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes(file_to_open, "utf-8"))
        elif self.path == "/WHOtest":
            if check_thread("WHO"):
                self.send_response(404)
                self.end_headers()
            else:
                self.send_response(200)
                self.end_headers()
        elif self.path == "/WHOnext?":
            self.path = (
                "./GraphicalRepresentation/assets/navigation/HarvardChanSPH/result.html"
            )
            try:
                file_to_open = open(self.path[:]).read()
                self.send_response(200)
            except:
                file_to_open = "File not found"
                self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes(file_to_open, "utf-8"))
            thread = threading.Thread(target=main, args=("HarvardChanSPH",))
            set_thread(thread, "HarvardChanSPH")
            start_thread("HarvardChanSPH")
        elif self.path == "/getHarvardChanSPHresult":
            try:
                file_to_open = open(
                    file="./Data/Fetched/HarvardChanSPH/tweets/HarvardChanSPH.csv",
                    encoding="utf-8",
                ).read()
                print(file_to_open)
                self.send_response(200)
            except:
                file_to_open = "File not found"
                self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes(file_to_open, "utf-8"))
        elif self.path == "/HarvardChanSPHtest":
            if check_thread("HarvardChanSPH"):
                self.send_response(404)
                self.end_headers()
            else:
                self.send_response(200)
                self.end_headers()
        elif self.path == "/HarvardChanSPHnext?":
            self.path = (
                "./GraphicalRepresentation/assets/navigation/VideoToAudio/result.html"
            )
            try:
                file_to_open = open(self.path[:]).read()
                self.send_response(200)
            except:
                file_to_open = "File not found"
                self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes(file_to_open, "utf-8"))
            thread = threading.Thread(target=convert_video_audio)
            set_process(thread, "convertVTA")
            start_process("convertVTA")

        elif self.path == "/videoToAudioTest":
            if check_thread("convertVTA"):
                self.send_response(404)
                self.end_headers()
            else:
                self.send_response(200)
                self.end_headers()

        elif self.path == "/audioToText?":
            self.path = (
                "./GraphicalRepresentation/assets/navigation/audioToText/result.html"
            )
            try:
                file_to_open = open(self.path[:]).read()
                self.send_response(200)
            except:
                file_to_open = "File not found"
                self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes(file_to_open, "utf-8"))
            thread = threading.Thread(target=audio_to_text)
            set_process(thread, "convertATT")
            start_process("convertATT")

        elif self.path == "/audioToTextTest":
            if check_thread("convertATT"):
                self.send_response(404)
                self.end_headers()
            else:
                self.send_response(200)
                self.end_headers()
        elif self.path == "/cluster?":
            self.path = (
                "./GraphicalRepresentation/assets/navigation/cluster/result.html"
            )
            try:
                file_to_open = open(self.path[:]).read()
                self.send_response(200)
            except:
                file_to_open = "File not found"
                self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes(file_to_open, "utf-8"))
            thread = threading.Thread(target=cluster)
            set_process(thread, "cluster")
            start_process("cluster")
        elif self.path == "/clusterTest":
            if check_thread("cluster"):
                self.send_response(404)
                self.end_headers()
            else:
                self.send_response(200)
                self.end_headers()

    def do_POST(self):
        if self.path == "/":
            self.path = "./GraphicalRepresentation/project_output_result.html"
        try:
            file_to_open = open(self.path[:]).read()
            self.send_response(200)
        except:
            file_to_open = "File not found"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file_to_open, "utf-8"))


if __name__ == "__main__":
    print("SERVER STARTED")
    httpd = HTTPServer(("localhost", 8080), Serv)
    httpd.serve_forever()
