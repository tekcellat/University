#include "transferFiles.h"
#include <unistd.h>
#include <sys/wait.h>
#define MAXSQLSTATEMENT 200
#define MAXNUMBEROFFILES 100
#define ERRDIRECTORYNOTEXISTS 0
#define MAXERRORLENGTH 7

/* 
	 * Creates the necessary directories for the server (if necessary). 
	 * These directories are: 
	 * "./serverFiles" 
	 * "./serverFiles/uploadedFiles" 
	 * "./serverFiles/commitedFiles" 
	 * "./serverFiles/currentFiles" 
	 */
void createServerDirectories();

/* 
	* Please wait for the user to log in and check if the data entered are correct. 
	* Send the client what rights he has. 
	*/

void loginUser();

/* 
	* Processes commands received from the user. 
	*/
void processCommands();

/* 
	* Used to add users to the database. 
	* This right will be held only by the administration. 
	*/
int insertInUsers(char *username, char *password, int right);

/*
	* Search the database for the user given as a parameter. 
	* If it finds it, it will call the verifyUser function. 
	*/
void searchUserInDB(char *username, char *password);

/* 
	* Check what rights the user found by searchUserInDB has. 
	* Modify the currentUser variable accordingly with one of the values: ADMIN, USUALUSER. 
	*/
int verifyUser(void *, int, char **, char **);

/* 
	* Copies the source file to the destination. 
	*/
void copyFile(char *source, char *dest);

/* 
	* Browse the currentFiles folder and create a string with the names of these files separated by \ n. 
	* Return: pointer to the created string. 
	*/
char *getCurrentFilesNames();

/* 
	* Browse the uploadedFiles folder and create a string with the names of these files separated by \ n. 
	* Return: pointer to the created string. 
	*/
char *getUploadedFilesNames();

/* 
	* Scrolls through each version and creates a string with each commit and the message attached to it. 
	* Return: pointer to the created string. 
	*/
char *allCommitsMessage();

/* 
	* Extracts the message attached to the commit indicated by the "version" parameter. 
	* Return: pointer to a string created in the form "Commit x: Message \ n" 
	*/
char *commitMessageFor(char *version);

/*
	* Checks if the current command is valid and executes the corresponding commands on the 
	* database in the system. 
	*/
int executeCreateUserCommand();

/* 
	* Checks if the current command is valid and receives + writes to the folder the indicated file. 
	*/
int executeUploadCommand();

/* 
	* Checks if the current order is valid and sends the indicated file to the customer. 
	*/
int executeDownloadCommand();

/* 
	* Checks if the current command is valid and performs the commit operation. 
	*/
int executeCommitCommand();

/* 
	* Creates the diff file with the specified name for the files sent as a parameter. 
	*/
int createDiffFile(char *fileName1, char *fileName2, char *diffFileName);

/*
	* Apply diffs from the diffFile file to the fileToBePatched file. 
	*/
int patchFile(char *fileToBePatched, char *diffFile);

/* 
	* Executes commit command. 
	* There will be 2 steps: 
	* - Finding the current version and creating the appropriate folder. 
	* - Create the corresponding diff files. 
	* NOT USED !! 
	* I USED THIS FUNCTION IN A PROTOTYPE VARIANT. 
	*/
int executeCommitCommand();

/* 
	* Executes reverse command. 
	* Copy files from uploadFiles to currentFiles. 
	* Modify the files using the diffs from the indicated version. 
	* NOT USED !! 
	* I USED THIS FUNCTION IN A PROTOTYPE VARIANT. 
	*/
int executeRevertCommand();
/*
	* Execute commit command. 
	* Save the differences from the previous version.
	* There will be 2 steps: 
	* - Finding the current version and creating the appropriate folder. 
	* - Create the corresponding diff files. 
	*/
int executeCommitEfficientCommand();

/* 
	* Executes reverse command. 
	* Copy files from uploadFiles to currentFiles. 
	* Modify the files using the diffs from the indicated version. 
	*/
int executeRevertEfficientCommand(char *);

/* 
	 * Executes a showDiff command. 
	 * It will check if the indicated version and the file exist and in case of a positive answer, 
	 * it will send to the client the content of the file with difference. 
	*/
void executeShowDiffCommand();

// the current user with whom the server interacts
struct user currentUser;
// the command received from the client
struct command currentCommand;
// the socket through which the clients will be accepted
int sd;
// the socket through which the communication with the client will be made
int client;
// the private key of the server
int key;

void main(int argc, char **argv)
{
	srand(0);
	/* I generate the server encryption key. */
	key = rand() % 128;

	/* Create the necessary directories for the server. */
	createServerDirectories();

	/* The structure that stores customer data. */
	struct sockaddr_in from;
	/* I initialize it with 0. */
	bzero(&from, sizeof(from));
	/* I calculate the size of the structure. */
	int length = sizeof(from);

	/* I initialize the server. */
	sd = initServer();

	/* I process clients. */
	while (1)
	{
		/* I accept the client by creating a new socket: the client through which the communication will be made. */
		if ((client = accept(sd, (struct sockaddr *)&from, &length)) < 0)
		{
			perror("[server]Error accept().\n");
			exit(-1);
		}

		/* Create a child process. */
		int pid = fork();
		/* I'm dealing with an alleged error. */
		if (pid == -1)
		{
			printf("Error while forking!\n");
			break;
		}
		/* Son */
		if (pid == 0)
		{
			/* I close the socket through which the acceptance is made. */
			close(sd);
			printf("We have a client!\n");
			currentUser.state = NOTLOGGEDIN;

			/* I am waiting for the user to log in. */
			loginUser();

			/* I process customer orders. */
			processCommands();

			/* Close the connection. */
			close(client);

			/* I finish the son process. */
			exit(0);
		}
		else
		{
			/* I close the communication connection, because this will be taken care of by the son. */
			close(client);
		}
	}

	/* We close the connection. */
	close(sd);
}

void processCommands()
{
	/* I process orders as long as no error has occurred or the user wants to close the connection. */
	while (strcmp(currentCommand.commandName, "quit") != 0 && strcmp(currentCommand.commandName, "Error") != 0)
	{

		/* I receive the command that is to be executed. */
		currentCommand = receiveCommand(client, key);

		/* If we are dealing with an error we get out of the loop. */
		if (strcmp(currentCommand.commandName, "Error") == 0)
		{
			printf("The command was not received correctly!\n");
			fflush(stdout);
			break;
		}

		/* I am processing a create_user command */
		if (strcmp(currentCommand.commandName, "create_user") == 0)
		{
			int result = executeCreateUserCommand();

			/* I am interpreting the result. */
			if (result == 0)
			{
				printf("The create_user command couldn't be finished!\n");
			}
			if (result == 1)
			{
				printf("The user was successfully created!\n");
			}
		}

		/* I am processing a download order. */
		if (strcmp(currentCommand.commandName, "download") == 0)
		{
			int result = executeDownloadCommand();

			/* I interpret the result. */
			if (result == 0)
			{
				printf("Error: Couldn't execute download command!\n");
			}
			else
			{
				printf("The download of the file %s succeeded!\n", currentCommand.parameters[0]);
			}
		}

		/* I am processing an upload command. */
		if (strcmp(currentCommand.commandName, "upload") == 0)
		{

			int result = executeUploadCommand();

			/* I interpret the result. */
			if (result == 0)
			{
				printf("Error: Couldn't execute upload command!\n");
			}
			else
			{
				printf("The upload of the file %s succeeded!\n", currentCommand.parameters[0]);
			}

			/* Convert the result to the network format. */
			result = htonl(result);

			/* Send the result of the client's operation. */
			if (write(client, &result, sizeof(int)) < sizeof(int))
			{
				printf("Error: Couldn't write the upload result!\n");
				continue;
			}
		}

		/* I am processing a command of type currentFiles. */
		if (strcmp(currentCommand.commandName, "currentFiles") == 0)
		{
			/* Create a string that will contain the names of the files in the directory ./serverFiles/currentFiles */
			char *currentFiles = getCurrentFilesNames();

			if (currentFiles == 0)
			{
				currentFiles = (char *)malloc(MAXERRORLENGTH * sizeof(char));
				strcpy(currentFiles, "error");
			}

			/* Send this string to the server. */
			writeInFdWithTPP(client, currentFiles, key);

			/* Free memory. */
			free(currentFiles);
		}

		/* I am processing an uploadedFiles command. */
		if (strcmp(currentCommand.commandName, "uploadedFiles") == 0)
		{
			/* Create a string that will contain the filenames in the ./serverFiles/uploaded directory */
			char *currentFiles = getUploadedFilesNames();

			if (currentFiles == 0)
			{
				currentFiles = (char *)malloc(MAXERRORLENGTH * sizeof(char));
				strcpy(currentFiles, "error");
			}

			/* Send this string to the server. */
			writeInFdWithTPP(client, currentFiles, key);

			/* Free memory. */
			free(currentFiles);
		}

		/* I am processing a delete command. */
		if (strcmp(currentCommand.commandName, "delete") == 0)
		{
			/* Create a string containing the path of the file to be deleted. */
			char *filePath = (char *)malloc(MAXFILENAMELENGTH * sizeof(char));
			sprintf(filePath, "./serverFiles/uploadedFiles/%s", currentCommand.parameters[0]);
			int result;

			/* Check if the file exists. */
			if (doesFileExist(filePath) == 0)
			{
				printf("The file %s doesn't exist!\n", filePath);

				/* File does not exist, I send a negative result to the client. */
				result = 0;
				result = htonl(result);
				write(client, &result, sizeof(int));
				continue;
			}
			else
			{
				if (remove(filePath) == 0)
				{
					printf("The file %s was successfully deleted!\n", filePath);

					/* The file has been deleted, I send a positive result to the client. */
					result = 1;
					result = htonl(result);
					write(client, &result, sizeof(int));
					continue;
				}
				else
				{
					printf("The file %s couldn't be deleted!\n", filePath);

					/* The file could not be deleted, sending a negative result to the client. */
					result = 0;
					result = htonl(result);
					write(client, &result, sizeof(int));
					continue;
				}
			}

			free(filePath);
		}

		/* I am processing a commit command. */
		if (strcmp(currentCommand.commandName, "commit") == 0)
		{
			int result = executeCommitEfficientCommand();

			/* I interpret the result. */
			if (result == 0)
			{
				printf("Error: Couldn't execute commit command!\n");
			}
			else
			{
				printf("The commit succeeded!\n");
			}

			/* Convert the result to the network format. */
			result = htonl(result);
			/* I send the result to the client. */
			if (write(client, &result, sizeof(int)) < sizeof(int))
			{
				printf("Error: Couldn't write in the client socket!\n");
			}
		}

		/* I am processing a status command. */
		if (strcmp(currentCommand.commandName, "status") == 0)
		{
			char *result;
			/* Check if the status of all committees or of an individual is desired. */
			if (strcmp(currentCommand.parameters[0], "all") == 0)
			{
				/* I generate a string with the status of all commits. */
				result = allCommitsMessage();
			}
			else
			{
				/* I generate a string with the status of that commit. */
				result = commitMessageFor(currentCommand.parameters[0]);
			}

			/* I send the generated string to the client. */
			writeInFdWithTPP(client, result, key);
			/* Free memory. */
			free(result);
		}

		/* I am processing a reverse command. */
		if (strcmp(currentCommand.commandName, "revert") == 0)
		{
			int result = executeRevertEfficientCommand(currentCommand.parameters[0]);

			/* I interpret the result. */
			if (result == 0)
			{
				printf("Error: Couldn't execute commit command!\n");
			}
			else
			{
				printf("The revert succeeded!\n");
			}

			/* Convert the result to the network format. */
			result = htonl(result);
			/* I send the result to the client. */
			if (write(client, &result, sizeof(int)) < sizeof(int))
			{
				printf("Error: Couldn't write in the client socket!\n");
			}
		}

		/* I am processing a showDiff command. */
		if (strcmp(currentCommand.commandName, "showDiff") == 0)
		{
			executeShowDiffCommand();
		}
		/* I read junk characters from the buffer if they are left. */
		readJunkFromFD(client);
	}
	printf("The client has disconnected!\n");
}

void loginUser()
{
	/* As long as the user is not logged in, we are waiting for data from the client. */
	while (currentUser.state == NOTLOGGEDIN)
	{
		/* We receive the login order. */
		currentCommand = receiveCommand(client, key);

		/* We write the data in the structure of the current user. */
		strcpy(currentUser.username, currentCommand.parameters[0]);
		strcpy(currentUser.password, currentCommand.parameters[1]);
		currentUser.state = NOTLOGGEDIN;

		/* We are looking for the user in the database. */
		searchUserInDB(currentUser.username, currentUser.password);

		/* Convert user status to network format. */
		currentUser.state = ntohl(currentUser.state);
		/*	Send the user's status to the client. */
		write(client, &currentUser.state, sizeof(int));

		/* Return to the initial value of the user's state. */
		currentUser.state = htonl(currentUser.state);
		printf("%d\n", currentUser.state);
	}
}

int executeRevertCommand()
{
	// I will not comment on this function, it is similar to the efficient one.
	char *revertVersionPath = (char *)malloc(MAXFILENAMELENGTH * sizeof(char));
	strcpy(revertVersionPath, "./serverFiles/");
	strcat(revertVersionPath, currentCommand.parameters[0]);
	DIR *dir = opendir(revertVersionPath);
	if (dir == 0)
	{
		return ERRDIRECTORYNOTEXISTS;
	}

	DIR *uploadedFilesDirectory;
	struct dirent *inFile;
	char *uploadedFilesPath = (char *)malloc(MAXFILENAMELENGTH * sizeof(char));
	strcpy(uploadedFilesPath, "./serverFiles/uploadedFiles/");
	if (NULL == (uploadedFilesDirectory = opendir(uploadedFilesPath)))
	{
		printf("Failed to open the directory!\n");

		return 0;
	}

	char *currentFilesPath = (char *)malloc(MAXFILENAMELENGTH * sizeof(char));
	strcpy(currentFilesPath, "./serverFiles/currentFiles/");
	removeFilesFromDirectory(currentFilesPath);

	while ((inFile = readdir(uploadedFilesDirectory)))
	{
		if (!strcmp(inFile->d_name, "."))
			continue;
		if (!strcmp(inFile->d_name, ".."))
			continue;
		strcat(currentFilesPath, inFile->d_name);
		strcat(uploadedFilesPath, inFile->d_name);

		copyFile(uploadedFilesPath, currentFilesPath); // copyFile (source, dest)

		strcpy(currentFilesPath, "./serverFiles/currentFiles/");
		strcpy(uploadedFilesPath, "./serverFiles/uploadedFiles/");
	}
	closedir(uploadedFilesDirectory);

	DIR *currentFilesDirectory;

	if (NULL == (currentFilesDirectory = opendir(currentFilesPath)))
	{
		printf("Failed to open the directory!\n");

		return 0;
	}

	char *diffFilePath = (char *)malloc(MAXFILENAMELENGTH * sizeof(char));

	while ((inFile = readdir(currentFilesDirectory)))
	{
		if (!strcmp(inFile->d_name, "."))
			continue;
		if (!strcmp(inFile->d_name, ".."))
			continue;
		sprintf(diffFilePath, "%s/%s.diff", revertVersionPath, inFile->d_name);
		if (access(diffFilePath, F_OK) == -1)
		{
			continue;
		}
		sprintf(currentFilesPath, "./serverFiles/currentFiles/");
		strcat(currentFilesPath, inFile->d_name);
		patchFile(currentFilesPath, diffFilePath); // (fileToBePatched, diffFile)
	}
	closedir(currentFilesDirectory);

	return 1;
}

int executeCommitCommand()
{
	// I will not comment on this function. It is similar to the efficient one.
	char c;
	char *fileName = readFromFdWithTPP(client, key);
	if (read(client, &c, sizeof(char)) < 1)
	{
		printf("[server]Error reading junk character!\n");

		return 0;
	}

	fflush(stdout);
	char *filePath = (char *)malloc(MAXFILENAMELENGTH * sizeof(char));
	strcpy(filePath, "./serverFiles/commitedFiles/");
	removeFilesFromDirectory(filePath);

	while (strcmp(fileName, "finished") != 0)
	{
		strcpy(filePath, "./serverFiles/commitedFiles/");
		strcat(filePath, fileName);
		if (receiveFile(client, filePath, key) == 0)
		{
			printf("Error receiving file!\n");

			return 0;
		}
		if (read(client, &c, sizeof(char)) < 1)
		{
			printf("[server]Error reading junk character!\n");

			return 0;
		}
		fileName = readFromFdWithTPP(client, key);
		if (read(client, &c, sizeof(char)) < 1)
		{
			printf("[server]Error reading junk character!\n");

			return 0;
		}
	}

	int nrVersions = 1;
	char *directoryName = (char *)malloc(MAXFILENAMELENGTH * sizeof(char));
	sprintf(directoryName, "%d", nrVersions);
	char *directoryPath = (char *)malloc(MAXFILENAMELENGTH * sizeof(char));
	strcpy(directoryPath, "./serverFiles/");
	strcat(directoryPath, directoryName);
	while (mkdir(directoryPath, 0700) == -1)
	{
		nrVersions++;
		sprintf(directoryName, "%d", nrVersions);
		strcpy(directoryPath, "./serverFiles/");
		strcat(directoryPath, directoryName);
	}

	DIR *commitedFilesDirectory;
	struct dirent *inFile;
	char *commitedFilesDirectoryPath = (char *)malloc(MAXFILENAMELENGTH * sizeof(char));
	strcpy(commitedFilesDirectoryPath, "./serverFiles/commitedFiles/");
	if (NULL == (commitedFilesDirectory = opendir(commitedFilesDirectoryPath)))
	{
		printf("Failed to open the directory!\n");

		return 0;
	}
	char *filePath1 = (char *)malloc(MAXFILENAMELENGTH * sizeof(char));
	char *filePath2 = (char *)malloc(MAXFILENAMELENGTH * sizeof(char));
	char *diffFilePath = (char *)malloc(MAXFILENAMELENGTH * sizeof(char));
	char *currentFilesPath = (char *)malloc(MAXFILENAMELENGTH * sizeof(char));
	strcpy(currentFilesPath, "./serverFiles/currentFiles/");
	removeFilesFromDirectory(currentFilesPath);

	while ((inFile = readdir(commitedFilesDirectory)))
	{
		if (!strcmp(inFile->d_name, "."))
			continue;
		if (!strcmp(inFile->d_name, ".."))
			continue;
		printf("Diffing file: %s\n", inFile->d_name);
		strcpy(filePath1, "./serverFiles/uploadedFiles/");
		strcpy(filePath2, "./serverFiles/commitedFiles/");
		strcpy(diffFilePath, directoryPath);
		strcat(diffFilePath, "/");
		strcat(diffFilePath, inFile->d_name);
		strcat(diffFilePath, ".diff");
		strcat(filePath1, inFile->d_name);
		strcat(filePath2, inFile->d_name);
		createDiffFile(filePath1, filePath2, diffFilePath);
		sprintf(currentFilesPath, "./serverFiles/currentFiles/%s", inFile->d_name);
		copyFile(filePath2, currentFilesPath); // source, destination
	}

	if (currentCommand.nrParameters > 0)
	{
		char *commitMessageFile = (char *)malloc(MAXFILENAMELENGTH * sizeof(char));
		sprintf(commitMessageFile, "%s/message.txt", directoryPath);
		FILE *out = fopen(commitMessageFile, "w");

		for (int i = 0; i < currentCommand.nrParameters; i++)
		{
			fprintf(out, "%s ", currentCommand.parameters[i]);
		}
		fclose(out);
	}

	return 1;
}

int executeCommitEfficientCommand()
{
	/* I start with version 1 to check its existence. */
	int nrVersions = 1;
	/* I generate directory names. */
	char *directoryPath = (char *)malloc(MAXFILENAMELENGTH * sizeof(char));
	char *directoryName = (char *)malloc(MAXFILENAMELENGTH * sizeof(char));
	sprintf(directoryName, "%d", nrVersions);
	strcpy(directoryPath, "./serverFiles/");
	strcat(directoryPath, directoryName);

	/* Number until which version I reached with the commits. */
	while (1)
	{
		struct stat sb;
		/* I check if the directory exists */
		if (stat(directoryPath, &sb) == 0 && S_ISDIR(sb.st_mode))
		{
			/* It exists , so we move on to the next version. */
			nrVersions++;
			sprintf(directoryName, "%d", nrVersions);
			strcpy(directoryPath, "./serverFiles/");
			strcat(directoryPath, directoryName);
		}
		else
		{
			/* It doesn't exist, so we stop. */
			break;
		}
	}

	char *version = (char *)malloc(MAXVERSIONLENGTH * sizeof(char));
	sprintf(version, "%d", nrVersions);
	/* I bring the latest version of the files. */
	executeRevertEfficientCommand(version);

	char c;
	/* I start reading the files sent by the client. */
	char *fileName = readFromFdWithTPP(client, key);
	/* I read the junk character that remains in the buffer. */
	if (read(client, &c, sizeof(char)) < 1)
	{
		printf("[server]Error reading junk character!\n");

		return 0;
	}

	/* I generate the commitedFiles directory path. */
	char *filePath = (char *)malloc(MAXFILENAMELENGTH * sizeof(char));
	strcpy(filePath, "./serverFiles/commitedFiles/");
	/* I empty the commitedFiles directory */
	removeFilesFromDirectory(filePath);

	/* How long do we have files to receive. */
	while (strcmp(fileName, "finished") != 0)
	{
		/* Build the file path. */
		strcpy(filePath, "./serverFiles/commitedFiles/");
		strcat(filePath, fileName);
		/* I receive the file at the indicated path. */
		if (receiveFile(client, filePath, key) == 0)
		{
			printf("Error receiving file!\n");

			return 0;
		}

		/* I read the junk character that remains in the buffer. */
		if (read(client, &c, sizeof(char)) < 1)
		{
			printf("[server]Error reading junk character!\n");

			return 0;
		}

		/* I am reading the following file name. */
		fileName = readFromFdWithTPP(client, key);
		if (read(client, &c, sizeof(char)) < 1)
		{
			printf("[server]Error reading junk character!\n");

			return 0;
		}
	}

	/* Build the directory for the new commit version. */

	nrVersions = 1;
	sprintf(directoryName, "%d", nrVersions);
	/* Build the path of the commit directory. */
	strcpy(directoryPath, "./serverFiles/");
	strcat(directoryPath, directoryName);
	/* How long the directory creation failed */
	while (mkdir(directoryPath, 0700) == -1)
	{
		/* I move on to the next version. */
		nrVersions++;
		sprintf(directoryName, "%d", nrVersions);
		strcpy(directoryPath, "./serverFiles/");
		strcat(directoryPath, directoryName);
	}

	/* Helpful data structures for browsing files. */
	DIR *commitedFilesDirectory;
	struct dirent *inFile;
	/* Build the directory path that contains the files received from the client. */
	char *commitedFilesDirectoryPath = (char *)malloc(MAXFILENAMELENGTH * sizeof(char));
	strcpy(commitedFilesDirectoryPath, "./serverFiles/commitedFiles/");
	/* Open the directory containing the files received from the client. */
	if (NULL == (commitedFilesDirectory = opendir(commitedFilesDirectoryPath)))
	{
		printf("Failed to open the directory!\n");

		return 0;
	}
	/* Allocate space for the strings I will need. */
	char *filePath1 = (char *)malloc(MAXFILENAMELENGTH * sizeof(char));
	char *filePath2 = (char *)malloc(MAXFILENAMELENGTH * sizeof(char));
	char *diffFilePath = (char *)malloc(MAXFILENAMELENGTH * sizeof(char));
	char *currentFilesPath = (char *)malloc(MAXFILENAMELENGTH * sizeof(char));
	/* Build the currentFiles directory path. */
	strcpy(currentFilesPath, "./serverFiles/currentFiles/");

	/* Browse file by file from the commitedFiles directory. */
	while ((inFile = readdir(commitedFilesDirectory)))
	{
		if (!strcmp(inFile->d_name, "."))
			continue;
		if (!strcmp(inFile->d_name, ".."))
			continue;
		/* Build the appropriate file path. */
		/* filePath1: file in currentFiles */
		/* filePath2: file in commitedFiles */
		/* diffFilePath: file generated by diff */
		printf("Diffing file: %s\n", inFile->d_name);
		strcpy(filePath1, "./serverFiles/currentFiles/");
		strcpy(filePath2, "./serverFiles/commitedFiles/");
		strcpy(diffFilePath, directoryPath);
		strcat(diffFilePath, "/");
		strcat(diffFilePath, inFile->d_name);
		strcat(diffFilePath, ".diff");
		strcat(filePath1, inFile->d_name);
		strcat(filePath2, inFile->d_name);
		/* Check if the file exists. */
		if (doesFileExist(filePath1) == 1)
		{
			printf("File exists!\n");
		}
		else
		{
			printf("no");
			/* Does not exist, so I diff on the file in uploadedFiles */
			char *uploadedFilesPath = (char *)malloc(MAXFILENAMELENGTH * sizeof(char));
			sprintf(uploadedFilesPath, "./serverFiles/uploadedFiles/%s", inFile->d_name);
			if (doesFileExist(uploadedFilesPath) == 1)
			{
				createDiffFile(uploadedFilesPath, filePath2, diffFilePath);
			}
			else
			{
				printf("The file %s was not uploaded and will not be tracked. \n", inFile->d_name);
			}
			/* Copy the file from commitedFiles to currentFiles. */
			copyFile(filePath2, currentFilesPath); // source, destination
			continue;
		}
		/* Create the differences file. */
		createDiffFile(filePath1, filePath2, diffFilePath);
		/* Copy the file from commitedFiles to currentFiles. */
		sprintf(currentFilesPath, "./serverFiles/currentFiles/%s", inFile->d_name);
		copyFile(filePath2, currentFilesPath); // source, destination
	}

	/* I generate the message.txt file if the commit is accompanied by a message. */
	if (currentCommand.nrParameters > 0)
	{
		char *commitMessageFile = (char *)malloc(MAXFILENAMELENGTH * sizeof(char));
		sprintf(commitMessageFile, "%s/message.txt", directoryPath);
		FILE *out = fopen(commitMessageFile, "w");

		for (int i = 0; i < currentCommand.nrParameters; i++)
		{
			fprintf(out, "%s ", currentCommand.parameters[i]);
		}
		fclose(out);
	}

	/* Free memory. */
	free(directoryPath);
	free(directoryName);
	free(filePath);
	free(filePath1);
	free(filePath2);
	free(commitedFilesDirectoryPath);
	free(diffFilePath);
	free(currentFilesPath);

	return 1;
}

int executeRevertEfficientCommand(char *version)
{
	/* Calculate the path of the version I will have to revert to. */
	char *revertVersionPath = (char *)malloc(MAXFILENAMELENGTH * sizeof(char));
	strcpy(revertVersionPath, "./serverFiles/");
	strcat(revertVersionPath, version);
	DIR *dir = opendir(revertVersionPath);

	/* Check if this version exists. */
	if (dir == 0)
	{
		return ERRDIRECTORYNOTEXISTS;
	}

	/* Helpful data structures for browsing files. */
	DIR *uploadedFilesDirectory;
	struct dirent *inFile;

	/* Calculate uploadedFiles directory path */
	char *uploadedFilesPath = (char *)malloc(MAXFILENAMELENGTH * sizeof(char));
	strcpy(uploadedFilesPath, "./serverFiles/uploadedFiles/");

	/* Open the directory. */
	if (NULL == (uploadedFilesDirectory = opendir(uploadedFilesPath)))
	{
		printf("Failed to open the directory!\n");

		return 0;
	}

	/* I empty the currentFiles directory. */
	char *currentFilesPath = (char *)malloc(MAXFILENAMELENGTH * sizeof(char));
	strcpy(currentFilesPath, "./serverFiles/currentFiles/");
	removeFilesFromDirectory(currentFilesPath);

	/* Browse files in the uploadedFiles directory. */
	while ((inFile = readdir(uploadedFilesDirectory)))
	{
		if (!strcmp(inFile->d_name, "."))
			continue;
		if (!strcmp(inFile->d_name, ".."))
			continue;
		strcat(currentFilesPath, inFile->d_name);
		strcat(uploadedFilesPath, inFile->d_name);

		/*  Copy the file from uploadedFiles to currentFiles. */
		copyFile(uploadedFilesPath, currentFilesPath); // copyFile (source, dest)

		strcpy(currentFilesPath, "./serverFiles/currentFiles/");
		strcpy(uploadedFilesPath, "./serverFiles/uploadedFiles/");
	}

	/* Calculate how many commit versions there are so far. */
	int nrVersions = 1;
	char *directoryPath = (char *)malloc(MAXFILENAMELENGTH * sizeof(char));
	char *directoryName = (char *)malloc(MAXFILENAMELENGTH * sizeof(char));
	while (1)
	{
		struct stat sb;

		if (stat(directoryPath, &sb) == 0 && S_ISDIR(sb.st_mode))
		{
			nrVersions++;
			sprintf(directoryName, "%d", nrVersions);
			strcpy(directoryPath, "./serverFiles/");
			strcat(directoryPath, directoryName);
		}
		else
		{
			break;
		}
	}

	int revertVersion = atoi(version);

	/* Scroll through each version to the current one. */
	for (int i = 1; i <= revertVersion; i++)
	{
		sprintf(revertVersionPath, "./serverFiles/%d", i);

		/* Helpful data structures for browsing files. */
		DIR *currentFilesDirectory;
		sprintf(currentFilesPath, "./serverFiles/currentFiles");
		/* Open the currentFiles directory. */
		if (NULL == (currentFilesDirectory = opendir(currentFilesPath)))
		{
			printf("Failed to open the directory in for!\n");

			return 0;
		}

		char *diffFilePath = (char *)malloc(MAXFILENAMELENGTH * sizeof(char));

		/* Browse the currentFiles directory. */
		while ((inFile = readdir(currentFilesDirectory)))
		{
			if (!strcmp(inFile->d_name, "."))
				continue;
			if (!strcmp(inFile->d_name, ".."))
				continue;
			sprintf(diffFilePath, "%s/%s.diff", revertVersionPath, inFile->d_name);
			if (access(diffFilePath, F_OK) == -1)
			{
				continue;
			}
			/* I apply the differences from this version of commit to the current files. */
			sprintf(currentFilesPath, "./serverFiles/currentFiles/");
			strcat(currentFilesPath, inFile->d_name);
			patchFile(currentFilesPath, diffFilePath); // (fileToBePatched, diffFile)
		}

		/* Close the currentFiles directory. */
		closedir(currentFilesDirectory);
	}

	/* Free memory. */
	free(uploadedFilesPath);
	free(directoryName);
	free(directoryPath);
	free(revertVersionPath);
	free(currentFilesPath);
	return 1;
}

int executeDownloadCommand()
{
	/* We check the number of parameters. */
	if (currentCommand.nrParameters != 1)
	{
		int error = ERRWRONGFORMAT;
		error = htonl(error);
		if (write(client, &error, sizeof(int)) == 0)
		{
			printf("[server]Typing error!\n");
			return 0;
		}
		return 0;
	}
	/* Structures used to make the connection. */
	struct sockaddr_in dataSender;
	struct sockaddr_in dataReceiver;
	/* The socket through which the acceptance will be made, respectively the one through which the data transfer will be made. */
	int dataSD, acceptedDataSD;

	/* Cream socket. */
	if ((dataSD = socket(AF_INET, SOCK_STREAM, 0)) == -1)
	{
		printf("Error: Couldn't create data transfer socket!\n");
		return 0;
	}
	/* We add the REUSEADDR option on the socket. */
	int option = 1;
	setsockopt(sd, SOL_SOCKET, SO_REUSEADDR, &option, sizeof(option));

	/* We initialize the dataSender and dataReceiver structures. */
	bzero(&dataSender, sizeof(dataSender));
	bzero(&dataReceiver, sizeof(dataReceiver));

	/* Set the appropriate sockaddr fields. */
	dataSender.sin_family = AF_INET;
	dataSender.sin_addr.s_addr = htonl(INADDR_ANY);
	dataSender.sin_port = htons(0);

	/* Bind between socket and sockaddr structure */
	if (bind(dataSD, (struct sockaddr *)&dataSender, sizeof(struct sockaddr)) == -1)
	{
		perror("Error.");
		printf("Error: Couldn't bind the dataSender!\n");

		return 0;
	}

	/* We start listening for connections. */
	if (listen(dataSD, 2) == -1)
	{
		printf("Error: Couldn't listen in the data transfer socket!\n");
		return 0;
	}
	/* Calculate the dataSD socket port. */
	int length = sizeof(dataSender);
	if (getsockname(dataSD, (struct sockaddr *)&dataSender, &length) == -1)
	{
		perror("getsockname");
	}
	else
	{
		printf("port number %d\n", ntohs(dataSender.sin_port));
	}

	/* We transmit the client port to initialize the connection. */
	if (write(client, &dataSender.sin_port, sizeof(dataSender.sin_port)) < sizeof(dataSender.sin_port))
	{
		printf("Error: Couldn't write the port!\n");

		return 0;
	}

	/* We accept the client. */
	length = sizeof(dataReceiver);
	if ((acceptedDataSD = accept(dataSD, (struct sockaddr *)&dataReceiver, &length)) < 0)
	{
		printf("Data transfer link created!\n");
	}

	/* Cream the path of the file to be sent. */
	char *fileToBeSent = (char *)malloc(MAXFILENAMELENGTH * sizeof(char));
	strcpy(fileToBeSent, "./serverFiles/currentFiles/");
	strcat(fileToBeSent, currentCommand.parameters[0]);

	int ok;
	if (doesFileExist(fileToBeSent) == 0)
	{
		ok = 0;
	}
	else
	{
		ok = 1;
	}

	/* We notify the client that we can start the data transfer. */
	ok = htonl(ok);
	write(client, &ok, sizeof(int));

	/* We are sending the file. */
	int result = sendFile(acceptedDataSD, fileToBeSent, key);

	/* Close connections */
	close(dataSD);
	close(acceptedDataSD);

	/* Free memory. */
	free(fileToBeSent);
	return result;
}

int executeUploadCommand()
{
	/* We check the number of parameters. */
	if (currentCommand.nrParameters != 1)
	{
		int error = ERRWRONGFORMAT;
		error = htonl(error);
		if (write(client, &error, sizeof(int)) == 0)
		{
			printf("[server]Typing error!\n");
			return 0;
		}
		return 0;
	}
	/* Structures used to make the connection. */
	struct sockaddr_in dataSender;
	struct sockaddr_in dataReceiver;
	/* The socket through which the acceptance will be made, respectively the one through which the data transfer will be made. */
	int dataSD, acceptedDataSD;

	/* Cream socket. */
	if ((dataSD = socket(AF_INET, SOCK_STREAM, 0)) == -1)
	{
		printf("Error: Couldn't create data transfer socket!\n");
		return 0;
	}
	/* We add the REUSEADDR option. */
	int option = 1;
	setsockopt(sd, SOL_SOCKET, SO_REUSEADDR, &option, sizeof(option));

	/* We initialize the dataSender and dataReceiver structures. */
	bzero(&dataSender, sizeof(dataSender));
	bzero(&dataReceiver, sizeof(dataSender));

	/* Set the appropriate sockaddr fields. */
	dataSender.sin_family = AF_INET;
	dataSender.sin_addr.s_addr = htonl(INADDR_ANY);
	dataSender.sin_port = htons(0);

	/* Bind between socket and sockaddr structure */
	if (bind(dataSD, (struct sockaddr *)&dataSender, sizeof(struct sockaddr)) == -1)
	{
		perror("Error.");
		printf("Error: Couldn't bind the dataSender!\n");

		return 0;
	}

	/* We start listening for connections. */
	if (listen(dataSD, 2) == -1)
	{
		printf("Error: Couldn't listen in the data transfer socket!\n");
		return 0;
	}
	/* We calculate the port to which the client will have to connect. */
	int length = sizeof(dataSender);
	if (getsockname(dataSD, (struct sockaddr *)&dataSender, &length) == -1)
	{
		perror("getsockname");
	}
	else
	{
		printf("port number %d\n", ntohs(dataSender.sin_port));
	}

	/* We send the port to the client. */
	if (write(client, &dataSender.sin_port, sizeof(dataSender.sin_port)) < sizeof(dataSender.sin_port))
	{
		printf("Error: Couldn't write the port!\n");

		return 0;
	}

	/* We accept the connection with the client. */
	length = sizeof(dataReceiver);
	if ((acceptedDataSD = accept(dataSD, (struct sockaddr *)&dataReceiver, &length)) < 0)
	{
		printf("Data transfer link created!\n");
	}

	/* We send the specified file to the client. */
	char *receivedFile = (char *)malloc(MAXFILENAMELENGTH * sizeof(char));
	strcpy(receivedFile, "./serverFiles/uploadedFiles/");
	char *fileName;
	fileName = basename(currentCommand.parameters[0]);
	strcat(receivedFile, fileName);
	int result = receiveFile(acceptedDataSD, receivedFile, key);

	/* Close connection */
	close(dataSD);
	close(acceptedDataSD);

	/* Free memory. */
	free(receivedFile);
	return 1;
}

int executeCreateUserCommand()
{
	/* I check the number of parameters */
	if (currentCommand.nrParameters != 3 ||
		!(atoi(currentCommand.parameters[2]) == 0 || atoi(currentCommand.parameters[2]) == 1))
	{
		/* We have an invalid format, so we notify the client. */
		int error = ERRWRONGFORMAT;
		error = htonl(error);
		if (write(client, &error, sizeof(int)) == 0)
		{
			printf("[server]Typing error!\n");
			return 0;
		}
		return 0;
	}
	int result;
	/* We insert the user in the database. */
	result = insertInUsers(currentCommand.parameters[0], currentCommand.parameters[1],
						   atoi(currentCommand.parameters[2]));
	/* Convert from host format to network format. */
	result = htonl(result);
	/* I send the client the result obtained. */
	if (write(client, &result, sizeof(int)) == 0)
	{
		printf("[server]Typing error!\n");
		return 0;
	}

	return 1;
}

char *allCommitsMessage()
{
	char *result = (char *)malloc(MAXCOMMITNAMELENGTH * MAXNRCOMMITS * sizeof(char));
	strcpy(result, "\n");
	int nrVersions = 1;
	/* I calculate the path of the first version directory. */
	char *directoryName = (char *)malloc(MAXFILENAMELENGTH * sizeof(char));
	sprintf(directoryName, "%d", nrVersions);
	char *directoryPath = (char *)malloc(MAXFILENAMELENGTH * sizeof(char));
	strcpy(directoryPath, "./serverFiles/");
	strcat(directoryPath, directoryName);
	/* Calculate how many versions we have */
	while (1)
	{ /* Calculate the directory path for the received version as a parameter. */
		struct stat sb;

		if (stat(directoryPath, &sb) == 0 && S_ISDIR(sb.st_mode))
		{
			nrVersions++;
			sprintf(directoryName, "%d", nrVersions);
			strcpy(directoryPath, "./serverFiles/");
			strcat(directoryPath, directoryName);
		}
		else
		{
			break;
		}
	}

	for (int i = 1; i < nrVersions; i++)
	{
		char *version = (char *)malloc(MAXVERSIONLENGTH * sizeof(char));
		sprintf(version, "%d", i);

		/* I take the message for version i and add it to the total message. */
		char *currentMessage = commitMessageFor(version);
		strcat(result, currentMessage);
		strcat(result, "\n");

		free(currentMessage); /* Free memory. */
	}

	free(directoryName); /* Free memory. */
	free(directoryPath);

	return result;
}

char *commitMessageFor(char *version)
{
	char *result = (char *)malloc(MAXCOMMITNAMELENGTH * sizeof(char));
	char *message = (char *)malloc(MAXCOMMITNAMELENGTH * sizeof(char));

	char *messagePath = (char *)malloc(MAXFILENAMELENGTH * sizeof(char));
	sprintf(messagePath, "./serverFiles/%s/message.txt", version);

	/* Check if a message was left when committed. */
	if (doesFileExist(messagePath) == 0)
	{
		strcpy(message, "No message");
		sprintf(result, "Commit %s: %s\n", version, message);

		return result;
	}
	/* It exists, so I open it. */
	FILE *in = fopen(messagePath, "r");

	/* I read the message from the file and copy it as a result. */
	if (fgets(message, MAXCOMMITNAMELENGTH, in) == 0)
	{
		strcpy(message, "error");
		sprintf(result, "Commit %s: %s\n", version, message);
		return result;
	}
	sprintf(result, "Commit %s: %s\n", version, message);

	fclose(in);

	free(messagePath);
	free(message);
	return result;
}

char *getCurrentFilesNames()
{
	char *currentFilesNames = (char *)malloc(MAXFILENAMELENGTH * MAXNUMBEROFFILES * sizeof(char));
	strcpy(currentFilesNames, "\n");
	/* Calculate the path of the currentFiles directory. */
	char *directoryPath = (char *)malloc(MAXFILENAMELENGTH * sizeof(char));
	strcpy(directoryPath, "./serverFiles/currentFiles/");

	/* Helpful data structures for browsing files. */
	DIR *currentFilesDirectory;
	struct dirent *inFile;

	/* Open the directory. */
	if (NULL == (currentFilesDirectory = opendir(directoryPath)))
	{
		printf("Failed to open the directory!\n");

		return 0;
	}

	/* I go through the directory. */
	while ((inFile = readdir(currentFilesDirectory)))
	{
		if (!strcmp(inFile->d_name, "."))
			continue;
		if (!strcmp(inFile->d_name, ".."))
			continue;
		/* We add the file names to the result. */
		strcat(currentFilesNames, inFile->d_name);
		strcat(currentFilesNames, "\n");
	}

	return currentFilesNames;
}

char *getUploadedFilesNames()
{
	char *uploadedFilesNames = (char *)malloc(MAXFILENAMELENGTH * MAXNUMBEROFFILES * sizeof(char));
	strcpy(uploadedFilesNames, "\n");
	/* Calculate the path of the uploadedFiles directory. */
	char *directoryPath = (char *)malloc(MAXFILENAMELENGTH * sizeof(char));
	strcpy(directoryPath, "./serverFiles/uploadedFiles/");

	/* Helpful data structures for browsing files. */
	DIR *uploadedFilesDirectory;
	struct dirent *inFile;

	/* Open the directory. */
	if (NULL == (uploadedFilesDirectory = opendir(directoryPath)))
	{
		printf("Failed to open the directory!\n");

		return 0;
	}

	/* I go through the directory. */
	while ((inFile = readdir(uploadedFilesDirectory)))
	{
		if (!strcmp(inFile->d_name, "."))
			continue;
		if (!strcmp(inFile->d_name, ".."))
			continue;
		/* We add the file names to the result. */
		strcat(uploadedFilesNames, inFile->d_name);
		strcat(uploadedFilesNames, "\n");
	}

	return uploadedFilesNames;
}

void searchUserInDB(char *username, char *password)
{
	sqlite3 *db;
	char *err_msg = 0;

	/* I open the database. */
	int rc = sqlite3_open("users.db", &db);

	/* I check if an error has occurred. */
	if (rc != SQLITE_OK)
	{

		fprintf(stderr, "Cannot open database: %s\n",
				sqlite3_errmsg(db));
		sqlite3_close(db);

		return;
	}

	char *sql = (char *)malloc(MAXSQLSTATEMENT * sizeof(char));
	/* Build the select statement. */
	sprintf(sql, "SELECT right FROM Users where name = '%s' and password = '%s'", username, password);
	/* Execute the query. */
	rc = sqlite3_exec(db, sql, verifyUser, 0, &err_msg);

	/* I check the result. */
	if (rc != SQLITE_OK)
	{

		fprintf(stderr, "Failed to select data\n");
		fprintf(stderr, "SQL error: %s\n", err_msg);

		sqlite3_free(err_msg);
		sqlite3_close(db);

		return;
	}

	/*Close the database. */
	sqlite3_close(db);
	/* Free memory. */
	free(sql);
}

int verifyUser(void *NotUsed, int argc, char **argv,
			   char **azColName)
{
	/* We found the searched user, so we return his rights. */
	currentUser.state = atoi(argv[0]);
	return 0;
}

int insertInUsers(char *username, char *password, int right)
{
	sqlite3 *db;
	char *err_msg = 0;

	/* I open the database. */
	int rc = sqlite3_open("users.db", &db);

	/* Check for errors. */
	if (rc != SQLITE_OK)
	{

		fprintf(stderr, "Cannot open database: %s\n", sqlite3_errmsg(db));
		sqlite3_close(db);

		return 0;
	}

	/* Create the sql statement. */
	char *sql = (char *)malloc(200 * sizeof(char));
	sprintf(sql, "INSERT INTO Users VALUES('%s', '%s', %d);", username, password, right);

	/* Execute the select statement. */
	rc = sqlite3_exec(db, sql, 0, 0, &err_msg);

	/* I check the result. */
	if (rc != SQLITE_OK)
	{

		fprintf(stderr, "SQL error: %s\n", err_msg);

		sqlite3_free(err_msg);
		sqlite3_close(db);

		return 0;
	}

	/*Close the database. */
	sqlite3_close(db);
	/* Free memory. */
	free(sql);

	return 1;
}

int createDiffFile(char *fileName1, char *fileName2, char *diffFileName)
{
	/* Cream a new son. */
	int pid = fork();
	if (pid == -1)
	{
		printf("[Server]Error while forking!\n");
		return 0;
	}
	if (pid == 0)
	{
		/* son */
		/* Redirect stdout. */
		freopen(diffFileName, "w", stdout);
		/* Execute the diff command. */
		execlp("diff", "diff", fileName1, fileName2, NULL);
		printf("Error while executing diff!\n");
		exit(0);
	}
	else
	{
		/* We are waiting for the son to finish. */
		wait(NULL);

		return 1;
	}
}

int patchFile(char *fileToBePatched, char *diffFile)
{
	/* Cream a new thread . */
	int pid = fork();
	if (pid == -1)
	{
		printf("[Server]Error while forking!\n");
		return 0;
	}
	if (pid == 0)
	{
		/* son */
		/* Redirect stdin. */
		freopen(diffFile, "r", stdin);
		/* We execute the patch command. */
		execlp("patch", "patch -R", fileToBePatched, NULL);
		printf("Error while executing diff!\n");
		exit(0);
	}
	else
	{
		/* We are waiting for the son to finish. */
		wait(NULL);

		return 1;
	}
}

void copyFile(char *source, char *dest)
{
	pid_t pid;
	int status;
	/* Check if the strings are valid */
	if (!source || !dest)
	{
		printf("Source or destination wrong!\n");
	}

	/* Copy the source file to the destination. */
	pid = fork();
	if (pid == 0)
	{
		/* The son executes the cp command. */
		execl("/bin/cp", "/bin/cp", source, dest, NULL);
		printf("Couldn't execute the cp command!\n");
	}
	else if (pid < 0)
	{
		printf("Error! Couldn't create the child process!\n");
	}
	/* I'm waiting for the son */
	wait(&status);
}

void createServerDirectories()
{
	struct stat st = {0};

	/* I check if the directory exists */
	if (stat("./serverFiles", &st) == -1)
	{
		/* It doesn't exist, so I create it */
		mkdir("./serverFiles", 0700);
	}

	/* I check if the directory exists */
	if (stat("./serverFiles/uploadedFiles", &st) == -1)
	{
		/* It doesn't exist, so I create it */
		mkdir("./serverFiles/uploadedFiles", 0700);
	}

	/* I check if the directory exists */
	if (stat("./serverFiles/currentFiles", &st) == -1)
	{
		/* Doesn't exist, so I create it */
		mkdir("./serverFiles/currentFiles", 0700);
	}

	/* I check if the directory exists */
	if (stat("./serverFiles/commitedFiles", &st) == -1)
	{
		/* Doesn't exist, so I create it */
		mkdir("./serverFiles/commitedFiles", 0700);
	}
}

void executeShowDiffCommand()
{
	/* Calculate the path of the directory containing the specified version */
	char *versionPath = (char *)malloc(MAXFILENAMELENGTH * sizeof(char));
	char *filePath = (char *)malloc(MAXFILENAMELENGTH * sizeof(char));
	sprintf(versionPath, "./serverFiles/%s", currentCommand.parameters[0]);
	printf("%s\n", versionPath);

	struct stat st = {0};
	int ok = 1;
	/* Check if the directory exists */
	if (stat(versionPath, &st) == -1)
	{
		/* It does not exist, so I note that I cannot start the file submission procedure. */
		ok = 0;
	}

	if (ok == 1)
	{
		/* Calculate diff file path. */
		sprintf(filePath, "%s/%s.diff", versionPath, currentCommand.parameters[1]);

		printf("%s\n", filePath);

		/* I check if it exists. */
		if (doesFileExist(filePath) == 0)
		{
			ok = 0;
		}
	}

	/* Convert to network format. */
	ok = htonl(ok);

	/* I send the result to the client. */
	if (write(client, &ok, sizeof(int)) < sizeof(int))
	{
		printf("Error: Couldn't write the result in socket!\n");

		return;
	}
	/* Convert from host format to network format. */
	ok = ntohl(ok);
	int buffSize;
	char *fileContent = (char *)malloc(MAXBUFFLENGTH * sizeof(int));
	/* I open the file. */
	FILE *in = fopen(filePath, "r");
	if (in == 0)
	{
		printf("Error: Couldn't open file!\n");

		strcpy(fileContent, "Error");

		if (writeInFdWithTPP(client, fileContent, key) == 0)
		{
			printf("ERROR: Failed to send file %s.\n", filePath);
			return;
		}
	}

	/* I am reading the contents of the file. */
	if ((buffSize = fread(fileContent, sizeof(char), MAXBUFFLENGTH, in)) >= 0)
	{
		if (buffSize == 0)
		{
			strcpy(fileContent, "No differences!\n");
		}
		/* I send the content to the client. */
		if (writeInFdWithTPP(client, fileContent, key) == 0)
		{
			printf("ERROR: Failed to send file %s.\n", filePath);
			return;
		}
	}
}
