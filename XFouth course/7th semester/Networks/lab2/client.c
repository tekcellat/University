#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <netdb.h>

#define MSG_LEN 512
#define SRV_IP "127.0.0.1"
#define SOCK_PORT 9100

int main(void)
{
    int clientSock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (clientSock < 0)
    {
        perror("socket err");
        exit(clientSock);
    }

    struct hostent *host = gethostbyname("localhost");
    if (!host)
    {
        perror("gethostbyname err");
        return -1;
    }

    struct sockaddr_in serverAddr;
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(SOCK_PORT);
    serverAddr.sin_addr = *((struct in_addr *)host->h_addr_list[0]);

    if (connect(clientSock, (struct sockaddr *)&serverAddr, sizeof(serverAddr)) < 0)
    {
        perror("connect err");
        return -1;
    }

    printf("Num please: ");
    char message[MSG_LEN];
    fgets(message, MSG_LEN, stdin);
    sendto(clientSock, message, strlen(message), 0, (struct sockaddr *)&serverAddr, sizeof(serverAddr));
    close(clientSock);
    return 0;
}
