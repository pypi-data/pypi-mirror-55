"""
Based on input connection parameters, this main function prints out all jobs for a project
"""

from cspybase.services.job import CsPyJobAccess
from cspybase.services.project.access import CsPyProjectAccess
from cspybase.cli.core import create_connection, choose_project_name


def main():
    """
    Main function
    """
    connection = create_connection()
    prjaccess = CsPyProjectAccess(connection)
    projectname = choose_project_name()
    if projectname is None:
        connection.disconnect()
        return

    project = prjaccess.get_project(projectname)
    prjid = project.get_id()
    jobaccess = CsPyJobAccess(connection)
    jobs = jobaccess.get_jobs(prjid)
    for j in jobs:
        print(j)
    connection.disconnect()
