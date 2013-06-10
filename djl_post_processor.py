from dateutil import parser
from datetime import timedelta
from random import randrange
from djl_ui import *

class PostProcessor(object):
    def __init__(self, birthdate, fb):
        self.birthdate = birthdate
        self.fb = fb
        self.feed_link = "me/feed"
        self.bday_greets = set(["happy", "b'day", "bday", "birthday"])
        self.should_get_more_feeds = True
        self.should_animate_getting_posts = True
        self.num_posts = 0
        self.animated_posts = 0
        self.generic_posts = []
        self.special_posts = []
        self.loading_msgs = ["Getting posts", "Still digging",
                             "Boy, you're popular",
                             "What's for lunch?",
                             "Why do they call it facebook anyway?"]
        self.loading_msg = self.loading_msgs[0]

    def get_posts(self):
        while self.should_get_more_feeds:
            if self.should_animate_getting_posts:
                self.animate_getting_posts()
            self.feed_link = self.get_post(self.fb.graph.get(self.feed_link))

    def get_post(self, feeds):
        for feed in feeds["data"]:
            post_date = parser.parse(feed["created_time"]).replace(tzinfo=None)

            is_too_early = post_date.__lt__(self.birthdate - timedelta(days=1))
            if is_too_early: return self.stop_getting_posts()

            is_too_late = post_date.__gt__(self.birthdate + timedelta(days=2))
            is_not_msg = not feed.has_key("message")
            is_from_me = feed["from"]["id"].encode("utf-8") == self.fb.me["id"]
            if is_too_late or is_not_msg or is_from_me: continue
            else: self.should_animate_getting_posts = False

            self.num_posts += 1
            self.update_gotten_posts(self.num_posts)
            msg = feed["message"]

            post = {"id": feed["id"], "msg": msg,
                    "sender": self.fb.graph.get(feed["from"]["id"])}

            if self.is_msg_generic(msg): self.generic_posts.append(post)
            else: self.special_posts.append(post)

        feed_link = feeds["paging"]["next"].replace("https://graph.facebook.com/", "")
        return feed_link

    def is_msg_generic(self, msg):
        is_bday_greet = self.bday_greets.intersection(set(msg.lower().split()))
        is_question = msg.find("?") != -1
        is_long = len(msg) > len("happy birthday, %s! :)" % self.fb.me["id"])
        is_short = len(msg) < len("happy bday")
        has_first_name = msg.lower().find(self.fb.me["first_name"].lower()) != -1
        has_nickname = is_long and not has_first_name
        is_special = is_question or is_long or is_short or has_nickname

        return is_bday_greet and not is_special

    def animate_getting_posts(self):
        self.animated_posts += 1
        if self.animated_posts % 18 == 0: self.set_new_loading_msg()
        write(self.loading_msg + "." * (self.animated_posts % 4))

    def set_new_loading_msg(self):
        self.loading_msg = self.loading_msgs[randrange(len(self.loading_msgs))]

    def update_gotten_posts(self, gotten_posts):
        if gotten_posts % 25 == 0: self.set_new_loading_msg()
        write(self.loading_msg + "... %s" % gotten_posts)

    def stop_getting_posts(self):
        write("\rFinished! Got %s posts." % self.num_posts)
        self.should_get_more_feeds = False
        self.print_post_stats()

    def print_post_stats(self):
        num_gen = len(self.generic_posts)
        num_spec = len(self.special_posts)
        per_gen = round(100.0 * num_gen / self.num_posts, 2)

        djl_print("")
        djl_seperator()
        djl_print("Generic: %(num)s (%(per).2f%%)" % {"num": num_gen, "per": per_gen})
        djl_print("Special: %(num)s (%(per).2f%%)" % {"num": num_spec, "per": 100 - per_gen})
