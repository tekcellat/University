/* 5я часть
**Написать программу, в которой parent&child обмениваются 
**сообщением через программный канал.
*/

#include <stdio.h> //printf
#include <stdlib.h> //exit
#include <unistd.h> //pipe
#include <string.h> //strlen
#include <signal.h>
#include <time.h>

int parent_flag = 0;

void sigint_catcher(int signum) {
    printf( "\nProccess Catched signal #%d\n", signum);
    printf("Sent any message to clihd!\n");
    parent_flag = 1;
}

int main() {
	int child;
	int descr[2]; //дескриптор _одного_ программного канала
	//[0] - выход для чтения, [1] - выход для записи
	//потомок унаследует открытый программный канал предка

	signal(SIGINT, sigint_catcher);
	//signal(SIGCHLD, SIG_DFL);

	if ( pipe(descr) == -1) {
        	perror( "Couldn't pipe." );
		exit(1);
	}

	child = fork();
	if ( child == -1 ) {
        	perror( "Couldn't fork." );
		exit(1);
	}
	if ( child == 0 ) {

		close( descr[1] ); //потомок ничего не запишет в канал

		char msg[64];
		memset( msg, 0, 64 );
		int i = 0;

		//последовательно считываем из программного канала по 1 символу
		while( read(descr[0], &(msg[i++]), 1) != '\0' ) ;

		printf("Child: reading...\n\n");
		printf( "Child: read <%s>\n", msg );
	}
	else {

		close( descr[0] ); //предок ничего не считает из канала

		printf( "Parent: Waiting for CTRL+C signal for 5 seconds...\n" );
		sleep(5);

		 if (parent_flag) {
		     char msg[64] = "It`s my message for you, dear child. Father.";
		     write( descr[1], msg, strlen(msg) ); //передаём сообщение в канал

		     exit(0);

		 }
		 else {
		     char msg[64] = "Hi child!";
		     write( descr[1], msg, strlen(msg) ); //передаём сообщение в канал
		 }
		return 0;
	}
}
