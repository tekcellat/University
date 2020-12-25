#include "login.h"

struct user getUser()
{
	struct user currentUser;
	currentUser.state = NOTLOGGEDIN;
	printf("Insert username: ");

	/* username */
	if (fgets(currentUser.username, NMAX, stdin) == 0)
	{
		printf("Error reading username");
	}
	currentUser.username[strlen(currentUser.username) - 1] = 0;

	printf("Insert password: ");
	int n;
	/* password */
	getPassword(currentUser.password, stdin);
	currentUser.password[strlen(currentUser.password) - 1] = 0;

	return currentUser;
};

void getPassword(char *lineptr, FILE *stream)
{
	struct termios old, new1;
	int nread;
	/* Turn echoing off and fail if we can't. */
	if (tcgetattr(fileno(stream), &old) != 0)
		return;
	new1 = old;
	new1.c_lflag &= ~ECHO;
	if (tcsetattr(fileno(stream), TCSAFLUSH, &new1) != 0)
		return;
	/* Read the password. */
	fgets(lineptr, NMAX, stream);
	/* Restore terminal. */
	(void)tcsetattr(fileno(stream), TCSAFLUSH, &old);
};