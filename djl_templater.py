from djl_ui import *

class Templater(object):
    def __init__(self):
        self.templ_dict = {
            "l_first": color_string(OKBLUE, "%(l_first)s"),
            "u_first": color_string(OKBLUE, "%(u_first)s"),
            "l_last": color_string(OKBLUE, "%(l_last)s"),
            "u_last": color_string(OKBLUE, "%(u_last)s")
        }
        self.sample_templ = "thanks, %(u_first)s!"
        self.sample_name_dict = {
            "first_name": color_string(OKBLUE, "Tom"),
            "last_name": color_string(OKBLUE, "Anderson")
        }

    def show_tutorial(self):
        djl_print("Construct the template for your generic replies using the following variables:")
        djl_print("%(l_first)s = lowercase first name" % self.templ_dict)
        djl_print("%(u_first)s = uppercase first name" % self.templ_dict)
        djl_print("%(l_last)s = lowercase last name" % self.templ_dict)
        djl_print("%(u_last)s = uppercase last name" % self.templ_dict)
        prompt_for_continue()
        djl_print("Here's the default template:")
        djl_print(self.sample_templ % self.templ_dict)
        prompt_for_continue()
        djl_print("Here's the reply %(first_name)s %(last_name)s would get:" % self.sample_name_dict)
        djl_print(self.populate_template(self.sample_templ, self.sample_name_dict))
        prompt_for_continue()

    def populate_template(self, template, name_dict):
        first = name_dict["first_name"]
        last = name_dict["last_name"]
        return template % {"l_first": first.lower(), "u_first": first,
                           "l_last": last.lower(), "u_last": last}
