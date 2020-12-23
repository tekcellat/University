#include "transferFiles.h"

int sendFile(int sd, char *fileName, int key) {
	FILE *in = fopen(fileName, "r");
	/* Check if the file exists.  */
	if (doesFileExist(fileName) == 0) {
		return 0;
	} 

	char *sendBuff = (char *)malloc(MAXBUFFLENGTH * sizeof(char));
	bzero(sendBuff, MAXBUFFLENGTH);
    int buffSize;
    /* reading from the file */
    if((buffSize = fread(sendBuff, sizeof(char), MAXBUFFLENGTH, in))>0) {
        printf("%s\n", sendBuff);
        fflush(stdout);

        /* send the read content to the server. */
		if(writeInFdWithTPP(sd, sendBuff, key) == 0) {
            printf("ERROR: Failed to send file %s.\n", fileName);
            return 0;
        }
        bzero(sendBuff, MAXBUFFLENGTH);
    }

    /* free mem. */
    free(sendBuff);
	return 1;
}

int receiveFile(int sd, char *fileName, int key) {
	FILE *out = fopen(fileName, "w");
	/* checking to see if I could open the file. */
	if (out == 0) {
		printf("Error while opening the file.\n");
		return 0;
	}
	
	int buffSize;
	int writeSize;
	char *recvbuf;
	/* reading the contents of the file. */
	if((recvbuf = readFromFdWithTPP(sd, key)) != 0) {
		if (strlen(recvbuf) != 0) {
			printf("%s\n", recvbuf);
            fflush(stdout);
		}
		/* write the contents in the file. */
        for (int i = 0; i < strlen(recvbuf); i++) {
        	fprintf(out, "%c", recvbuf[i]);
        }
    }
    fclose(out);
    free(recvbuf);

	return 1;
}

int doesFileExist(const char *filename) {
    struct stat st;
    /* check if the file exists. */
    int result = stat(filename, &st);

    return result == 0;
}

int removeFilesFromDirectory(char *directoryPath) {
	DIR *directory;
	struct dirent *inFile;
	/* open the directory. */
	if (NULL == (directory = opendir(directoryPath))) {
		printf("Failed to open the directory!\n");

		return 0;
	}
	char *filePath = (char *)malloc(MAXFILENAMELENGTH * sizeof(char));

	/* browse through the files in the directory. */
	while ((inFile = readdir(directory))) {
		if (!strcmp (inFile->d_name, "."))
            continue;
        if (!strcmp (inFile->d_name, ".."))    
            continue;
        sprintf(filePath, "%s%s", directoryPath, inFile->d_name);
        /* deleting the file. */
        if (remove(filePath) == -1) {
        	return 0;
        } 
    }

    return 1;
}