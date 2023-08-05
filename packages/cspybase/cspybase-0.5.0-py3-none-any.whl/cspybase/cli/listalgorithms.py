"""
Based on input connection parameters, this main function prints all installed algorithms
"""

from cspybase.services.algorithm import CsPyAlgorithmAccess
from cspybase.cli.core import create_connection

def main():
    """Main function"""
    connection = create_connection()
    access = CsPyAlgorithmAccess(connection)
    algos = access.get_algorithms()
    for a in algos:
        print(a)
    connection.disconnect()
