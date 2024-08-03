import sys
import os
import glob
import json
import time
import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from http import HTTPStatus

from convert_articles import decorate

local_tz = datetime.timezone(-datetime.timedelta(seconds=time.timezone))
jst_tz = datetime.timezone(datetime.timedelta(hours=9))

class HomePageHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        try:
            payload = self.rfile.read(int(self.headers['content-length'])).decode('utf-8')

            if len("content") > 0xffff:
                raise RuntimeError("Too long data")

            payload = json.loads(payload)

            if "msgtype" not in payload:
                raise RuntimeError("Lack of \"msgtype\" field")
            
            if payload["msgtype"] == "preview":
                decorated = decorate(payload["content"])
                self.send_response(200)
                self.send_header('Content-type', "text/html")
                self.end_headers()
                self.wfile.write(decorated.encode())
                return
            elif payload["msgtype"] == "save":
                posted_date = datetime.datetime.now(local_tz).astimezone(jst_tz)
                modifying = False

                if "id" in payload:
                    post_id = payload["id"]
                    if post_id.isdecimal() and glob.glob("articles/sources/" + post_id):
                        modifying = True

                if not modifying:
                    if "title" not in payload or "content" not in payload:
                        raise RuntimeError("Lack of any fields of \"title\", \"content\"")
                    post_id = posted_date.strftime("%Y-%m-%d-%H%M")
                    if glob.glob("articles/sources/" + post_id):
                        raise RuntimeError("Rate Limit")

                    os.mkdir("articles/sources/" + post_id)

                    created_time = posted_date.strftime("%Y-%m-%d %H:%M:%S %z")

                    with open("articles/sources/" + post_id + "/meta.json", mode="w", encoding="utf-8") as f:
                        json.dump({
                            "title": payload["title"],
                            "created_time": created_time,
                            "modified_time": created_time
                        }, f)

                    with open("articles/sources/" + post_id + "/content.txt", mode="w", encoding="utf-8") as f:
                        f.write(payload["content"])

                    self.send_response(200)
                    self.send_header('Content-type', "text/plain")
                    self.end_headers()
                    self.wfile.write(created_time.encode())

                    return

            raise RuntimeError("Invalid msgtype")
        except Exception as e:
            print(e)
            self.send_error(
                    HTTPStatus.BAD_REQUEST,
                    "Bad Request")
            return

def run(host="localhost", port=8080):
    address = (host, port)
    server = HTTPServer(address, HomePageHTTPRequestHandler)
    server.serve_forever()

if __name__ == "__main__":
    match len(sys.argv)-1:
        case 0:
            run()
        case 1:
            run(port=int(sys.argv[1]))
        case _:
            run(sys.argv[1], int(sys.argv[2]))