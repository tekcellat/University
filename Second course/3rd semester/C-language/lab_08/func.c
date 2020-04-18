#include <stdio.h>
#include <stdlib.h>
#include <malloc.h>
#include "func.h"
#include "error.h"
#include <string.h>


void readArray(double *matrix, FILE *f, int n, int m){
    for (int i = 0; i < n; i++)
    	for (int j = 0; j < m; j++)
    		fscanf(f, "%lf", (matrix + i*m + j));
}

void findSum(double *matrix, double *matrix2, int n, int m, double *result){
	for (int i = 0; i < m; i++)
		for (int j = 0; j < n; j++){
			*(result + i*n + j) = *(matrix + i*n + j) + *(matrix2 + i*n + j);
		}
}

void print(double *result, int n, int m){
	FILE *f2;
	f2 = fopen("out.txt","w");
	for (int i = 0; i < m; i++){
		for (int j = 0; j < n; j++)
			fprintf(f2, "%lf  ", *(result + i*n + j));
		fprintf(f2, "\n");
	}
	fclose(f2);
}

void findProduct(double *matrix, double *matrix2, int m, int m2, int n, int n2, double *result){
	for (int i = 0; i < n; i++){
		for (int j = 0; j < n2; j++){
			*(result + i*n2 + j) = 0;
			for (int k = 0; k < m; k++){
				*(result + i*n2 + j) = *(result + i*n2 + j) + *(matrix + i*m + k) * *(matrix2 + n2*k + j);
			}
		}
	}
}

void findReverseMatrix(double *matrix, double *matrixE, int n, int m){
	for (int k = 0; k < n; k++){
		for (int i = k; i < n; i++){
			*(matrixE + k*n + i) = *(matrixE + k*n + i) / *(matrix + k*n + k);
			*(matrix + k*n + i) = *(matrix + k*n + i) / *(matrix + k*n + k);
		}

		for (int i = k + 1; i < n; i++)
			for (int j = k; j < n; j++){
				*(matrixE + i*n + j) = *(matrixE + i*n + j) - *(matrixE + k*n + j) * *(matrix + i*n + k);
				*(matrix + i*n + j) = *(matrix + i*n + j) - *(matrix + k*n + j) * *(matrix + i*n + k);
			}
	}
	for (int k = n-1; k > -1; k--){
		for (int i = k - 1; i > -1; i--)
			for (int j = k; j > i; j--){
				*(matrixE + i*n + j) = *(matrixE + i*n + j) - *(matrixE + k*n + j) * *(matrix + i*n + k);
				*(matrix + i*n + j) = *(matrix + i*n + j) - *(matrix + k*n + j) * *(matrix + i*n + k);
			}
	}
}

void mainFunction(FILE *f, char **action){
	int n = 0;
    int m = 0;
    fscanf(f, "%d", &m);
    fscanf(f, "%d", &n);

    double *matrix;
	matrix = (double*)malloc(n*m * sizeof(double));

	readArray(matrix, f, n, m);
	if (strcmp(*(action), "1") == 0){
		if (n == m){
			double *matrixE;
			matrixE = (double*)malloc(n*m * sizeof(double));
			for (int i = 0; i < n; i++)
				for (int j = 0; j < n; j++)
					if (i == j) *(matrixE + i*n + j) = 1.0;
					else *(matrixE + i*n + j) = 0.0;
			findReverseMatrix(matrix, matrixE, n, m);
			print(matrixE, n, m);
		}
	}
	else if (strcmp(*(action), "2") == 0){
		int n2 = 0;
    	int m2 = 0;

    	fscanf(f, "%d", &n2);
	    fscanf(f, "%d", &m2);

    	if ((n == m2) && (m == n2)){
	    	
			double *matrix2;
			matrix2 = (double*)malloc(n2*m2 * sizeof(double));
			readArray(matrix2, f, n2, m2);

			double *result;
			result = (double*)malloc(m*n * sizeof(double));
			findSum(matrix, matrix2, m, n, result);
			print(result, m, n);
		}
		else { printf("Error. Matrix size does not match (m & n).");}
	}
	else{
		int n2 = 0;
    	int m2 = 0;
    	fscanf(f, "%d", &n2);
    	fscanf(f, "%d", &m2);
    	if (m == m2){
			double *matrix2;
			matrix2 = (double*)malloc(n2*m2 * sizeof(double));
			readArray(matrix2, f, n2, m2);

			double *result;
			result = (double*)malloc(n2*n * sizeof(double));
			findProduct(matrix, matrix2, m, m2, n, n2, result);
			print(result, n2, n);
		}
		else { printf("Error. Matrix size does not match (m & n)."); }
	}
	fclose(f);
}

