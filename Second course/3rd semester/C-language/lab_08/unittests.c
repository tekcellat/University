#include <stdio.h>
#include <string.h>
#include <conio.h>
#include "func.h"


void startTest();
void testSumCase1();
void testSumCase2();
void testProductCase1();
void testProductCase2();
void testReverseCase1();
void testReverseCase2();
void eqMatrix(double *matrix1, double *matrix2, int n, int m);

int main(void){
    startTest();
    getch();
    return 0;
}

void startTest(){
    printf("Test of summ function. \n");
    testSumCase1();
    testSumCase2();
    printf("Test of product function. \n");
    testProductCase1();
    testProductCase2();
    printf("Test of reverse function. \n");
    testReverseCase1();
    testReverseCase2();
}

void testSumCase1(){
    double matrixTest1[] = {1, 2, 3, 4};
    double matrixTest2[] = {1, 3, 2, 4};
    double testResult[] = {2, 5, 5, 8};

    double *result;
    result = (double*)malloc(4 * sizeof(double));
    
    findSum(matrixTest1, matrixTest2, 2, 2, result);
    eqMatrix(result, testResult, 2, 2);
}

void testSumCase2(){
    double matrixTest1[] = {8, 4, 3, 5};
    double matrixTest2[] = {3, 2, 5, 4};
    double testResult[] = {11, 6, 8, 9};
    

    double *result;
    result = (double*)malloc(4 * sizeof(double));

    findSum(matrixTest1, matrixTest2, 2, 2, result);
    eqMatrix(result, testResult, 2, 2);
}

void testProductCase1(){
    double matrixTest1[] = {1, 2, 3, 4};
    double matrixTest2[] = {1, 3, 2, 4};
    double testResult[] = {5, 11, 11, 25};

    double *result;
    result = (double*)malloc(4 * sizeof(double));
    
    findProduct(matrixTest1, matrixTest2, 2, 2, 2, 2, result);
    eqMatrix(result, testResult, 2, 2);
}

void testProductCase2(){
    double matrixTest1[] = {5, 7, 2, 3};
    double matrixTest2[] = {6, 1, 2, 3, 9, 5};
    double testResult[] = {51, 68, 45, 21, 29, 19};

    double *result;
    result = (double*)malloc(2*3 * sizeof(double));
    
    findProduct(matrixTest1, matrixTest2, 2, 2, 2, 3, result);
    eqMatrix(result, testResult, 3, 2);
}

void testReverseCase1(){
    double matrixTest[] = {2, 4, 6, 2};
    double testResult[] = {0.500000, -2.000000, -3.000000, 0.500000};
    double result[] = {1, 0, 0, 1}; // Matrix E

    findReverseMatrix(matrixTest, result, 2, 2);
    eqMatrix(result, testResult, 2, 2);
}

void testReverseCase2(){
    double matrixTest[] = {10, 20, 4, 8};
    double testResult[] = {0.100000, -2.500000, -0.400000, 0.125000};
    double result[] = {1, 0, 0, 1}; // Matrix E

    findReverseMatrix(matrixTest, result, 2, 2);
    eqMatrix(result, testResult, 2, 2);
}

void eqMatrix(double *test, double *result, int n, int m){
    int flag = 0;
    for (int i = 0; i < n*m; i++)
        if (*(test+i) != *(result+i))
            flag = 1;
    if (flag == 0) printf("Test done. \n");
    else printf("Error. \n");
}