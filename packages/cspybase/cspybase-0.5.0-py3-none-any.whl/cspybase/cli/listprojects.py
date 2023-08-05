"""
Based on input connection parameters, this main function prints out all user projects.
"""

from cspybase.services.project.access import CsPyProjectAccess
from cspybase.cli.core import create_connection


def main():
    """
    Main function
    """
    connection = create_connection()
    access = CsPyProjectAccess(connection)
    projects = access.get_projects()
    for p in projects:
        print(p)
    connection.disconnect()
