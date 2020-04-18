#include <stdio.h>
#include <stdlib.h>
 
int main()
{
    int N = 0, CurrentCounter = 0, BiggestCounter = 0, FrequentEl = 0;
//CurrentCounter - текущее число повторений
//BiggestCounter - наибольшее число повторений
//FrequentEl - наиболее часто встречающийся элемент
    int * Array = NULL;
    printf("Input N = ");
    scanf("%d", &N);
    Array = (int*)malloc(N*sizeof(int));
    if(Array == NULL)
    {
        return 1;
    }
//Забиваем массив псевдослучайными числами
    for(int i = 0; i < N; i++)
    {
        Array[i] = rand()%N;
        printf("%d ", Array[i]);
    }
    printf("\n");
    
    for(int i = 0; i < N; i++)
    {
        for(int j = i; j < N; j++)
        {
            if(Array[i] == Array[j])
            {
                 CurrentCounter++;
            }
        }
        if(CurrentCounter > BiggestCounter)
        {
             BiggestCounter = CurrentCounter;
             FrequentEl = Array[i];
        }
        CurrentCounter = 0;
    }
    printf("Element = %d\n", FrequentEl);
    return 0;
}