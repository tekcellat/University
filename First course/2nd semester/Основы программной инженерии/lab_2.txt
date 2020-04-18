import random

def indentific_words():
    df = open("note.txt", "r")
    word = str(input("Word: ")).lower()
    len_word = len(word)
    count = 0
    for line in df:
        q = 0
        for i in word:
            if i in line:
                q += 1
        if len_word <= q:
            count += 1
    print(count)
    df.close()

def indentific_symbols():
    df = open("note.txt", "r")
    symbol = str(input("Symbols: ")).lower()
    q = 0
    for line in df:
        for s in line:
            if s == symbol:
                q += 1
    print(q)
    df.close()


def generate_random():
    df = open("note.txt", "a")
    rand_int = random.randint(1, 10)
    r_str = ""
    for i in range(rand_int):
        symbol = chr(random.randint(97, 122))
        r_str += str(symbol)
    print(r_str)
    df.write("\n" + r_str)
    df.close()


def Main():
    #Главное меню
    while True:
        print("To generate random string with length 1-10 - 1")
        print("To count the quantity of indentific words - 2")
        print("To count the quantity of indentific symbols - 3")
        print("To break the programm press - 0")
        key = str(input("Press any key: "))
        if key == "1":
            generate_random()
        elif key == "2":
            indentific_words()
        elif key == "3":
            indentific_symbols()
        elif key == "0":
            break
        else:
            print("Please input olny 1,2,3,0")

Main()
