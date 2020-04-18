#ifndef MYSORT_H
#define MYSORT_H

#include "struct.h"

#define SUCCESS 0
#define MEMORY_ALLOCATION_ERROR -5 

int sort_table(struct information* array, int n, int *const time_bubble, int *const time_qsort);
void mysort(void *base, size_t num, size_t size,  int (*compare)(const void *, const void *));
void swap(void *, void *, int);
unsigned long long tick(void);
int compare_string(const void *a, const void *b);
int sort_key_array(struct information* array, int n, int **p, int *const time_bubble, int *const time_qsort);
int compare_key(const void *a, const void *b);

#endif