import os
import pyodbc as py

def getStudyRegions():
    """Gets all study region names imported into your local Hazus install

    Returns:
        studyRegions: list -- study region names
    """
    comp_name = os.environ['COMPUTERNAME']
    c = py.connect('Driver=ODBC Driver 11 for SQL Server;SERVER=' +
        comp_name + '\HAZUSPLUSSRVR; UID=SA;PWD=Gohazusplus_02')
    exclusionRows = ['master', 'tempdb', 'model', 'msdb', 'syHazus', 'CDMS', 'flTmpDB']
    cursor = c.cursor()
    cursor.execute('SELECT [StateID] FROM [syHazus].[dbo].[syState]')   
    for state in cursor:
        exclusionRows.append(state[0])
    cursor = c.cursor()
    cursor.execute('SELECT * FROM sys.databases')
    studyRegions = []
    for row in cursor:
        if row[0] not in exclusionRows:
            studyRegions.append(row[0])
    studyRegions.sort(key=lambda x: x.lower())
    return studyRegions