from data.variables import (WAIT_DICT,
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
                            PASSPRT_CODE_DICT, WAIT_XPATH, REGISTR_ADRESS_XPATH, FACT_ADRESS_XPATH, GENDER_XPATH,
                            TEL_NUMB_XPATH, LAST_NAME_XPATH, FIRST_NAME_XPATH, MIDDLE_NAME_XPATH, EMAIL_XPATH,
                            PASSPRT_NUMB_XPATH, PASSPRT_DATE_XPATH, PASSPRT_DEPT_XPATH, PASSPRT_CODE_XPATH)


class Constant:
    @staticmethod
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
