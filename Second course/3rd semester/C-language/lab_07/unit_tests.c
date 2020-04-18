#include <stdio.h>
#include <stdlib.h>
#include <conio.h>
#include <malloc.h>
#include <string.h>
#include "func.h"
#include "error.h"


void testFilter();
void testBinarySort();


int main(int argc, char * argv[]){
	testFilter();
	testBinarySort();

    getch();
    return 0;
}

void testBinarySort(){
	//initial data
	int *test;								
	test = (int*)malloc(7 * sizeof(int));
    *(test+0) = 4;
    *(test+1) = 5;
    *(test+2) = 35;
    *(test+3) = 2;
    *(test+4) = 1;
    *(test+5) = 6;
    *(test+6) = 4;
    int *test2;
	test2 = (int*)malloc(5 * sizeof(int));
	*(test2+0) = 1;
	*(test2+1) = 4;
	*(test2+2) = -3;
	*(test2+3) = 4;
	*(test2+4) = -5;

	int *arrayFilterTestSort;
    arrayFilterTestSort = (int*)malloc(7 * sizeof(int));
	*(arrayFilterTestSort+0) = 1;
	*(arrayFilterTestSort+1) = 2;
	*(arrayFilterTestSort+2) = 4;
	*(arrayFilterTestSort+3) = 4;
	*(arrayFilterTestSort+4) = 5;
	*(arrayFilterTestSort+5) = 6;
	*(arrayFilterTestSort+6) = 35;

	int *arrayTestSort2;
	arrayTestSort2 = (int*)malloc(5 * sizeof(int));
	*(arrayTestSort2+0) = -5;
	*(arrayTestSort2+1) = -3;
	*(arrayTestSort2+2) = 1;
	*(arrayTestSort2+3) = 4;
	*(arrayTestSort2+4) = 4;

	int flag = 1;
	binarySort(test, 7);
	for (int i = 0; i < 7; i++){
		if (*(test+i) != *(arrayFilterTestSort + i))
			flag = 0;
	}
	if (flag == 1) printf("Test (sort of array with filter) is correct.\n");
	else printf("Error. Test incorrect.\n");

	binarySort(test2, 5);
	for (int i = 0; i < 5; i++){
		if (*(test2+i) != *(arrayTestSort2 + i))
			flag = 0;
	}
	if (flag == 1) printf("Test (sort of array with filter) is correct.\n");
	else printf("Error. Test incorrect.\n");
}
void testFilter(){
	//Initial data
	int *test3;								
	test3 = (int*)malloc(8 * sizeof(int));
    *(test3+0) = 1;
    *(test3+1) = 2;
    *(test3+2) = 4;
    *(test3+3) = 4;
    *(test3+4) = 5;
    *(test3+5) = 6;
    *(test3+6) = 35;
    *(test3+7) = 3;
    int *test4;
	test4 = (int*)malloc(8 * sizeof(int));
    *(test4+0) = 1;
    *(test4+1) = 4;
    *(test4+2) = -3;
    *(test4+3) = 4;
    *(test4+4) = -5;
    *(test4+5) = 3;
    *(test4+6) = 2;
    *(test4+7) = 3; 

    int *arrayFilterTest;
    arrayFilterTest = (int*)malloc(7 * sizeof(int));
    *(arrayFilterTest+0) = 1;
    *(arrayFilterTest+1) = 2;
    *(arrayFilterTest+2) = 4;
    *(arrayFilterTest+3) = 4;
    *(arrayFilterTest+4) = 5;
    *(arrayFilterTest+5) = 6;
    *(arrayFilterTest+6) = 35;
	int *arrayFilterTest2;
	arrayFilterTest2 = (int*)malloc(5 * sizeof(int));
	*(arrayFilterTest2+0) = 1;
	*(arrayFilterTest2+1) = 4;
	*(arrayFilterTest2+2) = -3;
	*(arrayFilterTest2+3) = 4;
	*(arrayFilterTest2+4) = -5;

	int *filterArray;
	filterArray = (int*)malloc(7 * sizeof(int));
	int *filterArray2;
	filterArray2 = (int*)malloc(5 * sizeof(int));

	int flag = 1;
	filter(filterArray, 7, test3);
	for (int i = 0; i < 7; i++){
		if (*(filterArray+i) != *(arrayFilterTest + i))
			flag = 0;
	}
	if (flag == 1) printf("Test (filter array function) is correct.\n");
	else printf("Error. Test incorrect.\n");

	flag = 1;
	filter(filterArray2, 5, test4);
	for (int i = 0; i < 5; i++){
		if (*(filterArray2+i) != *(arrayFilterTest2 + i))
			flag = 0;
	}
	if (flag == 1) printf("Test (filter array function) is correct.\n");
	else printf("Error. Test incorrect.\n");
}