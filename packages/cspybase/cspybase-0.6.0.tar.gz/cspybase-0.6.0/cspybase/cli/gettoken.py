"""
Based on input connection parameters, this main functions prints out a connection token.
"""

from cspybase.cli.core import create_connection


def main():
    """
    Main function
    """
    connection = create_connection()
    token = connection.get_token()
    print('Token', token)
    connection.disconnect()
