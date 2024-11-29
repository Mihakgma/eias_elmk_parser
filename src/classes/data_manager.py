from pandas import DataFrame, merge, concat
from os import path as os_path
from os import makedirs as os_makedirs
from os import listdir as os_listdir
from os import chdir as os_chdir
from json import load as json_load
from json import dump as json_dump

from data.variables import APPLN_NUMBER_COLNAME, JOIN_WARNING, TEMP_XLSX_FILENAME, LOGS_DIR, NAVIGATOR_SERIALIZE_FILE, \
    FILIAL_COLNAME, REGISTR_ADRESS_DICT, FACT_ADRESS_DICT
from functions import excel_to_data_frame_parser, printDimensionsOfDF, get_filial_name


class DataManager:
    """
    This class helps to process DFs from navigation class
    for example it performs merging DFs with
    general (left part) and personal (right part) info,
    contains static methods for doing these operations.
    """

    @staticmethod
    def preprocess_personal_df(personal_df) -> DataFrame:
        df_pers_data = DataFrame.from_dict(personal_df).T.reset_index()
        df_pers_data.rename({'index': APPLN_NUMBER_COLNAME}, axis='columns', inplace=True)
        df_pers_data[APPLN_NUMBER_COLNAME] = df_pers_data[APPLN_NUMBER_COLNAME]\
                                                         .apply(lambda x: int(x))
        return df_pers_data.copy()

    @staticmethod
    def merge_dfs_automatically(right_df_key_name: str = "__right_df_dict") -> tuple:
        left_df = excel_to_data_frame_parser(file=TEMP_XLSX_FILENAME,
                                             sheet_name="Sheet1",
                                             rows_to_skip=0,
                                             blank_values_drop=0,
                                             first_row_header=0)
        printDimensionsOfDF(dfInput=left_df,
                            warnStr="downloading left DF from excel", )
        navigators_fields_values = DataManager.get_json_values()
        if right_df_key_name not in navigators_fields_values:
            raise KeyError(f"Key {right_df_key_name} not found in navigators fields")
        right_df = navigators_fields_values[right_df_key_name]
        right_df = DataManager.preprocess_personal_df(right_df)
        df = DataManager.merge_dfs(general_df=left_df,
                                   personal_df=right_df,
                                   need_preprocess_pers_data=False)
        return df, left_df, right_df

    @staticmethod
    def merge_dfs(general_df, personal_df, need_preprocess_pers_data=False) -> DataFrame:
        if need_preprocess_pers_data:
            df_pers_data = DataManager.preprocess_personal_df(personal_df)
        else:
            df_pers_data = personal_df
        appl_df = general_df.copy()
        try:
            df_merged = merge(appl_df,
                              df_pers_data,
                              on=APPLN_NUMBER_COLNAME,
                              how='left')
        except ValueError as ve:
            print(ve)
            df_merged = concat([appl_df, personal_df],
                               axis=1,
                               ignore_index=True,
                               keys=[APPLN_NUMBER_COLNAME])
        rows_equal = appl_df.shape[0] == df_pers_data.shape[0]
        join_warn = JOIN_WARNING[rows_equal]
        print(join_warn)
        if not rows_equal:
            open_table_name = 'ОТКРЫТАЯ ТАБЛИЦА'
            personal_data_table = 'ТАБЛИЦА по ПЕРСОНАЛЬНЫМ ДАННЫМ (скрытая)'
            print(f'\nРазмерность ДФ из <{open_table_name}> составила: <{appl_df.shape}>')
            print(f'\nРазмерность ДФ, из <{personal_data_table}> составила: <{df_pers_data.shape}>')
            print('\nПо всей видимости не доПарсено следующее количество строк')
            print(f'<{abs(appl_df.shape[0] - df_pers_data.shape[0])}> из ДФ:')
            print([
                      open_table_name,
                      personal_data_table
                  ][appl_df.shape[0] > df_pers_data.shape[0]])
            print()
        print(df_merged.shape)
        df_merged[FILIAL_COLNAME] = get_filial_name(first_lst_in=df_merged[REGISTR_ADRESS_DICT].to_list(),
                                                    second_lst_in=df_merged[FACT_ADRESS_DICT].to_list())
        # заменить пропущенные значения на пустые строки
        df_merged.fillna('', inplace=True)
        return df_merged

    @staticmethod
    def get_json_values():
        fullpath_json = DataManager.get_navigator_json_file_path()
        with open(fullpath_json, "r", encoding='utf-8') as f:
            json_values = json_load(f)
        return json_values

    @staticmethod
    def get_navigator_json_file_path():
        return os_path.join(LOGS_DIR, NAVIGATOR_SERIALIZE_FILE)

    @staticmethod
    def serialize_navigator_instance(data_to_serialize: dict):
        try:
            fullpath_json = DataManager.get_navigator_json_file_path()
            os_makedirs(LOGS_DIR, exist_ok=True)
            with open(fullpath_json, "w", encoding='utf-8') as f:
                json_dump(data_to_serialize, f, indent=4)
            print(f"Navigator data SERIALIZED successfully to <{NAVIGATOR_SERIALIZE_FILE}>")
        except Exception as exception:
            print(f"Error during serialization: {exception}")


if __name__ == '__main__':
    cwd = "../LOGS"
    try:
        os_chdir(cwd)
        print(os_listdir())
        DataManager.merge_dfs_automatically()
    except FileNotFoundError as e:
        print(e)
        print("probably need to change cwd to right dir...")
