import re

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
COLORREGEX = r'\x1b\[\d+m'

def color_matches(string):
    matches = list(re.finditer(COLORREGEX, string))
    return [{"end":m.end(), "start":m.start(), "len":m.end() - m.start()} for i, m in enumerate(matches)]

def colorless_string(string):
    return re.sub(COLORREGEX, '', string)

def color_string(color, string):
    return color + string + ENDC
