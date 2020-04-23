#include <stdio.h>
#define BUFFSIZE 0x1000

int main(int argc, char* argv[])
{
    char buffer[BUFFSIZE];
    int len;
    int i;
    FILE* f;
    
    f = fopen("/proc/self/environ","r");
    while ((len = fread(buffer, 1, BUFFSIZE, f)) > 0)
    {
        for (i = 0; i < len; i++)
            if (buffer[i] == 0)
                buffer[i] = 10;
        buffer[len - 1] = 10;
        
        printf("%s", buffer);
    }
    
    fclose(f);
    return 0;
}

