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
    word = str(input("Введите слово, какое удалить: "))
    for i in range (len(text)):
        for j in range(len(text[i])):
            if text[i][j] == word:
                text.remove([i][j])
    return text


def replace(text):
    old = str(input("Введите, какое слово заменить: "))
    new = str(input("Введите, на что заменить это: "))
    for i in range (len(text)):
        for j in range(len(text[i])):
            if text[i][j] == old: text[i][j] = new
    return text


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
s1 = "So if                 you're asking me I want you to know"
s2 = "When my time comes"
s3 = "Forget the wrong that I've done"
s4 = "Help me leave behind some reasons to be missed"
s5 = "And don't resent me"
s6 = "And when you're feeling empty"
s7 = "Keep me in your memory"
s8 = "Leave out all the rest."
Text = [s1, s2, s3, s4, s5, s6, s7, s8]

text = []
for i in range(len(Text)):
    text.append(list(Text[i].split( )))
Text = text

print(Text)
Text = keys(Text)
print('\n'.join(str(value) for value in Text))
