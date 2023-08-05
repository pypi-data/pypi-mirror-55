"""
Command line core utility package
"""

import getpass

from cspybase.services.core.connection import CsPyConnection
from cspybase.services.core.exception import CsPyException


def choose_password():
    password = getpass.getpass(prompt="Password: ")
    print("   >>> *****\n")
    return password


def choose_string(prompt_text, default_value=None, help_function=None):
    text = "%s: " % prompt_text if default_value is None else "%s [%s]: " % (prompt_text, default_value)
    chosen = input(text).strip()
    while _is_empty_string(chosen) or chosen == '?':
        if chosen == '?' and help_function is not None:
            help_function()
        if _is_empty_string(chosen) and default_value is not None:
            chosen = default_value
            break
        chosen = input(text).strip()

    print("   >>> %s\n" % chosen)
    return chosen


def choose_integer(prompt_text, int_default_value=None, help_function=None):
    chosen = None
    default_value = None if int_default_value is None else str(int_default_value)
    while _integer_or_none(chosen) is None:
        chosen = choose_string(prompt_text, default_value, help_function)
    return int(chosen)


def choose_project_name():
    project_name = choose_string("Project name", "teste")
    return project_name


def create_connection():
    hostname = choose_string("Host name", "localhost")
    port = choose_integer("Host port", 8010)
    user = choose_string("User", "admin")
    password = choose_password()
    connection = CsPyConnection(hostname, port)
    connected = connection.connect_with_login(user, password)
    if not connected:
        raise CsPyException('Could not create a connection for %s at %s:%d' % (user, hostname, port))
    return connection


def _integer_or_none(txt):
    if txt is None:
        return None
    try:
        i = int(txt)
        return i
    except ValueError:
        return None


def _is_empty_string(txt):
    if txt is None:
        return True
    if txt.strip() == "":
        return True
    return False
