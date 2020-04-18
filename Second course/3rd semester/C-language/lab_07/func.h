#ifndef H_FUNC
#define H_FUNC


#include <stdio.h>
#include <stdlib.h>
#include <conio.h>
#include <malloc.h>


int cmpfunc (const void * a, const void * b);
void printReverse(int *array, int quantity);
int findQuantity(FILE *f);
int readArray(int *array, FILE *f, int quantity);
void binarySort(int *array, int quantity);
void printArray(int *array, int quantity);
void filter(int *filterArray, int quantity, int *array);
int findQuantityFilter(int *array, int quantity);


#endif