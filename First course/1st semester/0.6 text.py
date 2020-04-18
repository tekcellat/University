def keys(text):
    while True:
        print('\n', "Выберите одно из следующих действий:")
        print("1 - для удаления какого-либо слова в тексте")
        print("2 - для замены какого-либо слова в тексте")
        print("3 - для выравнивания текста")
        print("4 - для выхода из программы")
        key = int(input())
        if key == 1:
            text = delete(text)
        elif key == 2:
            text = replace(text)
        elif key == 3:
            text = align(text)
        elif key == 4:
            return text
        else:
            print("Введите пожалуйста цифру 1 - 4 для выбора")


def delete(text):
    new_text = []
    word = str(input("Введите слово, какое удалить: "))
    for i in range(len(text)):
        new_line = text[i].replace(" " + word, " # ")
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
        print('\n', "Выберите одно из следующих действий:")
        print("1 - для выравнивания по левому краю")
        print("2 - для выравнивание по правому краю")
        print("3 - для выравнивания по ширине")
        print("4 - для выхода из программы")
        key = int(input())
        if key == 1:
            text = text_old
        elif key == 2:
            text = right_al(text)
        elif key == 3:
            text = width_al(text)
        elif key == 4:
            return text
        else:
            print("Введите пожалуйста цифру 1 - 4 для выбора")


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


# Программа для обработки текста
s1 = "This is text in English"
s2 = "I tipo know this language well"
s3 = "But i can write this program right"
s4 = "And we need dlinniy line"
s5 = "I have it in the end of text"
s6 = "In here i have 8 stok"
s7 = "And do not have smisl"
s8 = "Take how i obesyat this is dlinnaya sring"
Text = (s1, s2, s3, s4, s5, s6, s7, s8)
Text = keys(Text)
print('\n'.join(str(value) for value in Text))
