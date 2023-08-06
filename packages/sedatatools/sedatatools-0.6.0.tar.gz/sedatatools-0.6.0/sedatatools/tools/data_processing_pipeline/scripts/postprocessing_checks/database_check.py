"""
Postprocessing database check v0.01
For the doc part, please read it in C:\Projects\DataTeam\sedatatools\sedatatools\tools\data_processing_pipeline
\docs\Documentation_database_check_script.docx
"""
from sedatatools.tools.connectors import prime
import pyodbc
import pandas as pd
from loguru import logger


def connect_to_db():
    """
    connect to database
    :return: connection
    """

    prime_conf = prime.Prime()
    user_name = prime_conf.user_name
    password = prime_conf.password

    conn = pyodbc.connect(
        'DRIVER={SQL Server};SERVER='+server+';DATABASE='+db_name+';UID='+user_name+';PWD='+password)

    return conn


def db_dtypes_uniqueness(connection):
    """
    Check if data types across all columns are unique
    :param connection: from connect_to_db() func
    :return: log if not unique
    """

    sql = "select cn from (select DATA_TYPE as dt, COLUMN_NAME as cn, TABLE_NAME from INFORMATION_SCHEMA.COLUMNS) " \
          "as new GROUP BY cn HAVING count(distinct(dt)) > 1"

    dtypes_format = pd.read_sql(sql, connection)

    logger.error(str(list(dtypes_format.cn))+' have no unique data type in sql database.')


def table_001_exists(connection):
    """
    Check if table 001 exists
    :param connection: from connect_to_db() func
    :return: log if no 001 table or no 001 for any summary level in db
    """

    sql_001 = "select distinct(TABLE_NAME) from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME like '%_001'"

    sql_fips = "select distinct(COLUMN_NAME) from INFORMATION_SCHEMA.COLUMNS where COLUMN_NAME like '%_FIPS'"

    table_001 = pd.read_sql(sql_001, connection)

    table_fips = pd.read_sql(sql_fips, connection)

    if len(table_001) < 1:
        logger.error("Tables 001 missing from the database. Table 001 contains info on geographic data. "
                     "Go back to the processing data and check why it didn't create 001 tables.")

    if len(table_001) > 1 and len(table_001) != len(table_fips):
        logger.error('No equal number of tables 001 and Summary level. Every Summary level has to have 001 table.')


def fips_names_in_sl(cursor, connection):
    """
    Check if all _FIPS and _NAMES column are present in all tables in db
    :param cursor: conn.cursor()
    :param connection: from connect_to_db() func
    :return: log in no _FIPS or _NAME column in any table in db
    """

    tables = "select * from table_names"

    number_of_tables = pd.read_sql(tables, connection)

    len_number_of_tables = len(number_of_tables)

    fips_name_in_all_tables = "select distinct(COLUMN_NAME), TABLE_NAME from INFORMATION_SCHEMA.COLUMNS " \
                              "where COLUMN_NAME like '%FIPS' or COLUMN_NAME like '%_NAME' and " \
                              "TABLE_NAME not like 'table_names'"

    df_fips_name_in_all_tables = pd.read_sql(fips_name_in_all_tables, connection)

    len_fips_name_in_all_tables = len(df_fips_name_in_all_tables)

    cursor.execute("select COUNT(distinct(COLUMN_NAME)) "
                   "from INFORMATION_SCHEMA.COLUMNS "
                   "where COLUMN_NAME like '%FIPS' or COLUMN_NAME like '%_NAME' and TABLE_NAME not like 'table_names'")
    number_of_unique_name_fips_cols = cursor.fetchone()[0]

    cursor.execute("select COUNT(distinct(SUBSTRING(TABLE_NAME,CHARINDEX('SL', TABLE_NAME), 5))) "
                   "from INFORMATION_SCHEMA.COLUMNS "
                   "where TABLE_NAME not like 'table_names'")

    number_of_summary_levels = cursor.fetchone()[0]

    if len_number_of_tables * number_of_summary_levels * number_of_unique_name_fips_cols != len_fips_name_in_all_tables:
        logger.error('Not all FIPS and NAMES variables are present in all tables.')


def fips_has_name(cursor):
    """
    Check if every _FIPS column has its own _NAME column (e.g. SL010_FIPS must have SL010_NAME column)
    :param cursor: conn.cursor()
    :return: log in no _FIPS column has its own _NAME column in any table in db
    """

    cursor.execute("select count(distinct(COLUMN_NAME)) "
                   "from INFORMATION_SCHEMA.COLUMNS "
                   "where COLUMN_NAME like '%_FIPS' and TABLE_NAME not like 'table_names'")
    len_fip_col = cursor.fetchone()[0]

    cursor.execute("select count(distinct(COLUMN_NAME)) "
                   "from INFORMATION_SCHEMA.COLUMNS "
                   "where COLUMN_NAME like '%_NAME' and TABLE_NAME not like 'table_names' "
                   "and COLUMN_NAME not like '%QNAME'")
    len_name_col = cursor.fetchone()[0]

    if len_fip_col != len_name_col:
        logger.error('FIPS and NAME tables are mismatched. '
                     'Check that all Summary level FIPS have its NAME column names.')


def main():
    conn = connect_to_db()
    curs = conn.cursor()
    db_dtypes_uniqueness(conn)
    table_001_exists(conn)
    fips_names_in_sl(curs, conn)
    fips_has_name(curs)


if __name__ == "__main__":
    server = 'PRIME\MSSQLSERVER3'
    db_name = 'TEST_DB'
    main()
