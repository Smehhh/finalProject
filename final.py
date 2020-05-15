import json
import random
import re

STR_PATTERN = re.compile(r"([A-Za-z\-?]+[\s]*\b)")  # паттерн для проверки данных на корректность
COUNT = 20  # количество адресов для генерации


def load_json_from_file(file):
    """
    Функция для чтения данных из json-файла
    :param file: имя файла
    :return: прочитанные данные
    """
    with open(file) as json_file:
        data = json.load(json_file)
    return data


def on_test_mode(test_mode):
    """
    Декоратор, при вызове которого в консоль выводится строка вида «Вызов функции x с параметрами a, b, c»
    если значение хотя бы одного из аргументов было равно указанному и функция не вызывается.
    """

    def filter_ip_decorator(fn):
        def wrapper(args):
            for piece in args:
                for i in piece:
                    if test_mode == i:
                        print(f"Вызов функции {fn.__name__}  с параметрами {args} ")
                    else:
                        fn(args)

        return wrapper

    return filter_ip_decorator


# @on_test_mode("Moscow")
def address_parse(data, unique=True):
    """
    Обработчик входных данных
    :param data: Начальные данные
    :param unique: Флаг уникальности
    :return: Двумерный массив проверенных данных
    """
    if not isinstance(data, list):
        raise TypeError(f"Шаблон должен быть словарем, не {type(data)}")
    if not all(isinstance(oct_, list) for oct_ in data):
        raise TypeError("Шаблон должен включать в себя только списки")
    if len(data) != 3:
        raise ValueError("Шаблон должен быть длины 3!")
    tmp = []
    for address_part in data:
        part_list = []
        if not address_part:
            raise ValueError("Каждое поле должно содержать минимум одно значение")
        for item in address_part:
            if isinstance(item, str):
                if re.match(STR_PATTERN, item) is not None:
                    part_list.append(item)
                else:
                    raise Warning(f"Вы ввели название {item} с ошибкой. Названия должны содержать только буквы и тире")
            else:
                raise TypeError("Поля должны содержать только строки")
        tmp.append(part_list)

    if unique:
        unique_tmp = map(set, tmp)
        return list(map(list, unique_tmp))
    else:
        return tmp


def generate_address(tmp):
    """
    Генератор, возвращающий случайный адрес
    :param tmp: начальные данные пользователя в виде двумерного массива
    """
    template = address_parse(tmp)
    while True:
        state = random.choice(template[0])
        city = random.choice(template[1])
        street = random.choice(template[2])
        house = "Building " + str(random.choice(range(1, 200)))   # добавление дома
        is_block = random.randint(0, 1)
        if is_block:  # добавление корпуса
            block = "Block " + str(random.choice(range(1, 15)))
        apt = "Apt. " + str(random.choice(range(1, 900)))  # добавление номера квартиры
        if is_block:
            address = f"{state}, {city}, {street}, {house}, {block}, {apt}"
        else:
            address = f"{state}, {city}, {street}, {house}, {apt}"
        input_ = yield address
        if input_ is not None:
            pass


def main():
    gen = generate_address(load_json_from_file("settings.json"))
    for _ in range(COUNT):
        print(next(gen))
    # address_parse(load_json_from_file("settings.json")) # для проверки работы декоратора


if __name__ == "__main__":
    main()
