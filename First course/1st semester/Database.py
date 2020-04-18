from os import listdir
import pickle

current_db_name = None
db_list = listdir(path='.')
current_db = []


def create():
    """ Создание базы данных. """
    name = input('Введите имя файла:')
    if name == '':
        print('Имя файла не может быть пустым.')
    else:
        f = open(name, 'wb')
        pickle.dump([], f)
        f.close()
    
    
def open_db(s):
    """ Открыть существующую базу данных. """
    global current_db_name
    global current_db
    if s == 0:
        current_db_name = input('Введите имя файла: ')
    else:
        current_db_name = s
    if current_db_name in db_list:
        with open(current_db_name, 'rb') as f:
            current_db = pickle.load(f)
        print('Вы успешно открыли базу данных', current_db_name)
    else:
        print('Такой базы данных не существует.')
        current_db_name = None
    
    
def print_db(db, name):
    """ Вывести базу данных на экран. """
    if name is None:
        print('Сначала вы должны открыть базу данных.')
    else:
        line = '{:20}' + u'\u2502' + '{:14}'
        print()
        print(line.format('Фамилия', '  Год рождения'))
        for row in db:
            line = '{:20}' + u'\u2502' + '{:14d}'
            print(u'\u2015'*20 + u'\u253c' + u'\u2015'*14)
            print(line.format(row['Фамилия'], int(row['год'])))
        print()


def add():
    """ Добавить запись в текущую базу данных. """
    if current_db_name is None:
        print('Сначала вы должны открыть базу данных.')
    else:
        s = input('Введите запись в виде: "Фамилия год": ')
        if len(s.split()) == 2 and s.split()[1].isdigit()\
           and int(s.split()[1]) < 2018 and len(s.split()[1]) == 4:
            words = s.split()
            current_db.append({'Фамилия': words[0], 'год': int(words[1])})
            with open(current_db_name, 'wb') as f:
                pickle.dump(current_db, f)
        else:
            print('Неверный ввод.')


def sort_by_year(line):
    return line['год']


def sort_by_surname(line):
    return line['Фамилия']


def filter_db_by_surname(current_db):
    """ Выбор элементов базы данных, удовлетворяющих фильтру по фамилии """
    filtered_db = []
    filter_db_so = input('Введите желаемое значение фамилии: ')
    for line in current_db:
        if line['Фамилия'] == filter_db_so:
            filtered_db.append(line)
    return filtered_db


def filter_db_by_year(current_db):
    """ Выбор элементов базы данных, удовлетворяющих фильтру по году """
    while True:
        year = input('Введите желаемое значение года: ')
        if year.isdigit() and int(year) < 2018:
            break
        else:
            print('Вы должны ввести год.')
    filtered_db = []
    for line in current_db:
        if line['год'] == int(year):
            filtered_db.append(line)
    return filtered_db
    
    

def search():
    """ Поиск в базе данных """
    global current_db
    if current_db_name is None:
        print('Сначала вы должны открыть базу данных.')
    else:
        while True:
            k = input('Введите название столбца, по которому вы хотите\n\
отфильтровать записи(1)фамилия; 2)год; 3)фамилия и год): ')
            if k == '1' or k == '2' or k == '3':
                k = int(k)-1
                break
            else:
                print('Неверный ввод.')
        if k == 0 or k == 1:
            if k == 0:
                filtered_db = filter_db_by_surname(current_db)
                if len(filtered_db) > 0:
                    print_db(filtered_db, '1')
                else:
                    print('Таких записей в базе данных нет.')
            if k == 1:
                filtered_db = filter_db_by_year(current_db)
                if len(filtered_db) > 0:
                    print_db(filtered_db, '1')
                else:
                    print('Таких записей в базе данных нет.')
        else:
            filtered_db = filter_db_by_surname(current_db)
            filtered_db = filter_db_by_year(filtered_db)
            if len(filtered_db) > 0:
                print_db(filtered_db, '1')
            else:
                print('Таких записей в базе данных нет.')

    
def remove():
    """ Удаление элементов из базы данных """
    global current_db
    counter = 0
    if current_db_name is None:
        print('Сначала вы должны открыть базу данных.')
    else:
        while True:
            k = input('Введите метод, по которому вы хотите\n\
отфильтровать удаляемые записи(1)фамилия; 2)год; 3)фамилия и год): ')
            if k == '1' or k == '2' or k == '3':
                k = int(k)-1
                break
            else:
                print('Неверный ввод.')
        if k == 0:
            filtered_db = filter_db_by_surname(current_db)
            for line in filtered_db:
                current_db.remove(line)
                counter += 1
            with open(current_db_name, 'wb') as f:
                    pickle.dump(current_db, f)
        if k == 1:
            filtered_db = filter_db_by_year(current_db)
            for line in filtered_db:
                current_db.remove(line)
                counter += 1
            with open(current_db_name, 'wb') as f:
                    pickle.dump(current_db, f)
        if k == 2:
            filtered_db = filter_db_by_surname(current_db)
            filtered_db = filter_db_by_year(filtered_db)
            for line in filtered_db:
                current_db.remove(line)
                counter += 1
            with open(current_db_name, 'wb') as f:
                    pickle.dump(current_db, f)
        if counter == 0:
            print('Таких записей в базе данных нет.')
        else:
            print('Удаление прошло успешно.')
def error_databaseI():
    if word == 0 or name == 0:
        print('Cannot be doing this process!')
    else:
        pass
    
def print_menu():
    """ Вывод меню """
    print('МЕНЮ:')
    print(' 1) Создать базу данных;')
    print(' 2) Открыть базу данных;')
    print(' 3) Просмотреть базу данных;')
    print(' 4) Добавить запись в базу данных;')
    print(' 5) Найти записи по фильтру;')
    print(' 6) Удалить записи по фильтру;')
    print(' 7) Выход.')


while True:
    print_menu()
    ask = input('Введите запрос: ')
    if ask == '1':
        create()
    elif ask == '2':
        open_db(0)
    elif ask == '3':
        print_db(current_db, current_db_name)
    elif ask == '4':
        add()
    elif ask == '5':
        search()
    elif ask == '6':
        remove()
    elif ask == '7':
        break
    else:
        print('Вы ввели неверный запрос.')
    db_list = listdir(path='.')
