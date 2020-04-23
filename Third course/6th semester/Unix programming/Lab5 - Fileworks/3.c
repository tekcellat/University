#include <stdio.h>

int main()
{
    FILE *f1;
    FILE *f2;

    f1 = fopen("alphabet.txt","w");
    f2 = fopen("alphabet.txt","w");
    int flag;
    for (char c = 'a'; c <= 'z'; c++)
    {
        if (!flag)
            fprintf(f1, "%c", c);

        if (!flag)
            fprintf(f2, "%c", c);
        flag = !flag;
    }
    fclose(f1);
    fclose(f2);

    return 0;
}
