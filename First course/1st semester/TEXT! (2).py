#Программа
def keys(text):
    while True:
        print('Меню:')
        print("1 - для удаления какого-либо слова в тексте")
        print("2 - для замены какого-либо слова в тексте")
        print("3 - для выравнивания текста")
        print("4 - для выхода из программы")
        key = int(input('Введите цифру: '))
        if key == 1:
            text = delete(text)
        elif key == 2:
            text = replace(text)
        elif key == 3:
            text = align(text)
        elif key == 4:
            return text
        else:
            print("ВВЕДЁН НЕВЕРНЫЙ ЗАПРОС!!!\n\n")
            pass

def delete(text):
    new_text = []
    word = str(input("Введите слово, какое удалить: "))
    for i in range(len(text)):
        new_line = text[i].replace(" " + word, "")
        new_text.append(new_line)
    return new_text


def replace(text):
    new_text = []
    old = str(input("Введите, какое слово заменить: "))
    new = str(input("Введите, на что заменить это: "))
    for i in range(len(text)):
        new_line = text[i].replace(old, new)
        new_text.append(new_line)
    return new_text


def max_len(text):
    max_l = 0
    for i in range(len(text)):
        x = len(text[i])
        if x >= max_l:
            max_l = x
    return max_l


def align(text):
    text_old = text
    while True:
        print("Меню:")
        print("1 - для выравнивания по левому краю")
        print("2 - для выравнивание по правому краю")
        print("3 - для выравнивания по ширине")
        print("4 - для выхода из программы")
        key = int(input('Введите цифру: '))
        if key == 1:
            text = text_old
        elif key == 2:
            text = right_al(text)
        elif key == 3:
            text = width_al(text)
        elif key == 4:
            return text
        else:
            print("ВВЕДЁН НЕВЕРНЫЙ ЗАПРОС!!!\n\n")
            pass


def right_al(text):
    new_text = []
    for i in range(len(text)):
        al = max_len(text) - len(text[i])
        new_line = text[i].replace(text[i], al * " " + text[i])
        new_text.append(new_line)
    return new_text


def width_al(text):
    new_text = []
    for i in range(len(text)):
        al = int((max_len(text) - len(text[i])) / text[i].count(" "))
        if max_len(text) == len(text[i]):
            new_line = text[i]
        else:
            if al == 0:
                al += 1
            new_line = text[i].replace(" ", " " * al)
        new_text.append(new_line)
    return new_text

# Сам текст
t1 = "Это маленький текст для лабы,"
t2 = "Написали меня кое-как дабы,"
t3 = "Работала программа и была сдала лаба"
t4 = "И еще нам нужна какая-то длинная строка"
t5 = "Яблоко, груша, варенье, помидор, банан, майонез"
t6 = "И при таком завтраке тебе быстро настанет конец"
Text = [t1, t2, t3, t4, t5, t6, ]
Text = keys(Text)
print('\n'.join(str(value) for value in Text))
