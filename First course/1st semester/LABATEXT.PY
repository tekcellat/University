def removeWord(text):
    '''Удаление заданного слова из текста.'''
    word_to_remove = input("Введите слово, которое нужно удалить: ")
    for i in range(len(text)):
        ind_to_remove = text[i].find(word_to_remove)
        while not ind_to_remove == -1:
            text[i] = text[i][:ind_to_remove] +\
                      text[i][ind_to_remove+len(word_to_remove)+1:]
            ind_to_remove = text[i].find(word_to_remove)
    return text


def changeWord(text):
    '''Замена одного слова другим.'''
    word_to_change = input("Введите слово, которое нужно заменить: ")
    word_for_change = input("Введите слово, на которое нужно\
заменить предыдущее: ")
    for i in range(len(text)):
        ind_to_change = text[i].find(word_to_change)
        while not ind_to_change == -1:
            text[i] = text[i][:ind_to_change] + word_for_change +\
                      text[i][ind_to_change+len(word_to_change):]
            ind_to_change = text[i].find(word_to_change)
    return text


def formatLeft(text):
    '''Выравнивание по левой стороне.'''
    for i in range(len(text)):
        text[i] = text[i].lstrip()
    return text


def formatCenter(max_len, text):
    '''Выравнивание по ширине.'''
    for i in range(len(text)):
        text[i] = text[i].center(max_len)
    return text


def formatRight(max_len, text):
    '''Выравнивание по правой стороне.'''
    for i in range(len(text)):
        text[i] = " "*(max_len - len(text[i])) + text[i]
    return text


def threeCon(text):
    '''Поиск предложения, в каждом слове которого не менее 3 символов.'''
    


def printMenu():
    '''Вывод меню.'''
    print('МЕНЮ:\n 1)Удалить слово из текста.\n 2)Заменить одно слого другим.\
\n 3)Отформатировать текст по левому краю.\n 4)Отформатировать текст по\
правому краю.\n 5)Отформатировать текст по ширине.\n 6) Найти предложение\
 ,в каждом слове которого не менее 3 букв.\n 7)Выход из программы.')


def printText(text):
    '''Вывод текста.'''
    for i in range(len(text)):
        print(text[i])


cons = 'qwrtipsdfghjklzxcvbnm'
text = []
print("Введите текст:")
max_len = 0
while True:
    text.append(input())
    if len(text[-1]) > max_len:
        max_len = len(text[-1])
    if text[-1][-1] == '.':
        break  

while True:
    printMenu()
    ask = input('Введите цифру, соответствующую вашему запросу: ')
    if ask == '1':
        text = removeWord(text)
        printText(text)
    elif ask == '2':
        text = changeWord(text)
        printText(text)
    elif ask == '3':
        text = formatLeft(text)
        printText(text)
    elif ask == '4':
        text = formatRight(max_len, text)
        printText(text)
    elif ask == '5':
        text = formatCenter(max_len, text)
        printText(text)
    elif ask == '6':
        pass
    elif ask == '7':
        break
    else:
        print('Вы ввели неверный запрос.')
        
