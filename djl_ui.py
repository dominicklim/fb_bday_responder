from djl_colors import *
import sys

def djl_print(string): print break_string_at_column(string, 80)

def djl_input(msg): return raw_input(break_string_at_column(msg, 80))

def seperator(columns): return "-" * columns

def djl_seperator(): print seperator(80)

def djl_y_or_n_seperator(): print djl_hint_seperator("(n = No; not n = Yes)", 2)

def djl_hint_seperator(hint, rt_sep_len):
    hint = " " + hint + " "
    return seperator(80 - len(hint) - rt_sep_len) + hint + seperator(rt_sep_len)

def break_string_at_column(string, column):
    new_string = ""

    while len(string) > column:
        closest_line_ender = closest_space_or_dash(string, column) + 1
        if (closest_line_ender == 0): break
        new_string += string[:closest_line_ender] + "\n"
        string = string[closest_line_ender:]

    return new_string + string

def closest_space_or_dash(string, column):
    colors = color_matches(string)
    cl_string = colorless_string(string)

    spaces = [ix for ix, c in enumerate(cl_string) if c == " "]
    next_space = next((spaces.index(x) for x in spaces if x > column), -1)

    if next_space > 0:
        break_index = spaces[next_space - 1]
        break_index_copy = break_index

        for i in range(len(colors)):
            if colors[i]["end"] < break_index_copy + colors[i]["len"]:
                break_index_copy += colors[i]["len"]
            else:
                break
            if i % 2 == 1: break_index = break_index_copy

        return break_index
    elif len(spaces) > 0 and spaces[-1] <= column:
        return spaces[-1]
    elif len(string) > column:
        if len(colors) > 1: column += colors[0]["len"]
        return column - 1
    else:
        return -1

def confirm_yes_or_no(msg):
    djl_y_or_n_seperator()
    user_input = djl_input(msg)
    try: return str(user_input).lower() == "n"
    except: return False

def write(string):
    sys.stdout.write("\r %s" % (" " * 80))
    sys.stdout.write("\r%s" % string)
    sys.stdout.flush()

def print_exit_tip():
    djl_print(color_string(HEADER, "Press ctrl+c to exit any time."))

def print_begin_responding():
    djl_print(color_string(HEADER, "We will now begin responding to posts."))

def print_confirm_continue():
    if confirm_yes_or_no("Would you like to continue?: "): exit()

def prompt_for_continue():
    djl_input(djl_hint_seperator("Press enter/return to continue", 3))

def exit():
    print djl_hint_seperator("So long!", 2)
    sys.exit()
