from pandas import DataFrame, merge

from data.variables import APPLN_NUMBER_COLNAME, JOIN_WARNING


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
        return df_pers_data.copy()

    @staticmethod
    def merge_dfs(general_df, personal_df, need_preprocess_pers_data=False) -> DataFrame:
        if need_preprocess_pers_data:
            df_pers_data = DataManager.preprocess_personal_df(personal_df)
        else:
            df_pers_data = personal_df
        appl_df = general_df.copy()
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
    data_manager = DataManager()
