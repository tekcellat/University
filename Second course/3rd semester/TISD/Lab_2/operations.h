#ifndef _OPERATIONS_H
#define _OPERATIONS_H

#include "struct.h"

#define SUCCESS 0
#define INPUT_ERROR -3
#define MEMORY_ALLOCATION_ERROR -5
#define NOTHING_DELETED -6
#define NOTHING_FOUND -7

int add_record(struct information** inform, int* const n);
int delete_record(struct information** inform, const char* const deleted_country, int* const n);
void write(FILE *f, const struct information* const array, const int n);
void print(const struct information* const array, const int n);
int find_country(struct information* array, const int n, char *continent, char *tourism_type);

#endif