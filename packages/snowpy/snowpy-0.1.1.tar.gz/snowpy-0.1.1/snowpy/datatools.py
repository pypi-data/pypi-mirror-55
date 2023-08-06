# -*- coding: utf-8 -*-
"""
SnowPy - A Python library to upload and doownload data from database systems
===============================================================================
- SnowPy data tools (datatools)
'SnowPy' was intially realsed as data tools for the mltoolkit project (https://mltoolkit.github.io/MLToolKit).

Author
------
- Sumudu Tennakoon

License
-------
- Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

Created Date
----------
- Sat Sep 28 2019

"""

from timeit import default_timer as timer
import gc
import socket
import getpass
import traceback
import sys
import os
import shutil
import csv
import pandas as pd
import numpy as np
import urllib
import sqlalchemy

try:
    import snowflake.connector
    from snowflake.sqlalchemy import URL
except:
    print("Error loading 'snowflake' library. Snowflake suppport disabled")

def execute_snowflake_sql_query(query, server=None, database=None, auth=None, schema=None, 
                                warehouse=None, on_error='ignore', return_time=False):         
    """
    Parameters
    ----------
    query : str
        SQL SELECT query
    server : str
        Database Server
    database : str
        Database
    auth :  dict
        e.g. auth = {'type':'user', 'user':'user', 'password':'password'} for username password authentication
             auth = {'type':'machine', 'uid':None, 'pwd':None} for machine authentication
    schema : str 
    warehouse : str
           
    Returns
    -------
    None
    """    
    
    engine = sqlalchemy.create_engine(URL(
        account = server,
        user = auth['user'],
        password = auth['password'],
        database = database,
        schema = schema,
        warehouse = warehouse,
        role = auth['role'],
    ))  
    
    try:   
        with engine.connect() as connection:
            start_time = timer() 
            connection.execute(query)
            execute_time = timer() - start_time
            print('Execute Time:', execute_time) 
            rowcount = None # need to add return value for affected rows
    except:
        execute_time = None
        rowcount = None
        
    if return_time:
        return rowcount, execute_time
    else:
        return rowcount  

                          
def read_data_snowflake(query, server=None, database=None, auth=None, schema=None, warehouse=None, 
                        date_columns=None, chunksize=None, method='pandas', on_error='ignore', return_time=False):
    """
    Parameters
    ----------
    query : str
        SQL query
    server : str
    database : str 
    auth :  dict
        e.g. auth = {'type':'user', 'user':'user', 'password':'password'} for username password authentication
             auth = {'type':'machine', 'uid':None, 'pwd':None} for machine authentication
    schema : str
    warehouse : str
    date_columns : list(str)
    chunksize : int
    method : str  
    
    Returns
    -------
    DataFrame : pandas.DataFrame
    """    
    
    execute_time = None
    
    engine = sqlalchemy.create_engine(URL(
        account = server,
        user = auth['user'],
        password = auth['password'],
        database = database,
        schema = schema,
        warehouse = warehouse,
        role = auth['role'],
    ))  
    
    try:
        with engine.connect() as connection:
            start_time = timer()
            if method == 'pandas':
                DataFrame = pd.read_sql(query, con=connection, parse_dates=date_columns, chunksize=chunksize)
            
            execute_time = timer() - start_time
            print('Data Load Time:', execute_time)  
    except:
        DataFrame = pd.DataFrame()
        
    if return_time:
        return DataFrame, execute_time
    else:
        return DataFrame           
    
def write_data_snowflake(DataFrame, server=None, database=None, auth=None, schema=None, table=None, columns=None, 
                         warehouse=None, index=False, if_exists='fail', chunksize=None, dtype=None, insertion_method='multi', 
                         temp_file_path='', dataset_label=None,  method='pandas', on_error='ignore', return_time=False):
    """
    Parameters
    ----------
    DataFrame : pandas.DataFrame
    server : str
        Database Server
    database : str
        Database
    auth :  dict
        e.g. auth = {'type':'user', 'user':'user', 'password':'password'} for username password authentication
             auth = {'type':'machine', 'uid':None, 'pwd':None} for machine authentication
    schema : str    
    table : str
    columns : list(str)
    warehouse : str
    index : bool
    if_exists : {'fail', 'append', 'replace'}, default 'fail'
    chunksize : int
    dtype : list(str)
    insertion_method : str, default 'multi'
    temp_file_path : str
    dataset_label : str
    method : {'pandas|'bulk'} 
    on_error : {None, 'ignore', 'raise'}, default 'ignore'
    return_time : bool
    
    Returns
    -------
    None
    """   
    
    if columns!=None:
        DataFrame = DataFrame[columns]
        
    column_names = DataFrame.columns    
    column_numbers = np.arange(len(column_names))+1
    
    COLUMN_NAME_LIST = ','.join(column_names.str.upper().values)
    COLUMN_NUMBERS_LIST = ','.join(['${}'.format(n) for n in column_numbers])
    
    engine = sqlalchemy.create_engine(URL(
        account = server,
        user = auth['user'],
        password = auth['password'],
        database = database,
        schema = schema,
        #warehouse = warehouse,
        role = auth['role'],
    ))  
    
    rowcount = None
    execute_time = None
            
    try:    
        with engine.connect() as connection:
            start_time = timer()        
            use_warehouse_command = """
            USE WAREHOUSE {warehouse};
            """.format(warehouse=warehouse)
            
            suspend_warehouse_command = """
            ALTER WAREHOUSE IF EXISTS {warehouse} SUSPEND;
            """.format(warehouse=warehouse)
            
            if method == 'pandas':
                connection.execute(use_warehouse_command)
                DataFrame.to_sql(table, con=connection, schema=schema, if_exists=if_exists, index=index, 
                                 dtype=dtype, method=insertion_method, chunksize=chunksize)
                connection.execute(suspend_warehouse_command)
            elif method == 'bulk':
                DataFrame.to_csv(temp_file_path, index=False, header=False, quoting=csv.QUOTE_ALL)
                
                stage_name = 'snowpy_stage_2019'
                file_format_name = 'snowpy_file_format'
                
                file_format_command = """
                CREATE OR REPLACE FILE FORMAT {file_format_name}
                TYPE = CSV
                FIELD_OPTIONALLY_ENCLOSED_BY ='"'
                FIELD_DELIMITER = ','
                SKIP_HEADER = 0
                NULL_IF = ('');
                """.format(file_format_name=file_format_name)
                
                stage_create_command = """
                CREATE OR REPLACE STAGE {stage_name}
                FILE_FORMAT = {file_format_name};            
                """.format(file_format_name=file_format_name, stage_name=stage_name)
            
                stage_drop_command = """
                DROP STAGE {stage_name};
                """.format(stage_name=stage_name)
    
                file_upload_command = """
                PUT file://{temp_file_path} @{stage_name}
                PARALLEL = 32;
                """.format(temp_file_path=temp_file_path, stage_name=stage_name)
    
                insert_command = r"""
                COPY INTO {table} ({COLUMN_NAME_LIST})
                FROM (
                  SELECT {COLUMN_NUMBERS_LIST}
                  FROM @{stage_name}/{table_name}.csv.gz t
                )
                PURGE = TRUE;
                """.format(table=table, stage_name=stage_name,
                COLUMN_NAME_LIST=COLUMN_NAME_LIST,
                COLUMN_NUMBERS_LIST=COLUMN_NUMBERS_LIST
                )
                
                connection.execute(stage_create_command)
                connection.execute(file_format_command)
                connection.execute(file_upload_command)
                #
                connection.execute(use_warehouse_command)          
                connection.execute(insert_command)
                connection.execute(stage_drop_command)
                connection.execute(suspend_warehouse_command)
                
            rowcount = DataFrame.shape[0]            
            execute_time = timer() - start_time
            print('data write time:', execute_time)  

    except:
        execute_time = None
        rowcount = None
        
    if return_time:
        return rowcount, execute_time
    else:
        return rowcount 
    
def execute_mssql_query(query=None, server=None, database=None, auth=None, driver='ODBC Driver 13 for SQL Server', 
                         on_error='ignore', return_time=False, params=None):
    """
    Parameters
    ----------
    query : str
        SQL SELECT query
    server : str
        Database Server
    database : str
        Database
    auth :  dict
        e.g. auth = {'type':'user', 'user':'user', 'password':'password'} for username password authentication
             auth = {'type':'machine', 'uid':None, 'pwd':None} for machine authentication
    params : dict
        extra parameters (not implemented)
    driver : str, default 'ODBC Driver 13 for SQL Server'
        E.g.: 'ODBC Driver 13 for SQL Server', 'ODBC Driver 17 for SQL Server', 'SQL Server'
    on_error : {None, 'ignore', 'raise'}, default 'ignore'
    return_time : bool
        
    Returns
    -------
    DataFrame : pandas.DataFrame
    """        
        
    # Download ODBC Driver https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
    # 'SQL Server' # 
    autocommit = 'True'
    fast_executemany = True
    
    if server!=None and  database!=None and query!=None and auth!=None :
        try:
            if auth['type']=='machine':
                connect_string = r'Driver={'+driver+'};SERVER='+server+';DATABASE='+database+';TRUSTED_CONNECTION=yes;autocommit='+autocommit+';'
                connect_string = urllib.parse.quote_plus(connect_string)
                
            elif auth['type']=='user':
                user =  auth['user'] 
                password =  auth['password'] 
                connect_string = r'Driver={'+driver+'};SERVER='+server+';DATABASE='+database+';UID='+user+'r;PWD='+password+'; autocommit='+autocommit+';'
                connect_string = urllib.parse.quote_plus(connect_string)
            else:
                raise Exception('No db server authentication method provided !')
            
            engine = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect="+connect_string, fast_executemany=fast_executemany)
            
            # connection
            connection = engine.connect()
            
            #transaction
            trans = connection.begin()
        
            # execute
            start_time = timer() 
            result = connection.execute(query)
            execute_time = timer() - start_time
            
            try:
                rowcount = result.rowcount
                print('{} rows affected. execute time = {} s'.format(rowcount,execute_time))
            except:
                rowcount = -1
                print('ERROR in fetching affected rows count. execute time = {} s'.format(execute_time))
                
            # commit
            trans.commit()
        
            # close connections, results set and dispose engine (moved to finally)
            #connection.close()
            #result.close()
            #engine.dispose()
        except:
            print(r'ERROR: Check If ODBC driver installed. \nIf not, Download ODBC Driver from https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server:\n{}\n'.format(traceback.format_exc()))
            rowcount = None
            execute_time = None
        finally:
            # close connections, results set and dispose engine
            try:
                connection.close()
            except:
                print('Failed to close connection !')
            try:
                result.close()
            except:
                print('Failed to close results !')
            try:
                engine.dispose()
            except:
                print('Failed to dispose engine !')
    else:
        execute_time = None
        rowcount = None 
        
    if return_time:
        return rowcount, execute_time
    else:
        return rowcount     

    
def read_data_mssql(query=None, server=None, database=None, auth=None, driver='SQL Server',  
                    on_error='ignore', return_time=False, params=None):
    """
    Parameters
    ----------
    query : str
        SQL SELECT query
    server : str
        Database Server
    database : str
        Database
    auth :  dict
        e.g. auth = {'type':'user', 'user':'user', 'password':'password'} for username password authentication
             auth = {'type':'machine', 'uid':None, 'pwd':None} for machine authentication
    driver : str, default 'ODBC Driver 13 for SQL Server'
        E.g.: 'ODBC Driver 13 for SQL Server', 'ODBC Driver 17 for SQL Server', 'SQL Server'
    on_error : {None, 'ignore', 'raise'}, default 'ignore'
    return_time : bool
    
    Returns
    -------
    DataFrame : pandas.DataFrame
    """   
    # Download ODBC Driver https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
        
    autocommit = 'True'
    fast_executemany = True
    execute_time = None

    if server!=None and  database!=None and auth!=None : 
        coerce_float=True
        index_col=None
        parse_dates=None
        
        try:
            if auth['type']=='machine':
                #connect_string = r'Driver={SQL Server};SERVER='+server+';DATABASE='+database+';TRUSTED_CONNECTION=yes;' #ODBC (slow)
                connect_string = r'Driver={'+driver+'};SERVER='+server+';DATABASE='+database+';TRUSTED_CONNECTION=yes;autocommit='+autocommit+';'
                connect_string = urllib.parse.quote_plus(connect_string)
            elif auth['type']=='user':
                user =  auth['user'] 
                password =  auth['password'] 
                #connect_string = r'Driver={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+uid+'r;PWD='+pwd+'}' #ODBC (slow)
                connect_string = r'Driver={'+driver+'};SERVER='+server+';DATABASE='+database+';UID='+user+'r;PWD='+password+'; autocommit='+autocommit+';'
                connect_string = urllib.parse.quote_plus(connect_string)
            else:
                raise Exception('No db server authentication method provided !') 
                
            #connection = pyodbc.connect(connect_string) #ODBC (slow)
            engine = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect="+connect_string, fast_executemany=fast_executemany)
            connection = engine
            
            start_time = timer() 
            DataFrame = pd.read_sql_query(sql=query, con=connection, coerce_float=coerce_float, index_col=index_col, parse_dates=parse_dates)
            execute_time = timer() - start_time
            
            #connection.close() 
            engine.dispose()
        except:
            print('Database Query Failed! Check If ODBC driver installed. \nIf not, Download ODBC Driver from https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-serve.:\n{}\n'.format(traceback.format_exc()))
            execute_time = None
    else:
        print('Check the destiniation table path (server, database, schema, table, auth) !')
        DataFrame=pd.DataFrame()
        execute_time = None
        
    print('{:,d} records were loaded. execute time = {} s'.format(len(DataFrame.index), execute_time))

    if return_time:
        return DataFrame, execute_time
    else:
        return DataFrame


def write_data_mssql(DataFrame, server=None, database=None, schema=None, table=None, index=False, 
                     dtypes=None, if_exists='fail', auth=None, insertion_method=None, chunksize=None,
                     driver='ODBC Driver 13 for SQL Server', on_error='ignore', return_time=False, params=None):
    """
    https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html
    
    Parameters
    ----------
    DataFrame : pandas.DataFrame
        DataFrame
    server : str
        Database Server
    database : str
        Database
    schema : str
        Database Schema
    table : str
        Table name
    if_exists : {'fail', 'replace', 'append'}, default 'fail'
        Action if the table already exists.
    auth :  dict
        e.g. auth = {'type':'user', 'user':'user', 'password':'password'} for username password authentication
             auth = {'type':'machine', 'uid':None, 'pwd':None} for machine authentication
    insertion_method : {None, 'multi', callable}
        see https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html
    driver : str, default 'ODBC Driver 13 for SQL Server'
        E.g.: 'ODBC Driver 13 for SQL Server', 'ODBC Driver 17 for SQL Server', 'SQL Server'
    on_error : {None, 'ignore', 'raise'}, default 'ignore'
    return_time : bool
    
    Returns
    -------
    None
    """ 
    
    # Download ODBC Driver https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
        
    autocommit = 'True'
    fast_executemany = True
    
    if server!=None and  database!=None and schema!=None and table!=None and auth!=None : 
        try:
            if auth['type']=='machine':
                connect_string = r'Driver={'+driver+'};SERVER='+server+';DATABASE='+database+';TRUSTED_CONNECTION=yes;autocommit='+autocommit+';'
                connect_string = urllib.parse.quote_plus(connect_string)
            elif auth['type']=='user':
                user =  auth['user'] 
                password =  auth['password'] 
                connect_string = r'Driver={'+driver+'};SERVER='+server+';DATABASE='+database+';UID='+user+'r;PWD='+password+'; autocommit='+autocommit+';'
                connect_string = urllib.parse.quote_plus(connect_string)
            else:
                raise Exception('No db server authentication method provided !') 
                
            #connection = pyodbc.connect(connect_string) #ODBC (slow)
            engine = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect="+connect_string, fast_executemany=fast_executemany)
            connection = engine
            
            start_time = timer() 
            if dtypes==None:
                DataFrame.to_sql(name=table, con=connection, schema=schema, index= index, if_exists=if_exists, method=insertion_method)
            else:
                DataFrame.to_sql(name=table, con=connection, schema=schema, index= index, dtype=dtypes, if_exists=if_exists, method=insertion_method)
            execute_time = timer() - start_time
            
            #connection.close() 
            engine.dispose()
            rowcount = len(DataFrame.index)
        except:
            print('Database Query Failed! Check If ODBC driver installed. \nIf not, Download ODBC Driver from https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-serve.:\n{}\n'.format(traceback.format_exc()))
            rowcount = None
            execute_time = None
    else:
        print('Check the destiniation table path (server, database, schema, table, auth) !')
        rowcount = None
        execute_time = None
    
    print('{:,d} records were written. execute time = {} s'.format(rowcount, execute_time))
    
    if return_time:
        return rowcount, execute_time
    else:
        return rowcount

def read_data_csv(file, separator=',', quoting= 'MINIMAL', compression='infer', encoding='utf-8', 
                  on_error='ignore', return_time=False):
    """
    https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_csv.html
    
    Parameters
    ----------    
    file : str
    separator : str
    index : bool
    compression : {'infer', 'gzip', 'bz2', 'zip', 'xz', None}, default 'infer'
    quoting : {'ALL', MINIMAL', 'NONNUMERIC', 'NONE'}, default 'MINIMAL'
    encoding : {'utf-8', 'utf-16'}, default 'utf-8'
    on_error : {None, 'ignore', 'raise'}, default 'ignore'
    return_time : bool
     
    Returns
    -------
    DataFrame : pandas.DataFrame
    """
    if quoting=='ALL':
        quoting = csv.QUOTE_ALL
    elif quoting=='MINIMAL':
        quoting = csv.QUOTE_MINIMAL        
    elif quoting=='NONNUMERIC':
        quoting = csv.QUOTE_NONNUMERIC        
    elif quoting=='NONE':
        quoting = csv.QUOTE_NONE   
    
    try:
        start_time = timer() 
        DataFrame = pd.read_csv(filepath_or_buffer=file, sep=separator, quoting=quoting, 
                                compression=compression, encoding=encoding)  
        execute_time = timer() - start_time
    except:
        execute_time = None
        DataFrame = pd.DataFrame()
        print(traceback.format_exc())
        
    print('{:,d} records were loaded. execute time = {} s'.format(len(DataFrame.index), execute_time))
    
    if return_time:
        return DataFrame, execute_time
    else:
        return DataFrame

def write_data_csv(DataFrame, file, separator=',', index=False, quoting='ALL', encoding='utf-8', 
                   compression='infer', chunksize=None, on_error='ignore', return_time=False):
    """
    https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_csv.html
    
    Parameters
    ----------    
    DataFrame : pandas.DataFrame
    file : str
    separator : str
    index : bool
    compression : {'infer', 'gzip', 'bz2', 'zip', 'xz', None}, default 'infer'
    quoting : {'ALL', MINIMAL', 'NONNUMERIC', 'NONE'}, default 'MINIMAL'
    encoding : {'utf-8', 'utf-16'}, default 'utf-8'
    chunksize : int, default None
    on_error : {None, 'ignore', 'raise'}, default 'ignore'
    return_time : bool
    
    Returns
    -------
    None
    """
    
    if quoting=='ALL':
        quoting = csv.QUOTE_ALL
    elif quoting=='MINIMAL':
        quoting = csv.QUOTE_MINIMAL        
    elif quoting=='NONNUMERIC':
        quoting = csv.QUOTE_NONNUMERIC        
    elif quoting=='NONE':
        quoting = csv.QUOTE_NONE        
    try:
        start_time = timer()     
        DataFrame.to_csv(path_or_buf=file, sep=separator, encoding=encoding, index=index, 
                         quoting=quoting, compression=compression, chunksize=chunksize)
        execute_time = timer() - start_time
        rowcount = DataFrame.shape[0]
    except:
        execute_time = 0
        print(traceback.format_exc())
        rowcount = None
        
    print('{:,d} records were written. execute time = {} s'.format(len(DataFrame.index), execute_time))
    
    
    
    if return_time:
        return rowcount, execute_time
    else:
        return rowcount
