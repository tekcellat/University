#include "common.h"

void err_n_exit(const char *fmt, ...)
{
    int errno_save;
    va_list ap;

    // All sys calls can set errno, so we need to save it now
    errno_save = errno;

    va_start(ap, fmt);

    vfprintf(stdout, fmt, ap);
    fprintf(stdout, "\n");
    fflush(stdout);

    // Print out error message if errno was set
    if (errno_save != 0)
    {
        fprintf(stdout, "(errno = %d): %s\n", errno_save,
                strerror(errno_save));
        fprintf(stdout, "\n");
        fflush(stdout);
    }

    va_end(ap);

    exit(EXIT_FAILURE);
}

char *alloc(uint32_t size)
{
    char *str = (char *)malloc(size);
    if (str == NULL)
        err_n_exit("Alloc memory failed");
    return str;
}