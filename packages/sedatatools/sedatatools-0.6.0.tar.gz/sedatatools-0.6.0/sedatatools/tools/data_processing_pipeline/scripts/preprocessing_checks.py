"""
This script will take a path to raw data as a parameter and path to all geotypes and sumlevels file.
It will check if folder exits, if files exists as well.
It will check geo column (if exists and if is unique), and if there is no Geo column, check if there is any other column that is unique
"""


import pandas as pd
import sys
import os
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
from loguru import logger


def get_files_list(file_path):

    # check if path leads to directory and if folder is empty
    if not os.path.isdir(file_path):
        logger.info("Error: Source file doesn't exist on selected location: " + file_path + " !")

    items = os.listdir(file_path)
    lis_of_files = []

    for item in items:
        if item.endswith('csv'):
            lis_of_files.append(os.path.join(file_path, item))

    if not lis_of_files:
        logger.info("Folder is empty!")

    else:
        return lis_of_files


def merge_data_and_geo(data, geo_data):
    """

    :param data: table for processing
    :param geo_data: All geo types and sum levels
    :return: geo and data tables merged
    """
    try:
        original_file = pd.read_csv(data, dtype={'Geo': 'str'})
        merged_data = pd.merge(geo_data, original_file, on='Geo', how='left')
        return merged_data

    except Exception as e:
        print(e)


def validate_files_list(file_path, csv_file):
    """
    This function will
    :param file_path:
    :param csv_file:
    :return:
    """
    file_shape = []
    df_shape = csv_file.shape
    file_shape.extend([file_path])
    file_shape.extend(df_shape)

    return file_shape


def check_len_in_all_df(data_frame):
    """
    This function will check if all tables have same number of rows
    :param data_frame: shape of the data frame with number of rows and columns in each table
    :return:
    """
    cols = data_frame.drop_duplicates(subset='Num of cols')
    num_of_cols = cols.shape[0]
    if num_of_cols > 1:
        for cols in cols.iterrows():
            logger.info('Check file ' + cols[1]['File_name'] + ' Different number of columns ')
    else:
        logger.info('Number of columns is the same for all tables in folder')
    return cols


def get_info_about_data(table_num, data_dim):
    logger.info('Number of tables: ' + str(table_num))
    columns = data_dim['Num of cols'].values[0]
    rows = data_dim['Num of rows'].values[0]
    logger.info('Dimension of data: Number of Rows ' + str(columns) + ' Number of rows: ' + str(rows))


def check_unique_values(file_name, csv_file):
    """
    This function will check if Geo column exists, and if it is unique
    :param file_name: File name
    :param csv_file: Geo and data table merged
    :return:
    """

    tables_with_unique_cols = []
    unique_counter = 0
    for item in csv_file.iteritems():
        if 'Geo' in item[0] and not item[1].is_unique:
            logger.info('Error - Geo column is not unique in: ' + file_name)
        elif 'Geo' in item[0] and not item[1].is_unique:
            unique_counter = unique_counter + 1
        elif item[1].is_unique:
            unique_counter = unique_counter + 1

    if unique_counter == 0:
        logger.info('Error - there is no unique columns in file: ' + file_name)
    else:
        tables_with_unique_cols.append(file_name)

    return tables_with_unique_cols


def check_data_types(file_name, merged_file):
    df_columns = list(merged_file.columns)
    df_columns.append('file_name')
    data_types_dataframe = pd.DataFrame(columns=[df_columns])
    for merged_col in merged_file.columns:
        if is_numeric_dtype(merged_file[merged_col]):
            data_types_dataframe[merged_col] = [merged_file[merged_col].dtype]
        elif is_string_dtype(merged_file[merged_col]):
            data_types_dataframe[merged_col] = ['str']

    data_types_dataframe['file_name'] = file_name
    return data_types_dataframe


def check_encoding(file_name):
    import chardet
    rawdata = open(file_name, 'rb').read()
    result = chardet.detect(rawdata)
    charenc = result['encoding']

    return charenc


def preprocessor_checks(param):
    # if Path(config['variableDefinitionsPath']).exists():
    #     variable_definition = get_variable_descriptions_from_file(
    #         config['variableDefinitionsPath'],
    #     )
    # else:
    #     variable_definition = get_variable_descriptions_from_directory(
    #         config['variableDefinitionsPath'],
    #     )
    #
    # # check if there is proper number of columns in a file, maybe this could be moved to separate function?
    # for v in variable_definition.values():
    #     col_nr = len(v)
    #     if 0 > col_nr > 5:
    #         logger.info(
    #             'Number of columns in variable description file/s is not ok!',
    #         )
    #         sys.exit()
    #
    # col_nr_prev = [i for i in variable_definition.values()]
    # for i in variable_definition.values():
    #     if len(i) != len(max(col_nr_prev, key=len)):
    #         logger.info('Number of columns changes in the file!?')
    #         sys.exit()
    pass


if __name__ == '__main__':

    path = sys.argv[1]
    all_geo_types = pd.read_csv(sys.argv[2] + '/all_geotypes_and_sumlev.csv', dtype={'Geo': 'str'})

    tables_with_unique_columns = []
    files_list = get_files_list(path)
    table_shape = []
    data_types_df = pd.DataFrame()
    number_of_tables = 0

    for file in files_list:
        geo_and_data_merged = merge_data_and_geo(file, all_geo_types)
        shape = validate_files_list(file, geo_and_data_merged)
        table_shape.append(shape)
        tables_with_unique_columns.append(check_unique_values(file, geo_and_data_merged))
        data_types= check_data_types(file, geo_and_data_merged)
        data_types_df = data_types_df.append(data_types)
        logger.info(check_encoding(file))
        number_of_tables = number_of_tables+1

    for col in data_types_df.columns:
        drop_na_dataframe = data_types_df[col].dropna()
        if drop_na_dataframe.unique().size > 1:
            logger.info(str(col) + ' Contains different data type')  # add info about file name
        else:
            pass

    table_shape = pd.DataFrame(table_shape, columns=['File_name', 'Num of cols', 'Num of rows'])
    data_dimension = check_len_in_all_df(table_shape)
    get_info_about_data(number_of_tables, data_dimension)
