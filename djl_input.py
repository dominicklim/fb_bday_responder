import webbrowser
import datetime
from djl_ui import *
from djl_templater import *
try:
    from facepy import GraphAPI
except ImportError, e:
    import sys
    djl_seperator()
    djl_print("Please install facepy. If you don't have pip, install that, too. Then type this into your terminal:")
    djl_print(color_string(HEADER, "$ sudo pip install facepy"))
    if not confirm_yes_or_no("Find out more about pip?: "):
        webbrowser.open("https://pypi.python.org/pypi/pip")
    exit()

class Input:
    def __init__(self, category, format, def_val, prompt_template="What is your %s?"):
        self.category = category
        self.format = format
        self.val = def_val
        self.err = ""
        self.input = ""
        self.prompt_template = prompt_template

    def set_error(self, err): self.err = (color_string(FAIL, err))
    def clear_error(self): self.err = ""

    def show(self):
        prompt = self.prompt_template % self.category
        if len(self.format) > 1: prompt += " {format: %s}" % self.format
        if len(self.err) > 1: prompt += " {error: %s}" % self.err

        self.input = djl_input(prompt + ": ")
        self.clear_error()
        self.validate()

    def validate(self):
        if len(self.err) > 0: return self.show()
        self.confirm()

    def confirm(self):
        self.set_error("reset requested")
        djl_seperator()
        djl_print(color_string(OKGREEN, "Good %s!" % self.category))
        djl_y_or_n_seperator()
        y_or_n = djl_input("Set %(cat)s to %(inp)s?: " % {
            "cat": color_string(OKGREEN, self.category), 
            "inp": color_string(OKGREEN, self.input), 
        })
        djl_seperator()

        try:
            if str(y_or_n).lower() != "n":
                self.val = self.input
                return
        except:
            pass

        self.show()

class FacebookAccessInput(Input):
    def __init__(self):
        Input.__init__(self, "Facebook Access Token", "", "")
        self.me = {}
        self.user_data_perms = ["publish_actions", "user_birthday"]
        self.extended_perms = ["read_stream"]

    def show(self):
        self.inform()
        Input.show(self)

    def validate(self):
        self.graph = GraphAPI(self.input)
        try:
            self.me = self.graph.get("me")
            perms = self.graph.get("me/permissions")["data"][0]
            self.check_perms(perms, self.user_data_perms)
            self.check_perms(perms, self.extended_perms)
        except:
            self.set_error("bad key")

        Input.validate(self)

    def check_perms(self, fb_perms, reqd_perms):
        for perm in reqd_perms:
            if not fb_perms.has_key(perm):
                self.set_error("[ ]%s unchecked" % perm)
                break

    def print_perms(self, perms):
        for perm in perms:
            djl_print(color_string(OKGREEN,"[x]%s" % perm))

    def inform(self):
        prompt = "You need a %s. Get one now?" % self.category

        if len(self.err) > 1: prompt += " {error: %s}" % self.err
        if not confirm_yes_or_no(prompt + ": "):
            webbrowser.open("https://developers.facebook.com/tools/explorer")
            self.show_required_permissions()

    def show_required_permissions(self):
        djl_seperator()
        djl_print("1. Click the 'Get Access Token' button.")
        djl_print("2. Check the following permission: ")
        djl_print("- User Data Permissions:")
        self.print_perms(self.user_data_perms)
        djl_print("- Extended Permissions:")
        self.print_perms(self.extended_perms)
        djl_print("3. Click the 'Get Access Token' button.")
        djl_print("4. Copy and paste the generated Access Token below.")
        djl_seperator()

class YearInput(Input):
    def __init__(self, birthday):
        self.now = datetime.datetime.now()
        Input.__init__(self, "year", "YYYY", self.now.year, "What %s are you responding to?")
        self.bday_list = birthday.split("/")

    def validate(self):
        try: year = int(self.input)
        except: self.set_error("bad format")

        try:
            self.birthdate = datetime.datetime(month=int(self.bday_list[0]),
                                               day=int(self.bday_list[1]),
                                               year=year, hour=0)
            if year < 2004: self.set_error("no facebook yet")
            elif self.now < self.birthdate: self.set_error("hasn't happened")
        except:
            self.set_error("invalid year")

        Input.validate(self)

class ReplyTemplateInput(Input):
    def __init__(self):
        Input.__init__(self, "reply template", "", "thanks, %(u_first)s!")
        self.templater = Templater()

    def show(self):
        self.templater.show_tutorial()
        Input.show(self)

    def validate(self):
        if len(self.input) > 0: self.val = self.input
        else: self.input = self.val
        Input.validate(self)

    def confirm(self):
        djl_seperator()
        djl_print("Here's the reply %(first_name)s %(last_name)s would get:" % self.templater.sample_name_dict)
        djl_print(self.templater.populate_template(self.input, self.templater.sample_name_dict))
        Input.confirm(self)
