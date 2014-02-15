"""
SUS utility functions for text.
"""

import config as conf


def get_colored_text(text, foreground, background="default", bold=False, newline=True):
    """
    Get the ansi code for color formatted text.
    Possible color options are:
    - black
    - red
    - green
    - yellow
    - blue
    - magenta
    - cyan
    - white
    - default
    @param text: The text to format
    @param foreground: The foreground color.
    @param background: The background clolr
    @param bold: Whether to make the text bold.
    @param newline: WHether to add a new line character to the end
    @return: The formatted text.
    """
    color_dict = {"black": 0, "red": 1, "green": 2, "yellow": 3, "blue": 4, "magenta": 5, "cyan": 6, "white": 7,
                  "default": 9}
    if not foreground in color_dict or not background in color_dict:
        result = text
        if newline: result += "\n"
    else:
        result = "\033["
        boldstr = "1" if bold else "0"
        result += boldstr
        result += ";"
        foreground_string = "3" + str(color_dict[foreground]) + "m"
        result += foreground_string

        result += "\033["
        background_string = "4" + str(color_dict[background]) + "m"
        result += background_string

        result += text

        result += "\033[0m"

        if newline:
            result += "\n"
    return result


def print_colored_text(text, foreground, background="default", bold=False, newline=True):
    """
    Print colored text as specified by @see get_colored_text
    """
    print(get_colored_text(text, foreground, background=background, bold=bold, newline=newline))


def status_block(value, true_color=conf.DEFAULT_TRUE_COLOR, false_color=conf.DEFAULT_FALSE_COLOR):
    """
    Get a colored block of text depending on whether the given boolean value is true or false.
    @param value: The given boolean value.
    @param true_color: The valua of the block given that the value is true.
    @param false_color: The value of the block given that the value is false.
    @return: The color formatted block of text
    """
    if value:
        color = true_color
    else:
        color = false_color
    return get_colored_text(conf.EVALUATION_BLOCK, "default", background=color, bold=False, newline=False)
