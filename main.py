from kabinet_zit import KabZitUser
from petro import PetroUser


FILE_PATH = "C:\\Users\\common.txt"

def append_to_file(debt, debt_name, file_path=FILE_PATH):
    with open(file_path, 'a') as f:
        f.write(f"{debt} {debt_name}\n")

if __name__ == "__main__":
    """Создаем экземпляры классов пользователя Кабинет-жителя и Петроэлектросбыт.
    Необходимые атрибуты (сумма долга) устанавливаются в конструкторе. Строки LOGIN и PASSWORD должны быть заменены"""
    kab_user = KabZitUser("LOGIN", "PASSWORD")
    petro_user = PetroUser("PHONE", "LOGIN", "PASSWORD")

    append_to_file(kab_user.debt, "ку")
    append_to_file(petro_user.debt, "электричество")
    append_to_file(400, "интернет")
    append_to_file("\nИтого", str(kab_user.debt + petro_user.debt + 400) + "\n")


