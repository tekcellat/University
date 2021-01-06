#include "config.h"
#include "common.h"

void handle_connection(int, char *);
void read_from_socket(int, char **);
void write_to_socket(int, const char *);

int main(int argc, char **argv)
{
    if (argc != 2)
        err_n_exit("usage: %s <page>", argv[0]);

    int server_socket;
    SA_IN server_addr;

    // 1. Create server socket
    if ((server_socket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)) < 0)
        err_n_exit("Create socket failed");

    // 2. Setup server address
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = inet_addr(LOCAL_IP);
    server_addr.sin_port = htons(SERVER_PORT);

    // 3. Connect to server
    if (connect(server_socket, (SA *)&server_addr, sizeof(server_addr)) < 0)
        err_n_exit("Connect failed");

    handle_connection(server_socket, argv[1]);

    return 0;
}

void handle_connection(int server_socket, char *page)
{
    char *http_GET = alloc(MSGLEN);
    char *http_res = alloc(MSGLEN);
    char *host = "localhost";

    /*
     * Client creates http-req and sends it to server,
     * then it waits for http-res from server
     */

    // Create GET request
    memset(http_GET, 0, MSGLEN);
    snprintf(http_GET, MSGLEN,
             "GET /%s HTTP/1.1\r\n"
             "Host: %s:%d\r\n"
             "Content-Type: text/plain\r\n\r\n",
             page, host, SERVER_PORT);

    write_to_socket(server_socket, http_GET);

    // Receive http-res from server
    read_from_socket(server_socket, &http_res);
    printf("http_res:\n%s\n", http_res);

    free(http_res);
    free(http_GET);
    close(server_socket);
}

void read_from_socket(int socket, char **msg)
{
    uint32_t bytes_read, received, cur_size, content_len;

    // Read header
    memset(*msg, 0, MSGLEN);
    cur_size = MSGLEN;
    received = 0;
    do
    {
        bytes_read = read(socket, (*msg) + received, MSGLEN);
        received += bytes_read;

        if (bytes_read < 0)
            err_n_exit("Read failed");

        if (bytes_read == 0 || strstr(*msg + (received - bytes_read), "\r\n\r\n") != NULL)
            break;

        if (received + MSGLEN > cur_size)
        {
            cur_size = received + MSGLEN;
            (*msg) = realloc((*msg), cur_size);
        }
    } while (1);

    // Get Content-length
    char *con_len = strstr(*msg, "Content-length");
    con_len = con_len + 16;
    sscanf(con_len, "%uld", &content_len);

    content_len -= (received - (int)(strstr(*msg, "\r\n\r\n") - (*msg)) - 4);

    cur_size = received + content_len;
    (*msg) = realloc((*msg), cur_size);

    // Read body
    do
    {
        bytes_read = read(socket, (*msg) + received, cur_size - received);
        received += bytes_read;

        if (bytes_read < 0)
            err_n_exit("Read failed");

        if (bytes_read == 0)
            break;
    } while (received < cur_size);
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