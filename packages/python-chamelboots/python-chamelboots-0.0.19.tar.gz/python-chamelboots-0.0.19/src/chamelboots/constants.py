"""Define constants used throughout the library."""

from enum import Enum

from faker import Faker
from lxml import etree

FAKE = Faker()
HTML_PARSER = etree.HTMLParser()


def global_safe(item: dict):
    """Update globals after checking for already existing globals."""

    return not any(key in globals() for key in item)


class WhiteSpace(str, Enum):
    EOL = "\n"
    SPACE = " "
    COMMA = ","
    COMMASPACE = ", "


class Join:
    LINES = WhiteSpace.EOL.join
    SPACES = WhiteSpace.SPACE.join
    COMMA = WhiteSpace.COMMA.join
    COMMASPACE = WhiteSpace.COMMASPACE.join
