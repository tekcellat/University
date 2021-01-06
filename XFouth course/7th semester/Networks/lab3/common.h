#ifndef COMMON_H
#define COMMON_H

#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h> // for variable argument functions
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <limits.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/time.h>
#include <netdb.h>
#include "config.h"

typedef struct sockaddr_in SA_IN;
typedef struct sockaddr SA;

typedef struct client_t
{
    int socket;
    SA_IN addr;
} client;

extern void err_n_exit(const char *, ...);

extern char *alloc(uint32_t);

#endif