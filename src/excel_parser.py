from pandas import ExcelFile as pd_ExcelFile


def excel_to_data_frame_parser(file: str,
                               sheet_name: str,
                               rows_to_skip: int = 1,
                               blank_values_drop: int = 10,
                               first_row_header: int = 0):
    """
    Парсит эксель-файл с выбором листа по его названию (file).
    Пропускает заданное количество первых строк (rows_to_skip).
    Дропает строки в конце таблице с заданным колиеством (tail_rows_drop)
    Возвращает датафрейм (далее - ДФ) или фрейм данных (таблица с данными).
    Если что-то идет не так (не выполняется одно из условий),
    то возращает False.
    """

    try:
        file = file
    except BaseException:
        print("Ошибка ввода")
        input()
        return False
    data = pd_ExcelFile(file)
    book_sheet_names = data.sheet_names
    # print("Названия листов в книге: ")
    # print(book_sheet_names)
    no_yes = ['НЕТ', 'ДА'][sheet_name in book_sheet_names]
    print(f'Искомый лист присутствует в книге: <{no_yes}>')
    if no_yes == 'ДА':
        sheet_number = book_sheet_names.index(sheet_name)
        df = data.parse(book_sheet_names[sheet_number], skiprows=rows_to_skip, header=first_row_header)
        # print('ДФ успешно спарсен!')
        df_out = df.dropna(thresh=blank_values_drop).copy()
        return df_out
    else:
        return False


def printDimensionsOfDF(dfInput, warnStr: str = ''):
    dfDimsLst = dfInput.shape
    print('После проведения <' + warnStr + '>')
    print(f"""размерность ДФ составила: 
    <{dfDimsLst[0]}> строк на <{dfDimsLst[1]}> столбцов""")
