#include <stdio.h>
#include <stdlib.h> 
#include <unistd.h> 
#include <signal.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/ipc.h>
#include <sys/sem.h>
#include <sys/shm.h>
#include <sys/stat.h>


const int N = 9;
const size_t shm_size = (9 + 2) * sizeof(int);

int* shm_attached_address;
int* shm_buffer;
int* shm_pos_consumer;
int* shm_pos_producer;

#define SB 0
#define SE 1
#define SM 2

#define P -1
#define V 1

struct sembuf producer_start[2] = { { SE , P, 0 }, { SB, P, 0 } };
struct sembuf producer_stop [2] = { { SB, V, 0 }, { SM  , V, 0 } };
struct sembuf consumer_start[2] = { { SM  , P, 0 }, { SB, P, 0 } };
struct sembuf consumer_stop [2] = { { SB, V, 0 }, { SE , V, 0 } };

void producer(const int semid, const int value, const int producer_id) {
    sleep(rand() % 3);
    if (semop(semid, producer_start, 2) == -1) {
        perror("!!! PRODUCER can't make operation on semaphors. ");
        exit(1);
    }
    shm_buffer[*shm_pos_producer] = value;
    printf("PRODUCER  %d   pos %d ===> produced %d\n", producer_id, *shm_pos_producer, shm_buffer[*shm_pos_producer]);
    (*shm_pos_producer)++;
    if (semop(semid, producer_stop, 2) == -1) {
        perror("!!! PRODUCER can't make operation on semaphors. ");
        exit(1);
    }
}

void consumer(const int semid, const int value, const int consumer_id) {
    sleep(rand() % 3);
    if (semop(semid, consumer_start, 2) == -1) {
        perror("!!! PRODUCER can't make operation on semaphors. ");
        exit(1);
    }
    printf("CONSUMER  %d   pos %d <=== consumed %d\n", consumer_id, *shm_pos_consumer, shm_buffer[*shm_pos_consumer]);
    (*shm_pos_consumer)++;

    if (semop(semid, consumer_stop, 2) == -1) {
        perror("!!! PRODUCER can't make operation on semaphors. ");
        exit(1);
    }
}

void create_producer(const int id, const int semid, int value, int COUNT) {
    pid_t child1_pid;
    if ((child1_pid = fork()) == -1) {
        perror("!!! Can't fork"); exit(1);
    }
    if(child1_pid == 0) {
        // child
        printf("Created producer %d\n", id);
        for (int i = 0; i < COUNT; i++) {
            producer(semid, value, id); value++;
        }

        printf("\tPRODUCER  %d   finished. Terminating...\n", id);
        exit(0);
    }
}

void create_consumer(const int id, const int semid, int COUNT) {
    pid_t child_pid;
    if ((child_pid = fork()) == -1) {
        perror("!!! Can't fork"); exit(1);
    }
    if(child_pid == 0) {
        printf("Created consumer %d\n", id);
        // child
        for (int i = 0; i < COUNT; i++) {
            consumer(semid, i, id);
        }

        printf("\tCONSUMER  %d   finished. Terminating...\n", id);
        exit(0);
    }
}


int main() {
    srand(0);
    int shmid;  // shared memory id
    int semid;  // semaphore id

    pid_t parent_pid = getpid();
    printf("Parent pid: %i\n", parent_pid);
    if ((shmid = shmget(IPC_PRIVATE, shm_size, IPC_CREAT | S_IRWXU | S_IRWXG | S_IRWXO)) == -1) {
        perror("Unable to create shared area"); exit(1);
    }

    shm_attached_address = shmat(shmid, NULL, 0);

    if (*(char*)shm_attached_address == -1) {
        perror("!!! can't attach memory"); exit(1);
    }

    shm_pos_producer = shm_attached_address;
    shm_pos_consumer = shm_attached_address + sizeof(int);
    shm_buffer = shm_attached_address + 2 * sizeof(int);
    (*shm_pos_producer) = 0;
    (*shm_pos_consumer) = 0;

	// создаем массив из 3х семафоров в локальном пр-ве процесса, с правами доступа PERM
    if ((semid = semget(IPC_PRIVATE, 3, IPC_CREAT | S_IRWXU | S_IRWXG | S_IRWXO)) == -1) {
        perror("Unable to create semapthores"); exit(1);
    }

    int ctl_SB = semctl(semid, SB, SETVAL, 1);
    int ctl_SE  = semctl(semid, SE , SETVAL, N);
    int ctl_SM   = semctl(semid, SM  , SETVAL, 0);

    if (ctl_SB == -1 || ctl_SE == -1 || ctl_SM == -1) {
        perror("!!! Cannot set controll semaphores"); exit(1); }
    
    create_consumer(0, semid, 4);
    create_consumer(1, semid, 5);

    create_producer(0, semid, 0, 3);
    create_producer(1, semid, 10, 3);
    create_producer(2, semid, 100, 3);

    int status;
    for (int i = 0; i < 5; i++) { wait(&status); }
	
    // отсоединяем разделяемый сегмент памяти
    if (shmdt(shm_attached_address) == -1) { 
        perror("!!! Can't detach shared memory segment"); exit(1);
    }
    exit(0);
}
