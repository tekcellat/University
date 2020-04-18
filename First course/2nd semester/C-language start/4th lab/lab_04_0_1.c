#include <stdio.h>
#define MAX_SIZE 10
#define LEN 100

int main()
{
    int arr[MAX_SIZE];
    int i, n, e=0;
    char str[LEN];
    char name[LEN] = {"Sum of even elements of array = %d"};
    FILE *file_in;
    FILE *file_out;
    file_in = fopen("in_0.txt", "r");
    file_out = fopen("out_0.txt", "a");

    printf("Enter size of the array: ");
    scanf("%d", &n);
    if(n<11)
    {
        printf("Enter %d elements in the array: ", n);
        for(i=0; i<n; i++)
        {
            scanf("%d", &arr[i]);
        }
        for(i=0; i<n; i++)
        {
            if(arr[i]%2==0)
                e=e+arr[i];   
        }
        if(file_in != NULL && file_out != NULL)
        {
            while(fgets(str, LEN, file_in))
                fprintf(stdout, "%s", str);
            fputs(name, file_out);
            printf("Sum of even elements of array = %d", e);
            return 0;
        }
        else
        {
            fprintf(stderr, "Cannot be open  any .txt file\n");
            return 1;
        }
    }
    else
        puts("Not right size of array");
}