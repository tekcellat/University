#include <stdio.h>
#include <math.h>

void input(double *, double *);
double calculate(const double, const double);

int main()
{
    double x, eps, sum, sumA;
    input(&x, &eps);
    if (x == 0)
    {
        printf("S(x) = %f\n", 0);
        printf("f(x) = %f\n", 0);
        printf("Abs. Err.: %f\n", 0);
        printf("Don't have: Rel. Err.");
    }
    else
    {
        sum = calculate(x, eps);
        sumA = asin(x);
        printf("S(x) = %f\n", sum);
        printf("f(x) = %f\n", sumA);
        printf("Abs. Err.: %f\n", fabs(sum - sumA));
        printf("Rel. Err.: %f\n", fabs((sum - sumA) / sumA));
    }
    return 0;
}

void input(double *x, double *eps)
{
    printf("Input x: ");
    int reads;    char a;
    do
    {
        while (((reads = scanf("%lf%c", x, &a)) != 2 && reads != EOF) || a != '\n')
        {
            printf("Please enter again, right number: ");
            // read at least one character until the next newline
            do
            {
                reads = scanf("%c", &a);
            } while (reads != EOF && a != '\n');
        }
        if (fabs(*x) > 1)
            printf("Please input x in interval [-1, 1]: ");
    } while (fabs(*x) > 1);

    printf("Input epsilon: ");
    while (((reads = scanf("%lf%c", eps, &a)) != 2 && reads != EOF) || a != '\n')
    {
        printf("Please enter again, right number: ");
        // read at least one character until the next newline
        do
        {
            reads = scanf("%c", &a);
        } while (reads != EOF && a != '\n');
    }
}

double calculate(const double x, const double eps)
{
    if (x == 0)
    {
        return 0;
    }
    double resT = 0;
    double tempn = x;
    double num = -1;
    double dominator = 0;
    while (tempn > eps)
    {
        resT += tempn;
        num += 2;
        dominator += 2;
        tempn = tempn * pow(x, 2) * pow(num, 2) / (dominator * (dominator + 1));
    }
    return resT;
}