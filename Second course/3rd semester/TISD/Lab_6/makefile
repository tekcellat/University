all: main.exe clean

main.exe: functions.o main.o tree.o btree.o
	gcc -o main.exe functions.o main.o tree.o btree.o

main.o: functions.h tree.h btree.h main.c
	gcc -std=c99 -Wall -Werror -g3 -pedantic -c main.c

functions.o: functions.h tree.h btree.h functions.c
	gcc -std=c99 -Wall -Werror -g3 -pedantic -c functions.c
    
tree.o: tree.h tree.c
	gcc -std=c99 -Wall -Werror -g3 -pedantic -c tree.c
    
bree.o: btree.h tree.h btree.c
	gcc -std=c99 -Wall -Werror -g3 -pedantic -c btree.c

clean:
	rm -f *.o