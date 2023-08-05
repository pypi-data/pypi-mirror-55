"""
Package for writting dummy csv file in a project
"""

import csv

from cspybase.cli.core import create_connection
from cspybase.cli.core import choose_project_name
from cspybase.services.project.access import CsPyProjectAccess


def main():
    """
    Main function
    """
    connection = create_connection()
    access = CsPyProjectAccess(connection);
    projectname = choose_project_name()
    project = access.get_project(projectname)
    rootdir = project.get_root()
    csvfile = rootdir.open_file("teste.csv", "wt")
    spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
    spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
    csvfile.close()

    connection.disconnect()
