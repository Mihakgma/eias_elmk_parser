from data.variables import * # Лучше всего здесь импортировать только необходимые переменные, а не все *

def get_constants():
    COLNAMES_DICT = (
        WAIT_DICT,
        REGISTR_ADRESS_DICT,
        FACT_ADRESS_DICT,
        GENDER_DICT,
        TEL_NUMB_DICT,
        LAST_NAME_DICT,
        FIRST_NAME_DICT,
        MIDDLE_NAME_DICT,
        EMAIL_DICT,
        PASSPRT_NUMB_DICT,
        PASSPRT_DATE_DICT,
        PASSPRT_DEPT_DICT,
        PASSPRT_CODE_DICT)

    PERS_DATA_XPATH = {
        WAIT_XPATH: [0, 0],
        REGISTR_ADRESS_XPATH: [0, 0],
        FACT_ADRESS_XPATH: [0, 1],
        GENDER_XPATH: [1, 0],
        TEL_NUMB_XPATH: [0, 0],
        LAST_NAME_XPATH: [0, 0],
        FIRST_NAME_XPATH: [0, 0],
        MIDDLE_NAME_XPATH: [0, 0],
        EMAIL_XPATH: [0, 0],
        PASSPRT_NUMB_XPATH: [0, 0],
        PASSPRT_DATE_XPATH: [0, 0],
        PASSPRT_DEPT_XPATH: [0, 0],
        PASSPRT_CODE_XPATH: [0, 0]}
    return COLNAMES_DICT, PERS_DATA_XPATH

# Вызов функции get_constants() теперь после ее определения
COLNAMES_DICT, PERS_DATA_XPATH = get_constants()


if __name__ == "__main__":
    pass
