lab07.exe: func.o lab07.o
	gcc -o lab07.exe func.o lab07.o

lab07.o: func.h error.h lab07.c
	gcc -std=c99 -Wall -Werror -g3 -pedantic -c lab07.c

func.o: func.h error.h func.c
	gcc -std=c99 -Wall -Werror -g3 -pedantic -c func.c
