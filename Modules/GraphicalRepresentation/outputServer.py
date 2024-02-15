import csv
from collections import defaultdict
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
import os


class Serv(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = "/ProjectOutputWebpage.html"
        elif self.path == "/?":
            self.path = "/ProjectOutputWebpage.html"
        try:
            print(self.path[1:])
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
        except:
            file_to_open = "File not found"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file_to_open, "utf-8"))

print("SERVER STARTED")
httpd = HTTPServer(("localhost", 8082), Serv)
httpd.serve_forever()
