from pandas import DataFrame, merge

from info import APPLN_NUMBER_COLNAME, JOIN_WARNING


class DataManager:
    """
    This class helps to process DFs from navigation class
    for example it performs merging DFs with
    general (left part) and personal (right part) info
    """
    def __init__(self,
                 general_df: DataFrame,
                 personal_data):
        self.__general_df = general_df
        self.__personal_df = personal_data
        self.__df_merged = None

    def preprocess_personal_df(self):
        df_pers_data = DataFrame.from_dict(self.__personal_df).T.reset_index()
        df_pers_data.rename({'index': APPLN_NUMBER_COLNAME}, axis='columns', inplace=True)
        self.__personal_df = df_pers_data.copy()

    def merge_dfs(self):
        self.preprocess_personal_df()
        appl_df = self.__general_df.copy()
        df_pers_data = self.__personal_df
        df_merged = merge(appl_df,
                          df_pers_data,
                          on=APPLN_NUMBER_COLNAME,
                          how='left')
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
        # заменить пропущенные значения на пустые строки
        df_merged.fillna('', inplace=True)
        return df_merged


if __name__ == '__main__':
    pass
