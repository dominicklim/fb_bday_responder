from djl_ui import *
from djl_templater import *

class PostResponder(object):
    def __init__(self, posts, template, graph):
        self.posts = posts
        self.template = template
        self.templater = Templater()
        self.graph = graph

    def respond(self):
        for post in self.posts:
            self.send_response_to_post(post, self.response_to_post(post))

    def response_to_post(self, post):
        return ""

    def send_response_to_post(self, post, response):
        self.graph.post(path=str(post["id"]) + "/comments", message=response)
        djl_print(response)
        print djl_hint_seperator("sent to: " + post["sender"]["name"], 1)

class GenericResponder(PostResponder):
    def response_to_post(self, post):
        return self.templater.populate_template(self.template, post["sender"])

class SpecialResponder(PostResponder):
    def response_to_post(self, post):
        djl_print("Post from " + post["sender"]["name"] + ": ")
        djl_print("> " + post["msg"] + "")

        res = self.templater.populate_template(self.template, post["sender"])
        new_thanks = djl_input("Thank you note for " + post["sender"]["name"] + ": (Enter nothing to post a generic response)\n")

        if len(new_thanks) > 0: res = new_thanks
        return res
