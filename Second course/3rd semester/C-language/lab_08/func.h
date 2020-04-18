#ifndef H_FUNC
#define H_FUNC


#include <stdio.h>
#include <stdlib.h>
#include <malloc.h>
#include <string.h>

//чуть-чуть комментариев

void readArray(double *matrix, FILE *f, int n, int m);
void findSum(double *matrix, double *matrix2, int n, int m, double *result);
void findProduct(double *matrix, double *matrix2, int m, int m2, int n, int n2, double *result);
void print(double *result, int n, int m);
void findReverseMatrix(double *matrix, double *matrixE, int n, int m);
void mainFunction(FILE *f, char **action);


#endif