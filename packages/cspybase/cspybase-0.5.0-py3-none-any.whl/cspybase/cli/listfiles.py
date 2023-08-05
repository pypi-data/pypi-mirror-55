"""
Based on input connection parameters, this main function prints out all files on root project directory
"""

from cspybase.services.project.access import CsPyProjectAccess
from cspybase.cli.core import create_connection, choose_project_name


def main():
    """
    Main function
    """
    connection = create_connection()
    access = CsPyProjectAccess(connection)
    projectname = choose_project_name()
    if (projectname is None):
        connection.disconnect()
        return

    project = access.get_project(projectname)
    root = project.get_root()
    files = root.list()
    for f in files:
        print(f)
    connection.disconnect()
