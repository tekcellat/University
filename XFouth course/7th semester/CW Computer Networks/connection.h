#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/stat.h>
#include <errno.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sqlite3.h>
#include <fcntl.h>
#include <signal.h>
#include <pthread.h>
#include <dirent.h>
#include "login.h"
#define PORT 2908
#define MAXJUNK 99999
#define MAXCLIENTS 10
#define MAXCOMMANDLENGTH 50
#define MAXNRPARAMETERS 10
#define MAXPARAMETERLENGTH 32
#define ERRWRONGFORMAT -1
#define SUCCESS 1
#define ERRSQL 0
#define FAIL 0
#define ERRNORIGHTS 2
#define MAXNRCOMMITS 1024
#define MAXCOMMITNAMELENGTH 256
#define MAXVERSIONLENGTH 10

/* 
	* The structure used to send commands to the network. 
	*/
struct command
{
	char *commandName;
	int nrParameters;
	char **parameters;
};

/* 
	* Encrypt data using Caesar's Cipher. 
	*/
void encryptData(char *data, int length, int key);

/* 
	* Decrypt the data using Caesar's Cipher. 
	*/
void decryptData(char *data, int length, int key);

/* 
	* Write in the file descriptor first the size of the buffer, 
	* and then the string. 
	*/
int writeInFd(int fd, char *buff);

/* 
	* Reads a string from the descriptor. 
	* The string sent is preceded by the size of the string.
	*/
char *readFromFd(int fd);

/* 
	* Write in the file descriptor first the size of the buffer, 
	* and then the string. 
	* Uses the three-pass protocol. 
	*/
int writeInFdWithTPP(int fd, char *buff, int key);

/* 
	* Reads a string from the descriptor. 
	* The string sent is preceded by the size of the string. 
	* Uses the three-pass protocol. 
	*/
char *readFromFdWithTPP(int fd, int key);

/* 
	* Used to send a command-type structure 
	* over the network (via the socket sent as a parameter). 
	*/
int sendCommand(int sd, struct command commandToBeSent, int key);

/* 
	* Returns a command-type structure read from the descriptor. 
	*/

struct command receiveCommand(int sd, int key);

/* 
	* Initializes the server. 
	* And start listening to customers. 
	* The only thing to achieve is acceptance and customer treatment. 
	* Returns the server socket (to which you will accept). 
	*/
int initServer();

/* 
	* Connects to the server. 
	* Returns the socket through which the communication with the server will be performed. 
	*/
int connectToServer(char *ip, char *port);

/* 
	 * Reads all text in the buffer without retaining it. 
	*/
void readJunkFromFD(int fd);
