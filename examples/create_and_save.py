#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from os import makedirs as os_makedirs
from os import environ as os_environ

from pandas import DataFrame, ExcelWriter


# In[ ]:


def create_dir_save_table(df: DataFrame or dict,
                          excel_file_name:str='',
                          number_col_names:list=['НОМЕР'],
                          several_tables:bool=False,
                          excel_file_format:str='.xlsx',
                          folder_name:str='КОНТРОЛЬ_КОНТРАКТОВ',
                          get_just_folder_path:bool=False):
    """
    Если параметр several_tables = True, тогда
    сохраняем несколько ДФ в один Excel-файл на разных его страницах!
    """
    
    desktop_path = str(os_environ['USERPROFILE'] + '\Desktop')+f'\\{folder_name}\\'
    if get_just_folder_path:
        return(desktop_path)
    excel_filename = desktop_path + excel_file_name + excel_file_format
    
    # заменяем тип данных с целыми числами на строку для корректного сохранеия в Excel
    if len(number_col_names):
        for num_colname in number_col_names:
            df[num_colname] = df[num_colname].astype(str)
    try:
        os_makedirs(desktop_path)
    except:
        print(f'Папка с названием {folder_name} была ранее создана на Вашем рабочем столе!')
    # непосредственно само сохранение файла!
    # several_tables=True
    if several_tables:
        writer = ExcelWriter(excel_filename)
        counter = 0
        for contr_num in list(df):
            counter += 1
            temp_df = df[contr_num][0]
            if len(contr_num) > 15:
                contr_num = counter
            temp_df.to_excel(writer, f'{contr_num}', index=False)
        writer.save()
        return
    # several_tables=False - по умолчанию!
    df.to_excel(excel_filename, index=False)

