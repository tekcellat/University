#include <limits.h>
#include "config.h"
#include "common.h"
#include "history.h"
#include "thr_pool.h"

void *handle_connection(void *);
void read_from_socket(int, char **);
void write_to_socket(int, const char *);
void log_history(SA_IN, const char *);

history *logger;

int main(int argc, char **argv)
{
    int server_socket, client_socket, addr_size;
    SA_IN server_addr, client_addr;

    // 1. Create server socket
    if ((server_socket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)) < 0)
        err_n_exit("Create socket failed");

    // 2. Setup server address
    bzero(&server_addr, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    server_addr.sin_port = htons(SERVER_PORT);

    // 3. Bind socket to address
    if (bind(server_socket, (SA *)&server_addr, sizeof(server_addr)) < 0)
        err_n_exit("Bind failed");

    // 4. Listen on socket
    if (listen(server_socket, SERVER_BACKLOG) < 0)
        err_n_exit("Listen failed");

    // Extra Task. Setup history
    logger = create(USER_MAX);

    /*
     * The thread in the pool will keep waiting until it gets signaled from the main thread
     * The main thread sends signal when there is a new connection coming into the server
     */

    // Create a set of threads to handle future connections
    thr_pool_t *pool;
    if ((pool = thr_pool_create(
             THREAD_POOL_MIN,
             THREAD_POOL_MAX,
             THREAD_POOL_LINGER,
             NULL)) == NULL)
        err_n_exit("Create pool failed");

    while (1)
    {
        printf("Waiting for connections on port %d...\n", SERVER_PORT);
        fflush(stdout);

        addr_size = sizeof(SA_IN);
        client_socket = accept(
            server_socket,
            (SA *)&client_addr,
            (socklen_t *)&addr_size);

        if (client_socket < 0)
            err_n_exit("Accept failed");

        client *pclient = (client *)malloc(sizeof(client));
        pclient->socket = client_socket;
        pclient->addr = client_addr;

        if (thr_pool_queue(pool, handle_connection, (void *)pclient) == -1)
            err_n_exit("Queue pool failed");
    }

    thr_pool_destroy(pool);
    close(server_socket);
    return 0;
}

void *handle_connection(void *pclient)
{
    int client_socket = ((client *)pclient)->socket;
    SA_IN client_addr = ((client *)pclient)->addr;
    free(pclient);

    char *http_req = alloc(MSGLEN);
    char *status_code = alloc(MSGLEN);
    char *actualpath = alloc(PATH_MAX);
    FILE *fp;

    /*
     * Server receives the http-req from client,
     * then it sends http-res back to client
     */
    read_from_socket(client_socket, &http_req);

    // Get the requested filename
    char *file_req = strchr(http_req, '/') + 1;
    int index = 0;
    while (file_req[index] != ' ')
        index++;
    file_req[index] = '\0';

    // Log user's visited page
    log_history(client_addr, file_req);

    strcpy(status_code, "200 OK");

    // Validity check for file_req
    if (realpath(file_req, actualpath) == NULL)
    {
        strcpy(status_code, "404 Not Found");
    }
    else
    {
        fp = fopen(actualpath, "r");
        if (fp == NULL)
            strcpy(status_code, "403 Forbidden");
    }

    // Create and send header first
    char *http_res_header = alloc(MSGLEN);
    memset(http_res_header, 0, MSGLEN);
    snprintf(http_res_header, MSGLEN, "HTTP/1.1 %s", status_code);
    if (status_code[0] == '2')
    {
        fseek(fp, 0L, SEEK_END);
        char *temp = alloc(MSGLEN);
        snprintf(temp, MSGLEN, "\nContent-length: %ld\nContent-Type: text/html", ftell(fp));
        strcat(http_res_header, temp);
        fseek(fp, 0L, SEEK_SET);
        free(temp);
    }
    strcat(http_res_header, "\r\n\r\n");

    write_to_socket(client_socket, http_res_header);

    // If the file requested exist, read its content
    // and send it to client as the response's body msg
    if (status_code[0] == '2')
    {
        uint32_t bytes_read;
        char *http_res_body = alloc(MSGLEN);
        memset(http_res_body, 0, MSGLEN);

        do
        {
            bytes_read = fread(http_res_body, sizeof(unsigned char), MSGLEN, fp);

            if (bytes_read > 0)
                write_to_socket(client_socket, http_res_body);
            else
                break;
        } while (feof(fp) == 0);

        free(http_res_body);
        fclose(fp);
    }

    free(http_req);
    free(actualpath);
    free(status_code);
    free(http_res_header);
    close(client_socket);

    show_log(logger);
    return NULL;
}

void read_from_socket(int socket, char **msg)
{
    uint32_t bytes_read, received, cur_size;

    memset(*msg, 0, MSGLEN);
    cur_size = MSGLEN;
    received = 0;
    do
    {
        bytes_read = read(socket, (*msg) + received, MSGLEN);
        received += bytes_read;

        if (bytes_read < 0)
            err_n_exit("Read failed");

        if (bytes_read == 0 || strstr((*msg) + (received - bytes_read), "\r\n\r\n") != NULL)
            break;

        if (received + MSGLEN > cur_size)
        {
            cur_size = received + MSGLEN;
            (*msg) = realloc(*msg, cur_size);
        }
    } while (1);
}

void write_to_socket(int socket, const char *msg)
{
    uint32_t bytes_write, sent, total;

    total = strlen(msg);
    sent = 0;
    do
    {
        bytes_write = write(socket, msg + sent, total - sent);
        if (bytes_write < 0)
            err_n_exit("Write failed");
        if (bytes_write == 0)
            break;
        sent += bytes_write;
    } while (sent < total);
}

void log_history(SA_IN id, const char *page)
{
    int ok = 0;
    for (int i = 0; i < logger->user_num; i++)
    {
        if (compare(logger->users[i].id, id))
        {
            uint32_t last = logger->users[i].page_num;
            logger->users[i].page_num++;
            logger->users[i].pages[last] = realloc(logger->users[i].pages[last], strlen(page));
            strcpy(logger->users[i].pages[last], page);
            ok = 1;
            break;
        }
    }

    if (ok == 0)
    {
        if (logger->user_num + 1 > logger->capacity)
        {
            logger->curr_index = (logger->curr_index + 1) % logger->capacity;
            uint32_t index = logger->curr_index;
            logger->users[index].id = id;
            logger->users[index].page_num = 1;
            logger->users[index].pages[0] = alloc(strlen(page));
            strcpy(logger->users[index].pages[0], page);
        }
        else
        {
            uint32_t last = logger->user_num;
            logger->user_num++;
            logger->curr_index++;
            logger->users[last].id = id;
            logger->users[last].page_num = 1;
            logger->users[last].pages[0] = alloc(strlen(page));
            strcpy(logger->users[last].pages[0], page);
        }
    }
}