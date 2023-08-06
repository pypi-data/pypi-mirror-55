import os
import pandas as pd
import urllib
import sqlalchemy
from tqdm import tqdm

def bulketl(filepath,filetype,server,table,overwrite=False):
    """
    Load all files in a given directory to specified SQL Server.
    Supports Excel, CSV, and TXT files
    For Excel files, assumes Sheet1

    Args:
        filepath(str): The filepath of the directory containing the files
        filetype(str): The extension of the files to grab (.xlsx, .csv, .txt).
        server(str): The name of the SQL Server to connect to
        table(str): The fully qualified (database.schema.table) table to write to
        overwrite(bool): Drop/recreate table (default False)
    """
    if filepath.endswith != '/':
        filepath += '/'
    
    files = []

    for file in os.listdir(filepath):
        if file.endswith(filetype):
            files.append(file)
    
    qualifiers = table.split('.')
    db = qualifiers[0]
    schema = qualifiers[1]
    tablename = qualifiers[2]

    params = urllib.request.quote("DRIVER={SQL Server Native Client 11.0};SERVER=%s;DATABASE=%s;trusted_connection=Yes" % (server,db))
    engine = sqlalchemy.create_engine(f"mssql+pyodbc:///?odbc_connect={params}", isolation_level='AUTOCOMMIT')

    if overwrite == True:
        with engine.connect() as con:
            con.execute(f"IF OBJECT_ID('{table}','U') IS NOT NULL DROP TABLE {table}")

    if filetype == '.xlsx':
        for file in tqdm(files):
            df = pd.read_excel(filepath+file,
                               dtype='object')
            df.to_sql(tablename,
                      con=engine,
                      schema=schema,
                      if_exists='append',
                      index=False)
    
    if filetype == '.csv' or filetype == '.txt':
        for file in tqdm(files):
            df = pd.read_csv(filepath+file,
                             delimiter=',',
                             dtype='str',
                             encoding='ANSI')
            df.to_sql(tablename,
                      con=engine,
                      schema=schema,
                      if_exists='append',
                      index=False)

