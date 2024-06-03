from csv import DictReader, DictWriter
from os.path import exists

class NameError(Exception):
    def __init__(self, txt):
        self.txt = txt

def get_info():
    flag = False
    while not flag:
        try:
            first_name = input('Имя: ')
            if len(first_name) < 2:
                raise NameError('Слишком короткое имя')
            second_name = input('Введите фамилию: ')
            if len(second_name) < 5:
                raise NameError('Слишком короткая фамилия')
            phone_number = input('Введите номер телефона: ')
            if len(phone_number) < 11:
                raise NameError('Неверный номер')
        except NameError as err:
            print(err)
        else:
            flag = True
    return [first_name, second_name, phone_number]

def create_file(file_name):
    with open(file_name, 'w', encoding='utf-8', newline='') as data:
        f_w = DictWriter(data, fieldnames=['first_name', 'second_name', 'phone_number'])
        f_w.writeheader()

def write_file(file_name):
    res = read_file(file_name)
    user_data = get_info()
    new_obj = {'first_name': user_data[0], 'second_name': user_data[1], 'phone_number': user_data[2]}
    res.append(new_obj)
    standart_write(file_name, res)

def read_file(file_name):
    with open(file_name, encoding='utf-8') as data:
        f_r = DictReader(data)
        return list(f_r) # список со словарями

def remove_row(file_name):
    search = int(input('Введите номер строки для удаления: '))
    res = read_file(file_name)
    if 1 <= search <= len(res):
        res.pop(search - 1)
        standart_write(file_name, res)
    else:
        print('Введен неверный номер строки')

def standart_write(file_name, res):
    with open(file_name, 'w', encoding='utf-8', newline='') as data: 
        f_w = DictWriter(data, fieldnames=['first_name', 'second_name', 'phone_number'])
        f_w.writeheader()
        f_w.writerows(res)

def copy_data(source_file, dest_file, line_number):
    if not exists(source_file):
        print(f'Исходный файл {source_file} не найден.')
        return
    if not exists(dest_file):
        print(f'Файл назначения {dest_file} не найден. Создаю файл...')
        create_file(dest_file)

    src_data = read_file(source_file)
    if 1 <= line_number <= len(src_data):
        data_to_copy = src_data[line_number - 1]
        dest_data = read_file(dest_file)
        dest_data.append(data_to_copy)
        standart_write(dest_file, dest_data)
        print(f'Запись скопирована: {data_to_copy}')
    else:
        print('Некорректный номер строки.')

file_name = 'phone.csv'    
def main():
    while True:
        command = input('Введите команду: (w - запись, r - чтение, d - удаление, c - копирование, q - выход): ')
        if command == 'q':
            break
        elif command == 'w':
            if not exists(file_name):
                create_file(file_name)
            write_file(file_name)
        elif command == 'r':
            if not exists(file_name):
                print('Файл отсутствует, создайте файл')
                continue
            print(*read_file(file_name))
        elif command == 'd':
            if not exists(file_name):
                print('Файл отсутствует, создайте файл')
                continue
            remove_row(file_name)
        elif command == 'c':
            source_file = input('Введите имя исходного файла: ')
            dest_file = input('Введите имя файла назначения: ')
            line_number = int(input('Введите номер строки для копирования: '))
            copy_data(source_file, dest_file, line_number)
        else:
            print('Некорректная команда.')

main()
