import os

COLORS = dict(
    black=30,
    red=31,
    green=32,
    yellow=33,
    blue=34,
    magenta=35,
    cyan=36,
    white=37,
    brightblack=90,
    brightred=91,
    brightgreen=92,
    brightyellow=93,
    brightblue=94,
    brightmagenta=95,
    brightcyan=96,
    brightwhite=97,
)


def colored(text, color):
    """
    Returns a printable string in the given color.

    Colors are: black, red, green, yellow, blue, magenta, cyan, white,
    brightblack, brightred, brightgreen, brightyellow, brightblue,
    brightmagenta, brightcyan and brightwhite

    If the given color is invalid, it falls back to brightwhite.

    Respects the environment variable NO_COLOR.
    """
    if os.environ.get("NO_COLOR") is not None:
        return text

    colorcode = COLORS.get(color, COLORS["brightwhite"])
    sequence = "\033[%dm" % colorcode
    return "".join((sequence, text))


def lcut(s, sub):
    """
    Cuts off the substring `sub` if string `s` starts with it.
    """
    len_sub = len(sub)
    if s[:len_sub] == sub:
        return s[len_sub:]
    return s


def rcut(s, sub):
    """
    Cuts off the substring `sub` if string `s` ends with it.
    """
    len_sub = len(sub)
    if s[-len_sub:] == sub:
        return s[:-len_sub]
    return s


def cut(s, sub):
    """
    Cuts off the substring `sub` from the start and end of string `s`.
    """
    return rcut(lcut(s, sub), sub)
