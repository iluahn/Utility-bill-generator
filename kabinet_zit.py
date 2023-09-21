import requests
import json

BASE_KAB = "https://xn----7sbdqbfldlsq5dd8p.xn--p1ai/"

class KabZitUser():
    """Класс пользователя, имеющего учетную запись в Кабинет-жителя. 
    В конструктор необходимо передать логин (почтовый адрес) и пароль"""
    def __init__(self, username, psw):
        self.username = username
        self.psw = psw
        self.token = self.get_token()
        if self.token is not None:
            self.debt = self.get_amount()
            self.logout()


    def get_token(self):
        """POST-запрос: логинимся и получаем токен"""
        url = BASE_KAB + "api/v4/auth/login/"

        payload = {"username": self.username, "password": self.psw}
        headers = { }

        response = requests.request("POST", url, headers=headers, data=payload)
        response_dict = json.loads(response.text)
        try:
            token = response_dict["_token"]
            return token
        except KeyError:
            print("Кабинет-жителя.рф: ", response_dict)
            return None
        
    
    def get_amount(self):
        """"GET-запрос на получение информации о текущем долге"""
        url = BASE_KAB + "api/v4/cabinet/notices/?sectors=rent"
        payload = {}
        headers = {"Cookie": f"session_id={self.token}"}

        response = requests.request("GET", url, headers=headers, data=payload)
        response_dict = json.loads(response.text)
        debt = float(response_dict["debts"][0]["months"][0]["debt"]/100)
        return debt


    def logout(self):
        """Логаут с передачей токена (на бекенде он должен удаляться)"""
        url = BASE_KAB + "api/v4/auth/logout/"
        payload = {}
        headers = {"Cookie": f"session_id={self.token}"}

        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)



