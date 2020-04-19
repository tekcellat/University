/* 1я часть
* Написать программу, запускающую новый процесс системным вызовом 
* fork(). ‚ предке вывести собственный идентификатор ( функция
* getpid()), идентификатор группы ( функция getpgrp())  и 
* идентификатор потомка. ‚ процессе-потомке вывести собственный 
* идентификатор, идентификатор предка ( функция getppid()) и 
* идентификатор группы. убедиться, что при завершении процесса-предка 
* потомок получает идентификатор предка (PPID), равный 1.
*/

#include <stdio.h> //printf
#include <stdlib.h> //exit


int main() {
	int child = fork();
	if ( child == -1 ) {
		perror("couldn't fork.");
		exit(1);
	}

	if ( child == 0 ) {
		//потомственный код
		sleep(1);
		printf( "Child: pid=%d; 	group=%d;	parent=%d\n", getpid(), getpgrp(), getppid() );

		return 0;
	}
	int child2 = fork();
	if ( child2 == -1 ) {
		perror("couldn't fork.");
		exit(1);
	}
	if ( child2 == 0 ) {
		//потомственный код 2
		sleep(1);
		printf( "Child2: pid=%d;	group=%d;	parent=%d\n", getpid(), getpgrp(), getppid() );

		return 0;

	}
	else {
		//родительский код obshiy
        printf( "Parent: pid=%d;	group=%d;	child=%d;    child2=%d\n", getpid(), getpgrp(), child, child2 );
		return 0;
	}
}
