#include <stdio.h>
#include <stdlib.h>
#include "func.h"
#include "error.h"

int main(int argc, char const *argv[])
{
    const char* search = argv[4];
    const char* replace = argv[6];

    FILE* f = fopen(argv[1], "r");
    FILE* f_out = fopen(argv[2], "w");
    my_getline(f, f_out, search, replace);

    fclose(f);
    fclose(f_out);
    return 0;
}