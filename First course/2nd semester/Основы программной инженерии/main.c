
#include <stdio.h> 

int main()
{
    FILE *mf;
    char str[50];
    char *estr;
    mf = fopen ("opi_homewrok.txt","r");
    FILE *file_w;
    file_w = fopen("answer.txt","w");

    // Проверка открытия файла
    if (mf == NULL) {printf ("Error\n"); return -1;}
    else printf ("Successfull\n");


    //Чтение (построчно) данных из файла в бесконечном цикле
    while (1)
    {

        estr = fgets (str,sizeof(str),mf);
        while (bin != 0)
        {
            remainder = bin % 10;
            hex = hex + remainder * i;
            i = i * 2;
            bin = bin / 10;
        }
        printf("Equivalent hexadecimal value: %lX", hex);
        fprintf(file_w,"%lX",&hex);
        if (estr == NULL)
        {
            if ( feof (mf) != 0)
            {  
                printf ("\nEnd of file\n");
                break;
            }
            else
            {
                printf ("\nError file reads\n");
                break;
            }
        }
        printf ("     %s",str);
    }

    if ( fclose (mf) == EOF) printf ("Error\n");

    return 0;
} 