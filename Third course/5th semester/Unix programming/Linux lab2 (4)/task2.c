/* 2я часть
* написать программу по схеме первого задания, но в процессе-предке 
* выполнить системный вызов wait(). !Убедиться!, что в этом случае 
* идентификатор процесса потомка на !1! больше идентификатора 
* процесса-предка.
*/

#include <stdio.h> //printf
#include <stdlib.h> //exit
#include <sys/types.h> 
#include <sys/wait.h> //wait


int main() {
	int child = fork();
	if ( child == -1 ) {
		perror("Couldn't fork.");
		exit(1);
	}

	if ( child == 0 ) {
		//потомственный код
		sleep(2);
		printf( "Child: pid=%d;	group=%d;	parent=%d\n", getpid(), getpgrp(), getppid() );
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
	if (child != 0 && child2 != 0) {
		//родительский код
		printf( "Parent: pid=%d;	group=%d;	child1=%d 	child2=%d\n", getpid(), getpgrp(), child, child2 );
		int status;
		pid_t ret_value;

		ret_value = wait( &status );
		if ( WIFEXITED(status) )
		    printf("Parent: child %d finished with %d code.\n\n", ret_value, WEXITSTATUS(status) );
		else if ( WIFSIGNALED(status) )
		    printf( "Parent: child %d finished from signal with %d code.\n\n", ret_value, WTERMSIG(status));
		else if ( WIFSTOPPED(status) )
			printf("Parent: child %d finished from signal with %d code.\n\n", ret_value, WSTOPSIG(status));
			
		ret_value = wait( &status );
		if ( WIFEXITED(status) )
			printf("Parent: child %d finished with %d code.\n\n", ret_value, WEXITSTATUS(status) );
		else if ( WIFSIGNALED(status) )
			printf( "Parent: child %d finished from signal with %d code.\n\n", ret_value, WTERMSIG(status));
		else if ( WIFSTOPPED(status) )
			printf("Parent: child %d finished from signal with %d code.\n\n", ret_value, WSTOPSIG(status));
		return 0;
	}
}
