import requests
import json

BASE_IKUS = "https://ikus.pesc.ru/"

class PetroUser():
    """Класс пользователя, имеющего учетную запись в Петроэлектросбыт.
    В конструктор необходимо передать login_type (в моем случае = "PHONE"), логин и пароль"""
    def __init__(self, login_type, login, psw):
        self.login_type = login_type
        self.login = login
        self.psw = psw
        self.set_tokens() # установятся access_token и auth_token
        if self.access_token is not None:
            self.account_id = self.get_account_id()
            self.debt = self.get_debt()
            self.logout()
        else:
            self.debt = None


    def set_tokens(self): 
        """POST-запрос на получение авторизационной инфы (access+auth токены).
        Если залогиниться не удается, токены устанавливаются в None и в консоль выводится response от сервера.
        При логауте в payload нужно поместить оба токена"""
        url = BASE_IKUS + "api/v7/users/auth"

        payload = {"type": self.login_type, "login": self.login, "password": self.psw}
        response = requests.post(url, json=payload)
        response_dict = json.loads(response.text)

        # создаем соответствующие атрибуты класса с токенами (в случае успешного логина)
        try:
            self.access_token = response_dict["access"]
            self.auth_token = response_dict["auth"]
        except KeyError:
            print("Петроэлектросбыт: ", response_dict)
            self.access_token = None
            self.auth_token = None


    def get_account_id(self):
        """GET-запрос на получение account_id"""
        url = BASE_IKUS + "api/v8/accounts"
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        payload = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        response_dict = json.loads(response.text)

        # ищем id для ЕЛС (единого лицевого счета), а не ЛС, потому что нам нужна общая сумма
        if(response_dict[0]["tenancy"]["name"]["shorted"] == "ЕЛС"):
            return response_dict[0]["id"]
        else:
            return response_dict[1]["id"]
        

    def get_debt(self):
        """GET-запрос на получение суммы долга (сумма двух показателей)"""
        url = BASE_IKUS + f"api/v8/accounts/{self.account_id}/payments/bills/current"
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        payload = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        response_dict = json.loads(response.text)
        return response_dict["amount"]
    

    def logout(self):
        """DELETE-запрос на логаут (видимо удаление токена из БД)"""
        url = BASE_IKUS + "api/v6/users/auth"
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        payload = {"access": self.access_token, "auth": self.auth_token}
        #response = requests.request("DELETE", url, headers=headers, data=payload)
        response = requests.delete(url, json=payload, headers=headers)
        print(response.text)


