from login_function import get_login_password

DRIVER_ARGUMENTS = [
    r"--user-data=C:\Users\tabakaev_mv\AppData\Local\Yandex\YandexBrowser\User Data\Default",
    "--disable-notifications"
]

BROWSER_FILE_PATH = "C:\\Program Files\\Yandex\\YandexBrowser\\Application\\browser.exe"
WEBDRIVER_PATH = "C:\\yandexdriver\\yandexdriver.exe"
HOME_URL = "https://eias.rospotrebnadzor.ru/"
ELMK_URL = "https://eias.rospotrebnadzor.ru/gov-services/elmks"
LOGIN_PASSWORD_FULLPATH = "C:\\Users\\tabakaev_mv\\Desktop\\РАБОТА\\ЕИАС\\2023\\ТОКСИКОМОНИТОРИНГ\\ПОДГРУЗКА\\application\\eias_pass.txt"
UPLOAD_LAN_DIR = "\\192.168.201.38\\общая папка\\06 ООДЦ\\Выгрузка_ЭЛМК\\"
# получаем логин и пароль для входа
LOGIN, PASSWORD = get_login_password(txt_file_path=LOGIN_PASSWORD_FULLPATH)
NUM_ROWS_MARK = 'Количество записей: '
TEMP_XLSX_FILENAME = "temp_xlsx_elmk_first_df.xlsx"

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

COLNAMES_DICT = (
    WAIT_DICT,
    REGISTR_ADRESS_DICT,
    # REGISTR_ADRESS_BUILDING_DICT,
    # REGISTR_ADRESS_FLAT_DICT,
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

# XPATHS!!!
LOGIN_XPATH = "/html/body/main/div/form/div[1]/input"
PASSWORD_XPATH = "/html/body/main/div/form/div[2]/input"
SUBMIT_PASS_XPATH = "/html/body/main/div/form/button"
# ---!!! personal data !!! ---# beginning
WAIT_XPATH = ""
# REGISTR_ADRESS_XPATH = "/html/body/app-root/nz-layout/nz-layout/nz-layout/div/app-elmk/div/div[3]/form/div[2]/app-address/div/div/div[1]/nz-form-item/nz-form-control/div/div/nz-input-group/input"
REGISTR_ADRESS_XPATH = "/html/body/app-root/nz-layout/nz-layout/nz-layout/div/app-elmk/div/div[3]/form/div[2]/div[7]/div/nz-form-item/nz-form-control/div/div/input"
REGISTR_ADRESS_BUILDING_XPATH = "/html/body/app-root/nz-layout/nz-layout/nz-layout/div/app-elmk/div/div[3]/form/div[2]/app-address/div/div/div[2]/nz-form-item/nz-form-control/div/div/nz-select/nz-select-top-control/nz-select-item"
REGISTR_ADRESS_FLAT_XPATH = "/html/body/app-root/nz-layout/nz-layout/nz-layout/div/app-elmk/div/div[3]/form/div[2]/app-address/div/div/div[3]/nz-form-item/nz-form-control/div/div/nz-input-group/input"
FACT_ADRESS_XPATH = "/html/body/app-root/nz-layout/nz-layout/nz-layout/div/app-elmk/div/div[3]/form/div[2]/div[7]/app-address/div/div/div[1]/nz-form-item/nz-form-control/div/div/nz-input-group/input"
FACT_ADRESS_XPATH = "/html/body/app-root/nz-layout/nz-layout/nz-layout/div/app-elmk/div/div[3]/form/div[2]/div[9]/div[2]/div/nz-form-item/nz-form-control/div/div/input"
GENDER_XPATH = "/html/body/app-root/nz-layout/nz-layout/nz-layout/div/app-elmk/div/div[3]/form/div[2]/div[3]/div[4]/nz-form-item/nz-form-control/div/div/app-select/div/nz-select/nz-select-top-control/nz-select-item"
TEL_NUMB_XPATH = "/html/body/app-root/nz-layout/nz-layout/nz-layout/div/app-elmk/div/div[3]/form/div[2]/div[3]/div[7]/nz-form-item/nz-form-control/div/div/input"
LAST_NAME_XPATH = "/html/body/app-root/nz-layout/nz-layout/nz-layout/div/app-elmk/div/div[3]/form/div[2]/div[3]/div[1]/nz-form-item/nz-form-control/div/div/input"
FIRST_NAME_XPATH = "/html/body/app-root/nz-layout/nz-layout/nz-layout/div/app-elmk/div/div[3]/form/div[2]/div[3]/div[2]/nz-form-item/nz-form-control/div/div/input"
MIDDLE_NAME_XPATH = "/html/body/app-root/nz-layout/nz-layout/nz-layout/div/app-elmk/div/div[3]/form/div[2]/div[3]/div[3]/nz-form-item/nz-form-control/div/div/input"
EMAIL_XPATH = "/html/body/app-root/nz-layout/nz-layout/nz-layout/div/app-elmk/div/div[3]/form/div[2]/div[3]/div[8]/nz-form-item/nz-form-control/div/div/input"
PASSPRT_NUMB_XPATH = "/html/body/app-root/nz-layout/nz-layout/nz-layout/div/app-elmk/div/div[3]/form/div[2]/div[4]/div[1]/nz-form-item/nz-form-control/div/div/input"
PASSPRT_DATE_XPATH = "/html/body/app-root/nz-layout/nz-layout/nz-layout/div/app-elmk/div/div[3]/form/div[2]/div[4]/div[2]/nz-form-item/nz-form-control/div/div/nz-date-picker/div/input"
PASSPRT_DEPT_XPATH = "/html/body/app-root/nz-layout/nz-layout/nz-layout/div/app-elmk/div/div[3]/form/div[2]/div[4]/div[3]/nz-form-item/nz-form-control/div/div/input"
PASSPRT_CODE_XPATH = "/html/body/app-root/nz-layout/nz-layout/nz-layout/div/app-elmk/div/div[3]/form/div[2]/div[4]/div[4]/nz-form-item/nz-form-control/div/div/input"

PERS_DATA_XPATH = {
    WAIT_XPATH: [0, 0],
    REGISTR_ADRESS_XPATH: [0, 0],
    # REGISTR_ADRESS_BUILDING_XPATH:[1,0],
    # REGISTR_ADRESS_FLAT_XPATH:[0,0],
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

# ---!!! personal data !!! ---# ends
DF_ROW_NUMS_XPATH = "//*[contains(text(), 'Количество записей: ')]"
DF_TABLE_SCROLL_XPATH = "/html/body/app-root/nz-layout/nz-layout/nz-layout/div/app-elmks/div/div[3]/app-table/nz-table/nz-spin/div/div/nz-table-inner-scroll/div[2]"
