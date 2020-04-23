#include <stdio.h>
#include <string.h>

#define BUFFSIZE 0x1000

int main(int argc, char *argv)
{
    char buffer[BUFFSIZE];
    int len;
    FILE *f;
    
    f = fopen("/proc/self/stat","r");
    fread(buffer, 1, BUFFSIZE, f);
    char* p_ch = strtok(buffer, " ");
    
    printf("stat: \n");
    
    while (p_ch != NULL)
    {
        printf("%s \n", p_ch);
        p_ch = strtok(NULL, " ");
    }
    
    fclose(f);
    return 0;
}

