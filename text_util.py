def get_colored_text(text, foreground, background="default", bold=False, newline=True):
    COLOR_DICT = {"black": 0, "red": 1, "green": 2, "yellow": 3, "blue": 4, "magenta": 5, "cyan": 6, "white": 7,
                  "default": 9}
    if not foreground in COLOR_DICT or not background in COLOR_DICT:
        result = text
        if newline: result += "\n"
    else:
        result = "\033["
        boldstr = "1" if bold else "0"
        result += boldstr
        result += ";"
        foreground_string = "3" + str(COLOR_DICT[foreground]) + "m"
        result += foreground_string

        result += "\033["
        background_string = "4" + str(COLOR_DICT[background]) + "m"
        result += background_string

        result += text

        result += "\033[0m"

        newline_str = "\n" if newline else ""
        result += newline_str
    return result


def print_colored_text(text, foreground, background="default", bold=False, newline=True):
    print(get_colored_text(text, foreground, background=background, bold=bold, newline=newline))