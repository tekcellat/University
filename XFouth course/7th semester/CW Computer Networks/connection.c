#include "connection.h"

int initServer()
{

	/* Data structures required for connection. */
	struct sockaddr_in server;
	struct sockaddr_in from;

	int sd;
	/* I create the socket through which acceptance will be made. */
	if ((sd = socket(AF_INET, SOCK_STREAM, 0)) == -1)
	{
		printf("[server] Error creating socket!\n");
		exit(-1);
	}

	/* using the SO_REUSEADDR option */
	int on = 1;
	setsockopt(sd, SOL_SOCKET, SO_REUSEADDR, &on, sizeof(on));

	/* I initialize the sockaddr structures. */
	bzero(&server, sizeof(server));
	bzero(&from, sizeof(from));

	/* Set family */
	server.sin_family = AF_INET;
	/* I accept connection to any available address. */
	server.sin_addr.s_addr = htonl(INADDR_ANY);
	/* I accept connections to the PORT port. */
	server.sin_port = htons(PORT);

	/* Bind the socket to the sockaddr structure */
	if (bind(sd, (struct sockaddr *)&server, sizeof(struct sockaddr)) == -1)
	{
		printf("[server]Binding error!\n");
		exit(-1);
	}
	/* We start listening for connections. */
	if (listen(sd, MAXCLIENTS) == -1)
	{
		printf("[server]Listening error!\n");
		exit(-1);
	}

	return sd;
}

int connectToServer(char *ip, char *port)
{
	int sd;
	struct sockaddr_in server;
	int serverPort = atoi(port);

	/* Cream client socket. */
	if ((sd = socket(AF_INET, SOCK_STREAM, 0)) == -1)
	{
		printf("[client]Socket() error.\n");
		exit(-1);
	}

	/* We set the server data. */
	server.sin_family = AF_INET;
	server.sin_addr.s_addr = inet_addr(ip);
	server.sin_port = htons(serverPort);

	/* We make the connection. */
	if (connect(sd, (struct sockaddr *)&server, sizeof(struct sockaddr)) == -1)
	{
		printf("[client]Connection error!\n");
		exit(-1);
	}

	return sd;
}

struct command receiveCommand(int sd, int key)
{
	struct command commandReceived;
	/* I read the command name from the socket. */
	if ((commandReceived.commandName = readFromFdWithTPP(sd, key)) == 0)
	{
		printf("[server]Error reading command name!\n");
		commandReceived.commandName = (char *)malloc(MAXCOMMANDLENGTH * sizeof(char));
		strcpy(commandReceived.commandName, "Error");
		return commandReceived;
	}
	int x;
	char c;
	/* I read the junk character that remains in the buffer. */
	if (read(sd, &c, sizeof(char)) < 1)
	{
		printf("[server]Error reading junk character!\n");
		strcpy(commandReceived.commandName, "Error");
		return commandReceived;
	}
	/* I read the number of parameters. */
	if (read(sd, &x, sizeof(int)) < sizeof(int))
	{
		printf("[server]Error reading nrParameters!\n");
		strcpy(commandReceived.commandName, "Error");
		return commandReceived;
	}
	/* Convert it to the host format. */
	x = ntohl(x);
	commandReceived.nrParameters = x;
	commandReceived.parameters = (char **)malloc(MAXNRPARAMETERS * sizeof(char *));
	/* I read all the parameters. */
	for (int i = 0; i < commandReceived.nrParameters; i++)
	{
		commandReceived.parameters[i] = readFromFdWithTPP(sd, key);
		/* I read the junk character that remains in the buffer. */
		if (read(sd, &c, sizeof(char)) < 1)
		{
			printf("[server]Error reading junk character!\n");
			strcpy(commandReceived.commandName, "Error");
			return commandReceived;
		}
	}

	return commandReceived;
}

int sendCommand(int sd, struct command commandToBeSent, int key)
{
	/* Send the command name. */
	if (writeInFdWithTPP(sd, commandToBeSent.commandName, key) == 0)
	{
		return -1;
	}

	/*Send the number of parameters converted to the network format. */
	commandToBeSent.nrParameters = htonl(commandToBeSent.nrParameters);
	if (write(sd, &commandToBeSent.nrParameters, sizeof(int)) == 0)
	{
		return -1;
	}
	commandToBeSent.nrParameters = ntohl(commandToBeSent.nrParameters);
	/* Send parameter by parameter. */
	for (int i = 0; i < commandToBeSent.nrParameters; i++)
	{

		if (writeInFdWithTPP(sd, commandToBeSent.parameters[i], key) == 0)
		{
			return -1;
		}
	}
	return 0;
}

int writeInFd(int fd, char *buff)
{
	// NOT USED
	int n = strlen(buff);
	if (write(fd, &n, 4) < 4)
	{
		printf("Typing error!\n");
		return 0;
	}
	if (write(fd, buff, n + 1) < n + 1)
	{
		printf("Typing error!\n");
		return 0;
	}
	return 1;
};

char *readFromFd(int fd)
{
	// NOT USED
	int n, m;
	if (read(fd, &n, 4) < 4)
	{
		return 0;
	}
	if (n == 0)
	{
		return 0;
	}
	fflush(stdout);
	char *buff = (char *)malloc(n * sizeof(char));
	if (read(fd, buff, n) < n)
	{
		return 0;
	}

	buff[n] = 0;

	return buff;
};

int writeInFdWithTPP(int fd, char *buff, int key)
{

	/* STEP 1: Encrypt and send the message */
	int n = strlen(buff);

	encryptData(buff, strlen(buff), key);

	if (write(fd, &n, 4) < 4)
	{
		printf("Typing error!\n");
		return 0;
	}
	if (write(fd, buff, n + 1) < n + 1)
	{
		printf("Typing error!\n");
		return 0;
	}
	decryptData(buff, strlen(buff), key);

	/* STEP 2: I read the encrypted message twice. */
	int length, m;
	if (read(fd, &length, 4) < 4)
	{
		return 0;
	}
	if (length == 0)
	{
		return 0;
	}
	char *buffEncrypted = (char *)malloc(length * sizeof(char));
	if (read(fd, buffEncrypted, length) < length)
	{
		return 0;
	}
	buffEncrypted[length] = 0;

	char c;
	if (read(fd, &c, sizeof(char)) < 0)
	{
		printf("Error while reading the junk character!\n");
	}

	/* STEP 3: I decrypt the message and forward it. */
	n = strlen(buffEncrypted);
	decryptData(buffEncrypted, n, key);
	if (write(fd, &n, 4) < 4)
	{
		printf("Typing error!\n");
		return 0;
	}
	if (write(fd, buffEncrypted, n + 1) < n + 1)
	{
		printf("Typing error!\n");
		return 0;
	}

	return 1;
};

char *readFromFdWithTPP(int fd, int key)
{
	/* I read the encrypted message */
	int n, m;
	if (read(fd, &n, 4) < 4)
	{
		return 0;
	}
	if (n == 0)
	{
		return 0;
	}
	char *buff = (char *)malloc(n * sizeof(char));
	if (read(fd, buff, n) < n)
	{
		return 0;
	}

	buff[n] = 0;

	char c;
	if (read(fd, &c, sizeof(char)) < 0)
	{
		printf("Error while reading the junk character!\n");
	}

	/* I encrypt the message again and send it via fd. */
	encryptData(buff, n, key);
	if (write(fd, &n, 4) < 4)
	{
		printf("Typing error!\n");
		return 0;
	}
	if (write(fd, buff, n + 1) < n + 1)
	{
		printf("Typing error!\n");
		return 0;
	}

	/* I read the message and decrypt it to get the correct message. */
	if (read(fd, &n, 4) < 4)
	{
		return 0;
	}
	if (n == 0)
	{
		return 0;
	}
	if (read(fd, buff, n) < n)
	{
		return 0;
	}

	buff[n] = 0;

	decryptData(buff, n, key);

	return buff;
};

void encryptData(char *data, int length, int key)
{
	/* I encrypt data according to Caesar's cipher. */
	for (int i = 0; i < length; i++)
	{
		data[i] += key;
	}
}

void decryptData(char *data, int length, int key)
{
	/* I decrypt the data according to Caesar's cipher. */
	for (int i = 0; i < length; i++)
	{
		data[i] -= key;
	}
}

void readJunkFromFD(int fd)
{
	/* Fac non-blocking read. */
	fcntl(fd, F_SETFL, fcntl(fd, F_GETFL) | O_NONBLOCK);
	char *buff = malloc(MAXJUNK * sizeof(char));
	read(fd, buff, MAXJUNK);
	/* Redo read blocker. */
	fcntl(fd, F_SETFL, fcntl(fd, F_GETFL) & ~O_NONBLOCK);

	/* Free memory. */
	free(buff);
}
