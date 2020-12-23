#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <errno.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sqlite3.h>
#include <signal.h>
#include <pthread.h>
#include <libgen.h>
#include "connection.h"
#define MAXBUFFLENGTH 9999999
#define MAXFILENAMELENGTH 256

/* 
	* Receives a file to the indicated socket and writes it to fileName. 
	*/
int receiveFile(int sd, char *fileName, int key);

/* 
	* Sends the sent file as a parameter to the indicated socket. 
	*/
int sendFile(int sd, char *fileName, int key);

/* 
	* Checks if the indicated file exists in the file system. 
	* Return: 
	* 1 if file exists 
	* 0 if file does not exist 
	*/
int doesFileExist(const char *filename);

/* 
	* Deletes all files in the specified directory. 
	* Return: 
	* 1 if deletion was successful 
	* 0 otherwise  
	*/
int removeFilesFromDirectory(char *directoryPath);
