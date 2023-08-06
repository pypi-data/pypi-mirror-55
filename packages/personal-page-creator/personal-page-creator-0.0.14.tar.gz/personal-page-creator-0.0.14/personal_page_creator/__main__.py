
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

PORT = 8080
Handler = http.server.SimpleHTTPRequestHandler
socketserver.TCPServer.allow_reuse_address = True


class GithubService:
    def __init__(self, username, config=None):
        self.username = username
        self.all_repos = self.__class__.get_repos(self.username)
        self.own_repos = list(filter(lambda repo: not repo["fork"], self.all_repos))
        self.forked_repos = list(filter(lambda repo: repo["fork"], self.all_repos))

        owner = self.all_repos[0]["owner"]
        self.avatar_url = owner["avatar_url"]
        self.profile_url = owner["html_url"]
        self.config = config

        self.read_config()


    def read_config(self):
        if self.config:
            self.own_repos = list(filter(lambda repo: repo["name"] not in self.config.get("excluded", []), self.own_repos))
            self.forked_repos = list(filter(lambda repo: repo["name"] not in self.config.get("excluded", []), self.forked_repos))


    @staticmethod
    def get_repos(username):
        requestUrl = "https://api.github.com/users/{}/repos?per_page=100&page={}&type=all"
        resp = []
        page_num = 1
        while True:
            l = json.loads(requests.get(requestUrl.format(username, page_num)).content.decode('utf-8'))
            resp.extend(l)
            if len(l) != 100:
                break
            page_num += 1
        return resp



class ResourceLoader(BaseLoader):
    def __init__(self, path):
        self.path = path

    def get_source(self, environment, template):
        filename = '/'.join((self.path, template))
        return resource_string(__name__, filename).decode('utf-8'), filename, lambda: True


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
    gh_service = GithubService(username, config)

    with open("index.html", "w") as f:
        f.write(environment.get_template("index.template").render(data=gh_service))

    with open("style.css", "w") as f:
        f.write(environment.get_template("style.template").render(data=gh_service))

    httpd = socketserver.TCPServer(("", PORT), Handler)
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