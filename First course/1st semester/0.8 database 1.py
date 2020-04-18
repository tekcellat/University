def main():
    file = open("0.8_database.txt")
    d = []
    d1 = []
    for line in file:
        d.append(line[:-1])
    i = -1
    for k in range(len(d) - 2):
        c = d[k]
        t = d[k + 1]
        p = d[k + 2]
        i += 1
        if i % 3 == 0:
            data = \
                {
                    "country": c,
                    "city": t,
                    "population": p
                }
            d1.append(data)
    file.close()
    work(d1)


def add(data):
    d1 = data
    while True:
        print("Введите 1 или 0")
        key = int(input())
        if key == 1:
            c = str(input("Страна: "))
            t = str(input("Город: "))
            p = str(input("Население: "))
            data = \
                {
                    "country": c,
                    "city": t,
                    "population": p
                }
            d1.append(data)
        elif key == 0:
            break
        else:
            print("Вы ввели недопустимое")
    return d1


def work(data):
    while True:
        print("Выберите одно из следующих действий:")
        print("1 - для создания базы данных")
        print("2 - для добавление записи")
        print("3 - для удаления записи")
        print("4 - для поиска по одному из полей")
        print("5 - для удаления базы данных")
        print("0 - для выхода из программы")
        key = int(input())
        if key == 1:
            data = create(data)
        elif key == 2:
            data = add(data)
        elif key == 3:
            data = delete_el(data)
        elif key == 4:
            data = find_el(data)
        elif key == 5:
            data = dele(data)
        elif key == 0:
            return show(data)
        else:
            print("Введите пожалуйста цифру 1 - 5 или 0 для выбора действия.")


def show(data):
    if len(data) > 0:
        for i in data:
            print(i)
    else:
        print("База данных пуста")


def dele(data):
    data = []
    return data

####### problem
def find_el(data):
    element = str(input("Введите элемент, который желаете найти: "))
    for i in data:
        if element in i.values():
        #if element == i["country"] or element == i["city"] or element == i["population"]:
            print(i)


def delete_el(data):
    element = str(input("Введите элемент, который желаете удалить: "))
    for i in data:
        x = data[i]
        if element in x.values():
            data.remove(x)
    return data

####### not finished yet
def create(data):

    pass
####### don`t know if its important
def end(data):
    file = open("0.8_database.txt")

    for i in data:
        pass
    file.close()


main()
