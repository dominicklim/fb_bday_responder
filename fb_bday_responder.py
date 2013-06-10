#! /usr/bin/env python

from djl_ui import *
from djl_input import *
from djl_post_responder import *
from djl_post_processor import *

djl_seperator()
print_exit_tip()

fb = FacebookAccessInput()
fb.show()

year = YearInput(fb.me["birthday"])
year.show()

processor = PostProcessor(year.birthdate, fb)
processor.get_posts()

prompt_for_continue()
reply_template = ReplyTemplateInput()
reply_template.show()

print_begin_responding()
print_confirm_continue()

GenericResponder(processor.generic_posts, reply_template.val, fb.graph).respond()
SpecialResponder(processor.special_posts, reply_template.val, fb.graph).respond()
