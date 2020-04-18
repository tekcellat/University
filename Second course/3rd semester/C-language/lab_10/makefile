func.o: func.h func.c
	gcc -std=c99 -Wall -Werror -g3 -pedantic -c func.c
lab10.o: func.h lab10.c
	gcc -std=c99 -Wall -Werror -g3 -pedantic -c lab10.c
lab10.exe: func.o lab10.o
	gcc -o lab10.exe func.o lab10.o
