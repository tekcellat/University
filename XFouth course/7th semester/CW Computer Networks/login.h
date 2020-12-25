#include <stdio.h>
#include <termios.h>
#include <stdlib.h>
#include <string.h>
#define NMAX 35
#define ADMIN 0
#define USUALUSER 1
#define NOTLOGGEDIN -1

/*
* The structure that contains a user's data.
*/
struct user {
	char username[35];
	char password[35];
	int state;
};

/*
* Read a username and password from the keyboard.
* Returns a structure that contains this data.
*/
struct user getUser();
/*
* It intervenes when the password needs to be read in getUser.
* Temporarily blocks the display in the console until the user presses ENTER.
*/
void getPassword(char *lineptr, FILE *stream);