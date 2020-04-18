#ifndef H_FUNC
#define H_FUNC


#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int my_strlen(const char* source);
char* my_replace(const char *source, const char *search, const char *replace);
void my_getline(FILE *f, FILE *f_out, const char *search, const char *replace);

#endif