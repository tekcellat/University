lab08.o: func.h error.h lab08.c
	gcc -std=c99 -Wall -Werror -g3 -pedantic -c lab08.c

func.o: func.h error.h func.c
	gcc -std=c99 -Wall -Werror -g3 -pedantic -c func.c

lab08.exe: func.o lab08.o
	gcc -o lab08.exe func.o lab08.o

run: lab08.exe
    ./lab08.exe in_1.txt 1
clean:
	rm -rf *.o