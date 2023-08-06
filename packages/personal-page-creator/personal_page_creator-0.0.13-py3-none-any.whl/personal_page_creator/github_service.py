
import json
import requests

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
            l = json.loads(requests.get(requestUrl.format(username, page_num)).content)
            resp.extend(l)
            if len(l) != 100:
                break
            page_num += 1
        return resp
