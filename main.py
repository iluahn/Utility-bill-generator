from kabinet_zit import KabZitUser
from petro import PetroUser


FILE_PATH = "C:\\Users\\common.txt"

def append_to_file(debt, debt_name, file_path):
    """Запись долга в файл в соответствии с заданным форматом"""
    with open(file_path, 'a') as f:
        f.write(f"{debt} {debt_name}\n")


def generate_check(kab_user, petro_user, file_path=FILE_PATH):
    """Формирование чека. Разбито по категориям: ку, электричество и интернет (с фиксированной суммой 400). 
    В конце приводится итоговая сумма, которая считается только если получено оба значения долга (помимо интернета)"""
    with open(file_path, 'wb'): 
        pass
    if(hasattr(kab_user, "debt")):
        append_to_file(kab_user.debt, "ку", file_path)
    if(hasattr(petro_user, "debt")):
        append_to_file(petro_user.debt, "электричество", file_path)
    append_to_file(400, "интернет", file_path)
    if(hasattr(kab_user, "debt") and hasattr(petro_user, "debt")):
        append_to_file("\nИтого", str(kab_user.debt + petro_user.debt + 400) + "\n", file_path)
    else:
        append_to_file("\nInfo:", "получена не вся информация, проверьте вывод консоли\n", file_path)


if __name__ == "__main__":
    """Создаем экземпляры классов пользователя Кабинет-жителя и Петроэлектросбыт. Необходимые атрибуты устанавливаются в конструкторе. 
    Если залогиниться не удается, атрибуты-токены будут установлены как None, а атрибут с долгом не будет установлен."""
    kab_user = KabZitUser("LOGIN", "PASSWORD") # LOGIN и PASSWORD должны быть заменены
    petro_user = PetroUser("PHONE", "LOGIN", "PASSWORD") # LOGIN_TYPE, LOGIN и PASSWORD должны быть заменены

    generate_check(kab_user, petro_user)

    


