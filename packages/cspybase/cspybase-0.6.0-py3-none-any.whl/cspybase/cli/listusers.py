"""
Based on input connection parameters, this main function prints out all users.
"""

from cspybase.services.user.access import CsPyUserAccess
from cspybase.cli.core import create_connection


def main():
    """
    Main function
    """
    connection = create_connection()
    access = CsPyUserAccess(connection)
    users = access.get_users()
    for u in users:
        print(u)
    connection.disconnect()
