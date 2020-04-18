#include <stdio.h>
#include <stdlib.h>
#include <conio.h>
#include <malloc.h>
#include <string.h>
#include "func.h"
#include "error.h"


int main(int argc, char * argv[]){
	if (argc < 2){
		printf("ERROR");
		getch();
   		return 1;
	}
    FILE *f;
    f = fopen(argv[1],"r");
    int quantity = findQuantity(f);
    int *array;
	array = (int*)malloc(quantity * sizeof(int));
    rewind(f);
	readArray(array, f, quantity);
    fclose(f);
    if (argc > 3){
		if (strcmp(argv[3], "2") == 0){
			qsort(array, quantity, sizeof(int), cmpfunc);
			printArray(array, quantity);
		}
		else{
			int quantityFilter = findQuantityFilter(array, quantity);
			int *filterArray;
			filterArray = (int*)malloc(quantityFilter * sizeof(int));
			filter(filterArray, quantityFilter, array);
			binarySort(filterArray, quantityFilter);
			if (strcmp(argv[2], "0") == 0)
				printArray(filterArray, quantityFilter);
			else
				printReverse(filterArray, quantityFilter);
		}
    }
    else{
		binarySort(array, quantity);
		if (strcmp(argv[2], "0") == 0)
			printArray(array, quantity);
		else
			printReverse(array, quantity);
	}
    return 0;
}