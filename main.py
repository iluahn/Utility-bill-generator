import os
from dotenv import load_dotenv
from kabinet_zit import KabZitUser
from petro import PetroUser


def append_to_file(debt, debt_name, file_path):
    """Запись долга в файл в соответствии с заданным форматом"""
    with open(file_path, 'a') as f:
        f.write(f"{debt} {debt_name}\n")


def generate_check(kab_user, petro_user, file_path):
    """Формирование чека. Разбито по категориям: ку, электричество и интернет (с фиксированной суммой 400). 
    В конце приводится итоговая сумма, которая считается только если получено оба значения долга (помимо интернета)"""
    open(file_path, "w").close()
    append_to_file(kab_user.debt, "ку", file_path)
    append_to_file(petro_user.debt, "электричество", file_path)
    append_to_file(400, "интернет", file_path)
    if(kab_user.debt is None or petro_user.debt is None):
        append_to_file("\nInfo:", "получена не вся информация, проверьте вывод консоли\n", file_path)
    else:
        append_to_file("\nИтого", str(kab_user.debt + petro_user.debt + 400) + "\n", file_path)



if __name__ == "__main__":
    """Создаем экземпляры классов пользователя Кабинет-жителя и Петроэлектросбыт. Необходимые атрибуты устанавливаются в конструкторе. 
    Если залогиниться не удается, атрибуты-токены будут установлены как None, а атрибут с долгом не будет установлен."""
    load_dotenv()
    kab_user = KabZitUser(os.environ.get("KABINET_LOGIN"), os.environ.get("KABINET_PSW"))
    petro_user = PetroUser(os.environ.get("PETRO_LOGINTYPE"), os.environ.get("PETRO_LOGIN"), os.environ.get("PETRO_PSW"))
    generate_check(kab_user, petro_user, os.environ.get("FILE_PATH"))
