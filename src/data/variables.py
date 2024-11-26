from functions.login_function import get_login_password


START_KEY_WORD = "бачина"
DRIVER_ARGUMENTS = [
    r"--user-data=C:\Users\tabakaev_mv\AppData\Local\Yandex\YandexBrowser\User Data\Default",
    "--disable-notifications"
]


BROWSER_FILE_PATH = "C:\\Program Files\\Yandex\\YandexBrowser\\Application\\browser.exe"
WEBDRIVER_PATH = "C:\\yandexdriver\\yandexdriver.exe"
HOME_URL = "https://eias.rospotrebnadzor.ru/"
ELMK_URL = "https://eias.rospotrebnadzor.ru/gov-services/elmks"
LOGIN_PASSWORD_FULLPATH = ("C:\\Users\\tabakaev_mv\\Desktop\\РАБОТА\\ЕИАС\\2023"
                           "\\ТОКСИКОМОНИТОРИНГ\\ПОДГРУЗКА\\application\\eias_pass.txt")
UPLOAD_LAN_DIR = "\\192.168.201.38\\общая папка\\06 ООДЦ\\Выгрузка_ЭЛМК\\"
# получаем логин и пароль для входа
LOGIN, PASSWORD = get_login_password(txt_file_path=LOGIN_PASSWORD_FULLPATH)
NUM_ROWS_MARK = 'Количество записей: '
TEMP_XLSX_FILENAME = "temp_xlsx_elmk_first_df.xlsx"
LOGS_DIR = "LOGS"
NAVIGATOR_SERIALIZE_FILE = "navigator_data.json"
APPLICATIONS_NUMBERS_COUNTER_FILE = "applications_numbers_counter.json"

CERT_SCREEN_FILES = [
    r"C:\Users\tabakaev_mv\Desktop\РАБОТА\ЕИАС\2024\ЭЛМК\ELMK_screen_scans\cert_submit_window_1.bmp",
    r"C:\Users\tabakaev_mv\Desktop\РАБОТА\ЕИАС\2024\ЭЛМК\ELMK_screen_scans\cert_submit_window_2.bmp",
    r"C:\Users\tabakaev_mv\Desktop\РАБОТА\ЕИАС\2024\ЭЛМК\ELMK_screen_scans\cert_submit_window_3.bmp",
    r"C:\Users\tabakaev_mv\Desktop\РАБОТА\ЕИАС\2024\ЭЛМК\ELMK_screen_scans\cert_submit_window_4.bmp",
    r"C:\Users\tabakaev_mv\Desktop\РАБОТА\ЕИАС\2024\ЭЛМК\ELMK_screen_scans\cert_submit_window_5.bmp",
    ]
OK_CERT_SCREEN_FILE = r"C:\Users\tabakaev_mv\Desktop\РАБОТА\ЕИАС\2024\ЭЛМК\ELMK_screen_scans\OK_SUBMIT_SCAN_cert.png"

# выводы(print-ы) о проверках
NO_or_YES = ["НЕТ", "ДА"]
JOIN_WARNING = [
    "FULL INNER JOIN IS NOT COMPLETED!!!",
    "FULL INNER JOIN IS COMPLETED!!!"
]

# Наименования колонок в ИСХОДНОМ ДФ
APPLN_NUMBER_COLNAME = '№ заявления'

# НАИМЕНОВАНИЯ ПОЛЕЙ В СЛОВАРЕ СЛОВАРЕЙ
WAIT_DICT = "для_служебн_польз"
REGISTR_ADRESS_DICT = 'адрес_регистрации'
REGISTR_ADRESS_BUILDING_DICT = 'рег_ном_здания'
REGISTR_ADRESS_FLAT_DICT = 'рег_ном_квартиры'
FACT_ADRESS_DICT = 'адрес_фактический'
GENDER_DICT = 'пол'
TEL_NUMB_DICT = 'номер_телефона'
LAST_NAME_DICT = 'фамилия'
FIRST_NAME_DICT = 'имя'
MIDDLE_NAME_DICT = 'отчество'
EMAIL_DICT = 'е_майл'
PASSPRT_NUMB_DICT = 'паспорт_номер'
PASSPRT_DATE_DICT = 'паспорт_дата_выдачи'
PASSPRT_DEPT_DICT = 'паспорт_кем_выдан'
PASSPRT_CODE_DICT = 'паспорт_код_подразделения'

# в объединенном ДФ
FILIAL_COLNAME = 'филиал'


# XPATHS!!!
LOGIN_XPATH = "/html/body/main/div/form/div[1]/input"
PASSWORD_XPATH = "/html/body/main/div/form/div[2]/input"
SUBMIT_PASS_XPATH = "/html/body/main/div/form/button"
# ---!!! personal data !!! ---# beginning
WAIT_XPATH = ""
# REGISTR_ADRESS_XPATH = "/html/body/app-root/nz-layout/nz-layout/nz-layout/div/app-elmk/div/div[3]/form/div[2]/app-address/div/div/div[1]/nz-form-item/nz-form-control/div/div/nz-input-group/input"
REGISTR_ADRESS_XPATH = ("/html/body/app-root/nz-layout/nz-layout/nz-layout/div/app-elmk/div/div[3]/form/div[2]/div["
                        "7]/div/nz-form-item/nz-form-control/div/div/input")
REGISTR_ADRESS_BUILDING_XPATH = ("/html/body/app-root/nz-layout/nz-layout/nz-layout/div/app-elmk/div/div[3]/form/div["
                                 "2]/app-address/div/div/div["
                                 "2]/nz-form-item/nz-form-control/div/div/nz-select/nz-select-top-control/nz-select"
                                 "-item")
REGISTR_ADRESS_FLAT_XPATH = ("/html/body/app-root/nz-layout/nz-layout/nz-layout/div/app-elmk/div/div[3]/form/div["
                             "2]/app-address/div/div/div[3]/nz-form-item/nz-form-control/div/div/nz-input-group/input")
# FACT_ADRESS_XPATH = "/html/body/app-root/nz-layout/nz-layout/nz-layout/div/app-elmk/div/div[3]/form/div[2]/div[7]/app-address/div/div/div[1]/nz-form-item/nz-form-control/div/div/nz-input-group/input"
FACT_ADRESS_XPATH = ("/html/body/app-root/nz-layout/nz-layout/nz-layout/div/app-elmk/div/div[3]/form/div[2]/div["
                     "9]/div[2]/div/nz-form-item/nz-form-control/div/div/input")
GENDER_XPATH = ("/html/body/app-root/nz-layout/nz-layout/nz-layout/div/app-elmk/div/div[3]/form/div[2]/div[3]/div["
                "4]/nz-form-item/nz-form-control/div/div/app-select/div/nz-select/nz-select-top-control/nz-select-item")
TEL_NUMB_XPATH = ("/html/body/app-root/nz-layout/nz-layout/nz-layout/div/app-elmk/div/div[3]/form/div[2]/div[3]/div["
                  "7]/nz-form-item/nz-form-control/div/div/input")
LAST_NAME_XPATH = ("/html/body/app-root/nz-layout/nz-layout/nz-layout/div/app-elmk/div/div[3]/form/div[2]/div[3]/div["
                   "1]/nz-form-item/nz-form-control/div/div/input")
FIRST_NAME_XPATH = ("/html/body/app-root/nz-layout/nz-layout/nz-layout/div/app-elmk/div/div[3]/form/div[2]/div[3]/div["
                    "2]/nz-form-item/nz-form-control/div/div/input")
MIDDLE_NAME_XPATH = ("/html/body/app-root/nz-layout/nz-layout/nz-layout/div/app-elmk/div/div[3]/form/div[2]/div["
                     "3]/div[3]/nz-form-item/nz-form-control/div/div/input")
EMAIL_XPATH = ("/html/body/app-root/nz-layout/nz-layout/nz-layout/div/app-elmk/div/div[3]/form/div[2]/div[3]/div["
               "8]/nz-form-item/nz-form-control/div/div/input")
PASSPRT_NUMB_XPATH = ("/html/body/app-root/nz-layout/nz-layout/nz-layout/div/app-elmk/div/div[3]/form/div[2]/div["
                      "4]/div[1]/nz-form-item/nz-form-control/div/div/input")
PASSPRT_DATE_XPATH = ("/html/body/app-root/nz-layout/nz-layout/nz-layout/div/app-elmk/div/div[3]/form/div[2]/div["
                      "4]/div[2]/nz-form-item/nz-form-control/div/div/nz-date-picker/div/input")
PASSPRT_DEPT_XPATH = ("/html/body/app-root/nz-layout/nz-layout/nz-layout/div/app-elmk/div/div[3]/form/div[2]/div["
                      "4]/div[3]/nz-form-item/nz-form-control/div/div/input")
PASSPRT_CODE_XPATH = ("/html/body/app-root/nz-layout/nz-layout/nz-layout/div/app-elmk/div/div[3]/form/div[2]/div["
                      "4]/div[4]/nz-form-item/nz-form-control/div/div/input")
# XPATHS FOR GETTING PERSONAL DATA WITH FILTER HELP!
# FILTER_BUTTON_XPATH = "/html/body/app-root/nz-layout/nz-layout/nz-layout/div/app-elmks/div/div[2]/div[4]/a[1]/img[1]"
# or
FILTER_BUTTON_XPATH = "/html/body/app-root/nz-layout/nz-layout/nz-layout/div/app-elmks/div/div[2]/div[4]/a[1]"
FILTER_APPL_NUMBER_INPUT_XPATH = "/html/body/div/div/div/div/div/form/nz-form-item[1]/nz-form-control/div/div/input"
FILTER_APPL_SUBMIT_BUTTON_XPATH = "/html/body/div/div/div/div/div/form/div/div/button[1]"
# or
# FILTER_APPL_SUBMIT_BUTTON_XPATH ="/html/body/div/div/div/div/div/form/div/div/button[1]/span"

NOTIFICATION_CSSs = [
    ".class='ant-modal-close-x'",
    "class='ant-modal-close-x'",
    ".span[class='ant-modal-close-x']",
    "span[class='ant-modal-close-x']",
    ".button aria-label='Close'",
    "button aria-label='Close'"
]
NOTIFICATION_HEADER = "Внимание!"

# ---!!! personal data !!! ---# ends
DF_ROW_NUMS_XPATH = "//*[contains(text(), 'Количество записей: ')]"
DF_TABLE_SCROLL_XPATH = ("/html/body/app-root/nz-layout/nz-layout/nz-layout/div/app-elmks/div/div["
                         "3]/app-table/nz-table/nz-spin/div/div/nz-table-inner-scroll/div[2]")

NAVIGATOR_STATUS = {
        0: ["HAS_NOT_BEEN_INITIALIZED"],
        1: ["HAS_BEEN_INITIALIZED"],
        2: ["LOGGED_IN"],
        3: ["ENTERED_ELMK_PAGE"],
        4: ["LEFT_DF_HAS_BEEN_PARSED"],
        5: ["PARSING_PERSONAL_DATA"],
        6: ["STUCK_PARSING_PERSONAL_DATA"],
        7: ["KICKED_ON_MAIN_EIAS_PAGE"],
        8: ["KICKED_ON_CERTIFICATE_SUBMITTING_PAGE"],
        9: ["KICKED_OUT_OF_PORTAL"],
        10: ["ABORTED"],
        11: ["SERIALIZED"],
        12: ["DESERIALIZED"],
        14: ["APPLICATION_NUMBER_NOT_FOUND_BY_FILTER"],
        15: ["APPLICATION_NUMBER_FOUND_IN_DICT"],
        16: ["APPLICATION_VALUE_IS_NULL"],
        17: ["FILTER_WINDOW_IS_CLOSED_NOW"],
    }


COLNAMES_DICT = (
        WAIT_DICT[:],
        REGISTR_ADRESS_DICT[:],
        FACT_ADRESS_DICT[:],
        GENDER_DICT[:],
        TEL_NUMB_DICT[:],
        LAST_NAME_DICT[:],
        FIRST_NAME_DICT[:],
        MIDDLE_NAME_DICT[:],
        EMAIL_DICT[:],
        PASSPRT_NUMB_DICT[:],
        PASSPRT_DATE_DICT[:],
        PASSPRT_DEPT_DICT[:],
        PASSPRT_CODE_DICT[:])

PERS_DATA_XPATH = {
    WAIT_XPATH[:]: [0, 0],
    REGISTR_ADRESS_XPATH[:]: [0, 0],
    FACT_ADRESS_XPATH[:]: [0, 1],
    GENDER_XPATH[:]: [1, 0],
    TEL_NUMB_XPATH[:]: [0, 0],
    LAST_NAME_XPATH[:]: [0, 0],
    FIRST_NAME_XPATH[:]: [0, 0],
    MIDDLE_NAME_XPATH[:]: [0, 0],
    EMAIL_XPATH[:]: [0, 0],
    PASSPRT_NUMB_XPATH[:]: [0, 0],
    PASSPRT_DATE_XPATH[:]: [0, 0],
    PASSPRT_DEPT_XPATH[:]: [0, 0],
    PASSPRT_CODE_XPATH[:]: [0, 0]}
