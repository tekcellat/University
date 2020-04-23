
#include <stdio.h>
#include <unistd.h>

#define BUFFSIZE 0x1000

int main(int argc, char *argv)
{
    char buffer[BUFFSIZE];
    FILE *f;
    int len;
    
    f = fopen("/proc/self/cmdline", "r");
    len = fread(buffer, 1, BUFFSIZE, f);
    buffer[--len] = 0;
    
    printf("cmdline for %d \nprocess = %s\n", getpid(), buffer);
    fclose(f);
    
    return 0;
}



