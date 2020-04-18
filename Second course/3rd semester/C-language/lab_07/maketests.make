unit_tests.exe: func.o unit_tests.o
	gcc -o unit_tests.exe func.o unit_tests.o

unit_tests.o: func.h error.h unit_tests.c
	gcc -std=c99 -Wall -Werror -g3 -pedantic -c unit_tests.c

func.o: func.h error.h func.c
	gcc -std=c99 -Wall -Werror -g3 -pedantic -c func.c
