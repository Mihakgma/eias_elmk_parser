def get_login_password(txt_file_path: str):
    login = ''
    password = ''
    try:
        with open(txt_file_path) as file:
            lines = [line.rstrip() for line in file]
        login = lines[0]
        password = lines[1]
    except FileNotFoundError as e:
        print(e)
        print(f"default password is {password}")
        print(f"default login is {login}")
    return login, password
