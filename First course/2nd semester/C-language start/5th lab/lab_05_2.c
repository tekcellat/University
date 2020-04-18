#include <stdio.h>
#include <string.h>
#define MAX_SIZE 100


int *read_file(FILE *file_r,int *arr);
int File_Error(FILE *file);
int solve_task(int *arr, int *end);


int main(){
    //char file_name[15];
    FILE *file_r = fopen("file_name.txt","r");

    if(File_Error(file_r) == 0){
        int arr[MAX_SIZE];
        int *pend = read_file(file_r,arr);
        fclose(file_r);
        if(arr != pend) printf("Answer is = %d", solve_task(arr, pend));

        else printf("Please fill in the file, it is empty");

    }
    else printf("Cannot found file!!!");

    return 0;
}


int *read_file(FILE *file_r,int *arr){
    int *temp = arr,count = 0;
    for(count = 0; count<=MAX_SIZE && fscanf(file_r, "%d", temp) == 1; count++, temp++);

    if(count != 0 && count != 1) temp--;

    return temp;
}


int solve_task(int *arr, int *end){
    int max = *(arr) + *(end), temp;
    while(arr <= end){
        temp = *(arr) + *(end);
        arr++;
        end--;
        if(temp > max) max = temp;

    }
    return max;
}


int File_Error(FILE *file){
    int Input_Error = 0, Return_Error = 0;
    if (file == NULL){
        fprintf(stderr, "Error opening file: %s\n", strerror( Input_Error ));
        Return_Error = -1;

    }

    return Return_Error;

}