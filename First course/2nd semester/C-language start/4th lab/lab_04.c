#include<stdio.h>
#define MAX_SIZE 10

int even_elements();
int second();
int palindrome();
int sort();
void array();
int func();

int main()
{
    int size_array , res, i, arr[MAX_SIZE];
    printf("How many number you want to enter ?\n");
    res=scanf("%d", &size_array);
    if( size_array <= 2 || size_array > 10 || res!=1 )
    {
        printf("Not right size of array! ");
    }
    else
    {
        printf("Enter %d Numbers :", size_array);
        for (i = 0; i < size_array; i++)
            scanf("%d", &arr[i]);
        printf("\nSum of even elements: %d",even_elements(size_array, i, arr));
        printf("\n\nNew array is: %d ",second(size_array, i, arr));
        palindrome(size_array, i, arr);
        sort(size_array, i, arr);
    }
    return 0;
}


int even_elements(int size_array, int i, int arr[MAX_SIZE])
{
    int e=0;
    if(size_array<11)
    {
        for(i=0; i<size_array; i++)
        {
            if(arr[i]%2==0)
                e = e +arr[i]; 
        }
    }
    return e;
}

int second(int size_array, int i, int arr[MAX_SIZE])
{
    int sum = 0, size=0, b[11];
    for (i = 0; i < size_array; i++)
            sum = sum + arr[i];

    int average = sum / size_array;
    for (i = 0; i < size_array; i++)
    {
        if (arr[i] > average)
        {
            b[size] = arr[i];
            size++;
        }
    }
    return b[0];
}

int palindrome(int size_array, int i, int arr[MAX_SIZE])
{
    int temp;
    for (i = 0; i < size_array; i++)
    {
        int reverse = 0;
        temp = arr[i];
        while( temp != 0 )
        {
            reverse = reverse * 10;
            reverse = reverse + temp%10;
            temp = temp/10;
        }
        if ( arr[i] == reverse ) 
            printf("\n%d is a palindrome number.\n", arr[i]);
        else 
            printf("\n%d is not a palindrome number.\n", arr[i]);
    }
}

int sort(int size_array, int i, int arr[MAX_SIZE]) 
{
    int j, temp = 0;
    for (i = 0; i < size_array; i++)
    {
        for (j = i + 1; j < size_array; j++)
        {
            if (arr[i] > arr[j])
            {
                temp = arr[i];
                arr[i] = arr[j];
                arr[j] = temp;
            }
        }
    }       
    printf("\nThe sorted array using Buble sort is:\n"); 
    array(size_array, i, arr);
}

void array(int size_array, int i, int arr[MAX_SIZE])
{
    for (i = 0; i < size_array; i++)
        printf("%d ", arr[i]);

}

void func(int size_array, int i, int arr[MAX_SIZE]){
    int ret; int ret_2=0;
    for(i=0; i<size_array; i++ )
        printf("size is:%d", ret_2);
}