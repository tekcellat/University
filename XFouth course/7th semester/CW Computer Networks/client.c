#include "transferFiles.h"

/* 
	* Returns the login command structure for the read user. 
	*/
struct command setLoginCommand(struct user myUser);

/* 
	* Check the arguments of the main function. 
	* If they are not valid, it will close the client. 
	*/
void verifySyntax(int argc, char **argv);

/* 
	* Logs the client to the server. 
	* If the login was successful, currentUser.state will be set accordingly. 
	*/
void loginUser();

/* 
	* Processes a command as a string and transforms it into a 
	* command structure . 
	*/
struct command cutCommand(char *fullCommand);

/* 
	* Reads commands, interprets them and communicates with the appropriate server. 
	*/
void processCommands();

/*
	* Send to the server the files in the "./work" directory 
	*/
int sendWorkFiles(int sd);

/* 
	* Prints on the screen the names of the files in the client's ./work directory. 
	*/
void printWorkFiles();

/* 
	 * Closes the client when it receives the SIGINT signal. 
	 * Send a shutdown command to the server. 
	*/
void closeClient();

/* 
	 * Creates the directory that the client will work with in the client directory. 
	 * The "./work/" directory will be created if it does not exist. 
	*/
void createWorkDirectory();

/* 
	 * Processes a createUser command. 
	*/
void processCreateUserCommand();

/* 
	 * Processes an upload command. 
	*/
void processUploadCommand();

/* 
	 * Processes a delete command. 
	*/
void processDeleteCommand();

/*
	 * Processes a currentFiles command. 
	*/
void processCurrentFilesCommand();

/* 
	 * Processes an uploadedFiles command. 
	*/
void processUploadedFilesCommand();

/* 
	 * Processes a download command. 
	*/
void processDownloadCommand();

/* 
	 * Processes a status command. 
	*/
void processStatusCommand();

/* 
	 * Processes a commit command. 
	*/
void processCommitCommand();

/* 
	 * Processes a reverse command. 
	*/
void processRevertCommand();

/* 
	 * Processes a showDiff command. 
	*/
void processShowDiffCommand();

// retains the data of the current user.
struct user currentUser;
// remember the type of the current command and its parameters.
struct command currentCommand;
// the socket through which I transmit data to the server.
int sd;
// private key as
int key;
// server ip
char ip[NMAX];

void main(int argc, char **argv)
{
	srand(time(0));
	/* I generate the client key through which the encryption will be done. */
	key = rand() % 128;

	/* I assign the SIGINT signal to the closeClient method to be processed. */
	signal(SIGINT, closeClient);

	/* Create the required directories if they were not created. */
	createWorkDirectory();

	/* Check if the user has entered the ip and port. */
	verifySyntax(argc, argv);

	/* I copy to an auxiliary variable, because it will be necessary when we upload / download. */
	strcpy(ip, argv[1]);
	printf("%s\n", ip);

	/* I am connecting to the server. The socket through which the data transfer will be made is returned. */
	sd = connectToServer(argv[1], argv[2]);

	/* I am waiting for the user to log in. */
	loginUser();

	/* I process user commands. */
	processCommands();

	/*Close the connection to the server. */
	close(sd);
}

void processCommands()
{
	char *fullCommand = (char *)malloc(MAXCOMMANDLENGTH * sizeof(char));

	/* I process commands until the received command is an output (quit). */
	while (strcmp(currentCommand.commandName, "quit") != 0)
	{
		printf("Insert command:\n");

		/* I read the command from the keyboard */
		fgets(fullCommand, MAXCOMMANDLENGTH, stdin);

		/* "Cut" the command in a format that helps me. */
		currentCommand = cutCommand(fullCommand);

		/* I mark that at the moment I have not executed any command. */
		int ok = 0;
		int result;

		if (strcmp(currentCommand.commandName, "create_user") == 0 && currentUser.state == ADMIN)
		{
			processCreateUserCommand();
			ok = 1;
		}
		if (strcmp(currentCommand.commandName, "upload") == 0 && currentUser.state == ADMIN)
		{
			/* I check if the indicated file exists. */
			if (doesFileExist(currentCommand.parameters[0]) == 0)
			{
				printf("This file doesn't exist!\n");
				continue;
			}

			processUploadCommand();
			ok = 1;
		}

		if (strcmp(currentCommand.commandName, "delete") == 0 && currentUser.state == ADMIN)
		{
			processDeleteCommand();
			ok = 1;
		}

		if (strcmp(currentCommand.commandName, "currentFiles") == 0)
		{
			processCurrentFilesCommand();
			ok = 1;
		}

		if (strcmp(currentCommand.commandName, "uploadedFiles") == 0 && currentUser.state == ADMIN)
		{
			processUploadedFilesCommand();
			ok = 1;
		}

		if (strcmp(currentCommand.commandName, "workFiles") == 0)
		{
			/* I check that the number of parameters is valid. */
			if (currentCommand.nrParameters != 0)
			{
				printf("Error: Invalid number of parameters!\n");
				continue;
			}

			/* I display the file names in the "./work/" directory */
			printWorkFiles();
			ok = 1;
		}

		if (strcmp(currentCommand.commandName, "download") == 0)
		{
			processDownloadCommand();
			ok = 1;
		}

		if (strcmp(currentCommand.commandName, "status") == 0)
		{
			processStatusCommand();
			ok = 1;
		}

		if (strcmp(currentCommand.commandName, "commit") == 0 && currentUser.state == ADMIN)
		{
			processCommitCommand();
			ok = 1;
		}

		if (strcmp(currentCommand.commandName, "revert") == 0 && currentUser.state == ADMIN)
		{
			processRevertCommand();
			ok = 1;
		}

		if (strcmp(currentCommand.commandName, "showDiff") == 0)
		{
			processShowDiffCommand();
			ok = 1;
		}

		if (strcmp(currentCommand.commandName, "quit") == 0)
		{
			/* I send the command to the server to notify it that it must close its connection. */
			if (sendCommand(sd, currentCommand, key) == -1)
			{
				printf("Error while sending the command!\n");
			}
			break;
		}

		if (ok == 0 && strcmp(currentCommand.commandName, "quit") != 0)
		{
			printf("Wrong command or you don't have rights to execute it!\n");
		}

		/* I read random characters if they are left in the buffer. */
		readJunkFromFD(sd);

		printf("\n");
	}
	free(fullCommand);
}

int sendWorkFiles(int sd)
{
	/* Auxiliary files that will help me browse the ./work */
	DIR *directory;
	struct dirent *inFile;
	/* Set the directory path. */
	char *directoryPath = (char *)malloc(sizeof(char) * MAXFILENAMELENGTH);
	char *filePath = (char *)malloc(sizeof(char) * MAXFILENAMELENGTH);
	strcpy(directoryPath, "./work/");

	/* Open the directory. */
	if (NULL == (directory = opendir(directoryPath)))
	{
		printf("Failed to open the directory!\n");

		return 0;
	}
	/* Browse file by file directory. */
	while ((inFile = readdir(directory)))
	{
		if (!strcmp(inFile->d_name, "."))
			continue;
		if (!strcmp(inFile->d_name, ".."))
			continue;
		/* Set the current file path. */
		strcpy(filePath, directoryPath);
		strcat(filePath, inFile->d_name);

		/* Send the name of the current directory to the server. */
		if (writeInFdWithTPP(sd, inFile->d_name, key) == 0)
		{
			printf("Failed to write in socket!\n");
			return 0;
		}

		/* I'm actually sending the file to the server. */
		sendFile(sd, filePath, key);
	}

	/* I am sending a "finished" string indicating that I have no more files to send. */
	strcpy(filePath, "finished");
	if (writeInFdWithTPP(sd, filePath, key) == 0)
	{
		printf("Failed to write in socket!\n");
		return 0;
	}

	/* Free memory. */
	free(directoryPath);
	free(filePath);

	return 1;
}

void loginUser()
{
	/* I mark that the current user is not logged in. */
	currentUser.state = NOTLOGGEDIN;

	/* As long as the user is not logged in */
	while (currentUser.state == NOTLOGGEDIN)
	{
		/* I read the username and password */
		currentUser = getUser();
		printf("\n");
		/* I send the command to the server to be processed. */
		currentCommand = setLoginCommand(currentUser);
		sendCommand(sd, currentCommand, key);

		/* I am reading the result sent by the server. */
		read(sd, &currentUser.state, sizeof(int));

		/* Convert from network format to host format. */
		currentUser.state = ntohl(currentUser.state);

		/* I interpret the response from the server. */
		if (currentUser.state == NOTLOGGEDIN)
		{
			printf("Username/Password incorrect!\n");
		}
		if (currentUser.state == ADMIN)
		{
			printf("You are logged in as ADMINISTRATOR!\n");
		}
		if (currentUser.state == USUALUSER)
		{
			printf("You are logged in as an usual user!\n");
		}
		printf("\n");
	}
}

struct command cutCommand(char *fullCommand)
{
	char *p;
	struct command builtCommand;

	builtCommand.commandName = (char *)malloc(MAXCOMMANDLENGTH * sizeof(char));
	builtCommand.parameters = (char **)malloc(MAXNRPARAMETERS * sizeof(char *));

	/* Cut the string to the first space or newline. This is the name of the command. */
	p = strtok(fullCommand, " \n");
	strcpy(builtCommand.commandName, p);

	int nrP = 0;
	p = strtok(NULL, " \n");
	/* I process parameter by parameter and add it to the builtCommand structure as a parameter. */
	while (p)
	{
		builtCommand.parameters[nrP] = (char *)malloc(MAXPARAMETERLENGTH * sizeof(char));
		strcpy(builtCommand.parameters[nrP], p);

		nrP++;

		p = strtok(NULL, " \n");
	}

	builtCommand.nrParameters = nrP;

	return builtCommand;
}

struct command setLoginCommand(struct user myUser)
{
	struct command loginCommand;

	/* initialize / assign loginCommand structure fields. */
	loginCommand.commandName = (char *)malloc(MAXCOMMANDLENGTH * sizeof(char));
	loginCommand.parameters = (char **)malloc(MAXNRPARAMETERS * sizeof(char *));
	for (int i = 0; i < MAXNRPARAMETERS; i++)
	{
		loginCommand.parameters[i] = (char *)malloc(sizeof(char) * MAXPARAMETERLENGTH);
	}
	/* Set the user data accordingly in the command structure. */
	strcpy(loginCommand.commandName, "login");
	loginCommand.nrParameters = 2;
	strcpy(loginCommand.parameters[0], currentUser.username);
	strcpy(loginCommand.parameters[1], currentUser.password);

	return loginCommand;
}

void verifySyntax(int argc, char **argv)
{
	/* Check if we have the specified format. */
	if (argc != 3)
	{
		printf("Syntax: %s <server_address> <port> must be the format!\n", argv[0]);
		exit(-1);
	}
}

void printWorkFiles()
{
	/* Data structures that help you navigate the directory. */
	DIR *workDirectory;
	struct dirent *inFile;

	/* Set the path of the directory to be traversed. */
	char *workPath = (char *)malloc(MAXFILENAMELENGTH * sizeof(char));
	strcpy(workPath, "./work/");

	/* Open the directory. */
	if (NULL == (workDirectory = opendir(workPath)))
	{
		printf("Failed to open the directory!\n");

		return;
	}
	printf("\n");

	/* Browse the directory file by file. */
	while ((inFile = readdir(workDirectory)))
	{
		if (!strcmp(inFile->d_name, "."))
			continue;
		if (!strcmp(inFile->d_name, ".."))
			continue;
		/* Display the found file. */
		printf("%s\n", inFile->d_name);
	}
	printf("\n");

	free(workPath);
}

void closeClient()
{
	/* I send a quit command to the server. */
	strcpy(currentCommand.commandName, "quit");

	if (sendCommand(sd, currentCommand, key) == -1)
	{
		printf("Error while sending the command!\n");
		return;
	}

	/* I interrupt the application. */
	exit(0);
}

void createWorkDirectory()
{
	struct stat st = {0};

	/* I check if the directory exists */
	if (stat("./work", &st) == -1)
	{
		/* It doesn't exist, so I create it */
		mkdir("./work", 0700);
	}
}

void processCreateUserCommand()
{
	int result;

	/* I check if the number of parameters is valid. */
	if (currentCommand.nrParameters != 3)
	{
		printf("Error: Invalid number of parameters for createUser command!\n");
		return;
	}

	/* Send the command to the server. */
	if (sendCommand(sd, currentCommand, key) == -1)
	{
		printf("Error while sending the command!\n");
		return;
	}

	/* I am reading the result of the creation. */
	if (read(sd, &result, sizeof(int)) < sizeof(int))
	{
		printf("Error: Couldn't read the create_user result!\n");

		return;
	}
	/* I do network to host conversion. */
	result = ntohl(result);

	/* I treat the values ​​that can take results. */
	if (result == SUCCESS)
	{
		printf("The user was created!\n");
	}
	if (result == ERRWRONGFORMAT)
	{
		printf("Error: Wrong format!\n");
	}
	if (result == ERRSQL)
	{
		printf("Error: Something gone wrong in the sql statement! Maybe this user is already in database!\n");
	}
	if (result == ERRNORIGHTS)
	{
		printf("Error: You don't have rights to execute this command!\n");
	}
}

void processUploadCommand()
{
	int result;
	/* Send the command to the server. */
	if (sendCommand(sd, currentCommand, key) == -1)
	{
		printf("Error while sending the command!\n");
		return;
	}
	/* The socket through which the file will be transferred. */
	int dataSD;
	/* The structure that contains the data of the person who will receive the file. */
	struct sockaddr_in dataSender;

	/* Create socket */
	if ((dataSD = socket(AF_INET, SOCK_STREAM, 0)) == -1)
	{
		printf("Error: Couldn't create data transfer socket!\n");

		return;
	}
	/* Socket family */
	dataSender.sin_family = AF_INET;
	/* Ip specified as parameter at runtime. */
	dataSender.sin_addr.s_addr = inet_addr(ip);
	/* I read the port I need to connect to. */
	if (read(sd, &dataSender.sin_port, sizeof(dataSender.sin_port)) < sizeof(dataSender.sin_port))
	{
		printf("Error: Couldn't read the port to connect!\n");

		return;
	}
	/* I am connecting to the new link created by the server. */
	if (connect(dataSD, (struct sockaddr *)&dataSender, sizeof(struct sockaddr)) == -1)
	{
		printf("Error couldn't connect to data transfer socket!.\n");

		return;
	}

	/* Send the file via the newly created link. */
	if (sendFile(dataSD, currentCommand.parameters[0], key))
	{
		printf("File was successfully sent!\n");
	}
	else
	{
		printf("Couldn't send file!\n");
	}

	/* Close link */
	close(dataSD);
	/* I am reading the upload result. */
	read(sd, &result, sizeof(int));

	if (result == 1)
	{
		printf("The file was successfully received!\n");
	}
	if (result == 0)
	{
		printf("Error: The file couldn't be received!\n");
	}
}

void processDeleteCommand()
{
	int result;

	/* I check the number of parameters */
	if (currentCommand.nrParameters != 1)
	{
		printf("Error: Invalid number of parameters!\n");
		return;
	}

	/* I send the command to the server. */
	if (sendCommand(sd, currentCommand, key) == -1)
	{
		printf("Error while sending the command!\n");
		return;
	}

	/* I am reading the result sent by the server. */
	if (read(sd, &result, sizeof(int)) < sizeof(int))
	{
		printf("Error: Couldn't read the result!\n");
	}
	/* Convert the result from the network to the host. */
	result = ntohl(result);

	/* I print the result of the order. */
	if (result == 1)
	{
		printf("The file was successfully deleted!\n");
	}
	if (result == 0)
	{
		printf("Error: The file couldn't be deleted!\n");
	}
}

void processCurrentFilesCommand()
{
	/* I check the number of parameters. */
	if (currentCommand.nrParameters > 0)
	{
		printf("Invalid number of parameters!\n");
		return;
	}
	/* Send the command to be processed by the server. */
	if (sendCommand(sd, currentCommand, key) == -1)
	{
		printf("Error while sending the command!\n");
		return;
	}

	/* I am reading the message received from the server. */
	char *currentFiles = readFromFdWithTPP(sd, key);

	/* I am reading a junk character that remains in the buffer. */
	char c;
	if (read(sd, &c, sizeof(char)) < 0)
	{
		printf("Error while reading the junk character!\n");
		return;
	}

	/* I check if an error has occurred. */
	if (strcmp(currentFiles, "error") == 0)
	{
		printf("An error has occurred while getting the filenames!\n");

		return;
	}

	/* Print the text received from the server. */
	printf("%s\n", currentFiles);
	/* Free memory */
	free(currentFiles);
}

void processUploadedFilesCommand()
{
	/* I check the number of parameters */
	if (currentCommand.nrParameters > 0)
	{
		printf("Invalid number of parameters!\n");

		return;
	}
	/* I send the command to the server so that it can be processed. */
	if (sendCommand(sd, currentCommand, key) == -1)
	{
		printf("Error while sending the command!\n");

		return;
	}

	/* Retrieve the server-generated string. */
	char *uploadedFiles = readFromFdWithTPP(sd, key);

	/* I read the junk character left on the connection. */
	char c;
	if (read(sd, &c, sizeof(char)) < 0)
	{
		printf("Error while reading the junk character!\n");

		return;
	}

	/* I check if I had an error. */
	if (strcmp(uploadedFiles, "error") == 0)
	{
		printf("An error has occurred while getting the filenames!\n");

		return;
	}

	/* I write the string generated by the server on the screen. */
	printf("%s\n", uploadedFiles);
	/* Free memory. */
	free(uploadedFiles);
}

void processDownloadCommand()
{
	int result;

	/* I check if the number of parameters is appropriate. */
	if (currentCommand.nrParameters != 1)
	{
		printf("Invalid number of parameters!\n");
		return;
	}
	/* I send the command to the server to be processed. */
	if (sendCommand(sd, currentCommand, key) == -1)
	{
		printf("Error while sending the command!\n");
		return;
	}
	/* The socket through which the data transfer will be made. */
	int dataSD;
	/* The structure that will remember the data of the point from which the file will be sent. */
	struct sockaddr_in dataSender;

	/* Create the socket. */
	if ((dataSD = socket(AF_INET, SOCK_STREAM, 0)) == -1)
	{
		printf("Error: Couldn't create data transfer socket!\n");

		return;
	}

	/* I set the socket family. */
	dataSender.sin_family = AF_INET;
	/* I set the ip that the client inserted when launching the application. */
	dataSender.sin_addr.s_addr = inet_addr(ip);
	/* I am reading the port I will have to connect to */
	if (read(sd, &dataSender.sin_port, sizeof(dataSender.sin_port)) < sizeof(dataSender.sin_port))
	{
		printf("Error: Couldn't read the port to connect!\n");

		return;
	}

	/* I am connecting to the new connection. */
	if (connect(dataSD, (struct sockaddr *)&dataSender, sizeof(struct sockaddr)) == -1)
	{
		printf("Error couldn't connect to data transfer socket!.\n");

		return;
	}
	/* I read if I can start the download. */
	if (read(sd, &result, sizeof(int)) < sizeof(int))
	{
		printf("Error: Couldn't read the download result!\n");
		return;
	}
	/* Convert the result from the network to the host. */
	result = ntohl(result);

	/* If the result is 0 it means that that file does not exist. */
	if (result == 0)
	{
		printf("The file required doesn't exist!\n");
		return;
	}

	/* Set where I want the downloaded file to go. */
	char *receivedFile = (char *)malloc(MAXFILENAMELENGTH * sizeof(char));
	strcpy(receivedFile, "./work/");
	strcat(receivedFile, currentCommand.parameters[0]);

	/* I receive the file. */
	if (receiveFile(dataSD, receivedFile, key))
	{
		printf("File was successfully received!\n");
	}
	else
	{
		printf("Couldn't receive file!\n");
	}

	/* Close the link. */
	close(dataSD);
	/* Free memory. */
	free(receivedFile);
}

void processStatusCommand()
{
	/* I check the number of parameters */
	if (currentCommand.nrParameters != 1)
	{
		printf("Error: Invalid number Of parameters!\n");
		return;
	}
	/* I send the command to the server to be processed. */
	if (sendCommand(sd, currentCommand, key) == -1)
	{
		printf("Error while sending the command!\n");
		return;
	}

	/* I read the server-generated string in response. */
	char *result = readFromFdWithTPP(sd, key);

	/* I'm reading a junk character that's left in the buffer. */
	char c;
	if (read(sd, &c, sizeof(char)) < 0)
	{
		printf("Error reading junk character!\n");
		return;
	}

	/* I display the server-generated string on the screen. */
	printf("%s\n", result);
	/* Free memory. */
	free(result);
}

void processCommitCommand()
{
	int result;

	/* I send the server command to be processed. */
	if (sendCommand(sd, currentCommand, key) == -1)
	{
		printf("Error while sending the command!\n");
		return;
	}

	/* I send my files from the ./work directory */
	result = sendWorkFiles(sd);
	if (result == 0)
	{
		printf("The work files couldn't be sent!\n");
		return;
	}
	else
	{
		printf("The work files were sent!\n");
	}

	/* directory I read the result of the commit. */
	if (read(sd, &result, sizeof(char)) < 0)
	{
		printf("Error: Couldn't read commit result!\n");
		return;
	}
	/* Convert from network format to host format. */
	result = ntohl(result);

	/* I interpret the result. */
	if (result == 0)
	{
		printf("The work files were received!\n");
	}
	else
	{
		printf("The work files weren't received!\n");
	}
}

void processRevertCommand()
{
	int result;
	/* Sends the command to the server for processing. */
	if (sendCommand(sd, currentCommand, key) == -1)
	{
		printf("Error while sending the command!\n");
		return;
	}

	/* I receive the order result from the server. */
	if (read(sd, &result, sizeof(int)) < 0)
	{
		printf("Error: Couldn't read revert result!\n");
		return;
	}
	/* Convert the result from the network format to the host. */
	result = ntohl(result);

	/* I interpret the result. */
	if (result == 1)
	{
		printf("The revert succeeded!\n");
	}
	else
	{
		printf("The revert failed!\n");
	}
}

void processShowDiffCommand()
{
	/* I check if the format is correct. */
	if (currentCommand.nrParameters != 2)
	{
		printf("Error: Wrong format!\n");

		return;
	}

	/* Sends the command to the server for processing. */
	if (sendCommand(sd, currentCommand, key) == -1)
	{
		printf("Error while sending the command!\n");
		return;
	}

	/* I am reading the result from the server. */
	int result;
	if (read(sd, &result, sizeof(int)) < sizeof(int))
	{
		printf("Error: Couldn't read the showDiff result!\n");
	}

	/* Convert from network format to host. */
	result = ntohl(result);
	/* One of the files does not exist. */
	if (result == 0)
	{
		printf("Error: The file/version required doesn't exist.");

		return;
	}
	/* The file / directory exists. */

	/* I read the differences from the server. */
	char *diffFile = readFromFdWithTPP(sd, key);

	/* I display the result on the screen. */
	printf("Diff %s %s:\n%s\n", currentCommand.parameters[0], currentCommand.parameters[1], diffFile);

	/* Free memory. */
	free(diffFile);
}
