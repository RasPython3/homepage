import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler

def run(host="192.168.3.8", port=8080):
    address = (host, port)
    server = HTTPServer(address, SimpleHTTPRequestHandler)
    server.serve_forever()

if __name__ == "__main__":
    match len(sys.argv)-1:
        case 0:
            run()
        case 1:
            run(port=int(sys.argv[1]))
        case _:
            run(sys.argv[1], int(sys.argv[2]))