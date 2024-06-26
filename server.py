import os
import argparse
from http.server import HTTPServer
from http.server import SimpleHTTPRequestHandler

def run(
    server_class=HTTPServer,
    port=8000,
    directory=None,
):
    if directory:  # Change the current working directory if directory is specified
        os.chdir(directory)
    server_address = ("", port)
    httpd = server_class(server_address, SimpleHTTPRequestHandler)
    print(f"Serving HTTP on http://localhost:{port} from directory '{directory}'...")
    httpd.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HTTP Server")
    parser.add_argument(
        "--dir", type=str, help="Directory to serve files from", default="."
    )
    parser.add_argument("--port", type=int, help="Port to serve HTTP on", default=8888)
    args = parser.parse_args()

    run(port=args.port, directory=args.dir)
