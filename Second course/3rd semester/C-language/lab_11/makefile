lab11.exe: func.o lab11.o
    gcc -o lab11.exe func.o lab11.o
	
func.o: func.h error.h func.c
	gcc -std=c99 -Wall -Werror -g3 -pedantic -c func.c
	
lab11.o: func.h error.h lab11.c
	gcc -std=c99 -Wall -Werror -g3 -pedantic -c lab11.c