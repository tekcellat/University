#include <sys/ipc.h>
#include <sys/sem.h>
#include <sys/shm.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <signal.h>
#include <unistd.h>

int READERS = 5; 
int WRITERS = 3;

/*
READER 0
AWRITER 1
BIN_A_WRITER 2
WAIT_WRITER 3
*/

const int PERM =  S_IRWXU | S_IRWXG | S_IRWXO;

struct sembuf start_read[] = {
    { 3, 0, 1 },
    { 1, 0, 1 },   
    { 0, 1, 1 } };

struct sembuf  stop_read[] = {
    {0, -1, 1} };

struct sembuf  start_write[] = {
    { 3, 1, 1 },
    { 0, 0, 1 },
    { 2, -1, 1 },
    { 1, 1, 1 },
    { 3, -1, 1 } };

struct sembuf  stop_write[] = {
    { 1, -1, 1 },
    { 2, 1, 1 }};


void writer(int semid, int* shm, int num) {
    while (1) {
        semop(semid, start_write, 5);
        (*shm)++;
        printf("process %d   Writer #%d ----> %d\n", getpid(),num, *shm);
        semop(semid, stop_write, 2);
        sleep(2);
    }
}

void reader(int semid, int* shm, int num) {
    
    while (1) {
        semop(semid, start_read,3);
        printf("\tprocess %d  Reader #%d <---- %d\n",getpid(), num, *shm);
        semop(semid, stop_read,1);
        sleep(1);
    }
}

int main() {

    int shm_id;
    if ((shm_id = shmget(IPC_PRIVATE, 4, IPC_CREAT | PERM)) == -1) {
        perror("Unable to create a shared area.\n");
        exit( 1 );
    }
    
    int *shm_buf = (int*)shmat(shm_id, 0, 0);
    if (shm_buf == (void*) -1) {
        perror("Memory error!");
        exit( 1 );
    }
    
    (*shm_buf) = 0;
    
    int sem_id;
    if ((sem_id = semget(IPC_PRIVATE, 4, IPC_CREAT | PERM)) == -1) {
        perror("Unable to create a semaphore.\n");
        exit( 1 );
    }
    
    int ctrl = semctl(sem_id, 2, SETVAL, 1);
    if ( ctrl == -1) {
        perror( "Can't set semaphor`s values." );
        exit( 1 );
    }
    
    pid_t pid = -1;
    
    for (int i = 0; i < WRITERS && pid != 0; i++) {
        pid = fork();
        if (pid == -1) {
            perror("Fork error from writer's.\n");
            exit( 1 );
        }
        if (pid == 0) {
            writer(sem_id, shm_buf, i);
        }
    }
    
    for (int i = 0; i < READERS && pid != 0; i++) {
        pid = fork();
        if (pid == -1) {
            perror("Fork error from reader's.\n");
            exit( 1 );
        }
        if (pid == 0) {
            reader(sem_id, shm_buf, i);
        }
    }
    
    if (shmdt(shm_buf) == -1) {
        perror( "Memory error!" );
        exit( 1 );
    }
    
    if (pid != 0) {
        int *status;
        for (int i = 0; i < WRITERS + READERS; ++i) {
            wait(status);
        }
        if (shmctl(shm_id, IPC_RMID, NULL) == -1) {
            perror( "Memory error!" );
            exit( 1 );
        }
    }
    return 0;
}