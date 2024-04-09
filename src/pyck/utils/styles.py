def _colors_256(color_: int, s: str):
    """Takes in a string and a color code and returns the colored string."""
    return f"\033[38;5;{str(color_)}m{s}\033[0;0m"


def red(s: str):
    """Returns a string in red."""
    return _colors_256(160, s)


def grey(s: str):
    """Returns a string in grey."""
    return _colors_256(240, s)


def purple(s: str):
    """Returns a string in purple."""
    return _colors_256(21, s)


def bold(s: str):
    """Returns a string in bold."""
    return f"\033[1m{s}\033[0m"
