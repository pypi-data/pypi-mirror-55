
from pkg_resources import resource_string

from jinja2 import Template
from jinja2 import Environment, BaseLoader

import argparse
import http.server
import socketserver
import os
import sys
import json
import requests
import webbrowser
from threading import Timer

from jinja2 import BaseLoader, TemplateNotFound

from github_service import GithubService

PORT = 8080
Handler = http.server.SimpleHTTPRequestHandler
socketserver.TCPServer.allow_reuse_address = True

class ResourceLoader(BaseLoader):
    def __init__(self, path):
        self.path = path

    def get_source(self, environment, template):
        filename = '/'.join((self.path, template))
        mtime = os.path.getmtime(filename)
        return resource_string("personal_page_creator", filename).decode('utf-8'), filename, lambda: mtime == os.path.getmtime(filename)


environment = Environment(loader=ResourceLoader('templates'))



def main():
    parser = argparse.ArgumentParser(description="Generate static website to be used in GitHub pages")
    parser.add_argument(
        "--config", "-c", type=str, required=False, default="./config.json",
        dest="config_path", help="Path to the config file"
    )
    parser.add_argument(
        "--dry-run", "-dr", type=bool, required=False, default=False,
        dest="dry_run", help="Enable dry run"
    )
    args = parser.parse_args()
    if os.path.isfile(args.config_path):
        try:
            config = json.loads(open(args.config_path).read())
        except:
            raise argparse.ArgumentTypeError('Given path is not a valid json file')
    else:
        raise argparse.ArgumentTypeError('Given path does not exist')
    
    username = config["username"]
    gh_service = GithubService("udithprabhu", config)

    with open("index.html", "w") as f:
        f.write(environment.get_template("index.template").render(data=gh_service))

    with open("style.css", "w") as f:
        f.write(environment.get_template("style.template").render(data=gh_service))

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        try:
            print("serving at port", PORT)
            Timer(0.1, lambda: webbrowser.open_new("http://localhost:{}".format(PORT))).start()
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.shutdown()
            httpd.server_close()
            print("\nClosing server")
            

if __name__ == '__main__':
    main()