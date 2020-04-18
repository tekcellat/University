#include <stdio.h>
#include <math.h>

int solve(float x, float y, float x1, float y1, float y2, float x2);

int main()
{
    //Ввод данных
    float x,y,x1,y1,y2,x2;
    prfloatf("Write first coords(x1 and y1): ");
    scanf("%f %f",&x,&y);
    prfloatf("Write second coords(x2 and y2): ");
    scanf("%f %f",&x1,&y1);
    prfloatf("Write pofloat coords(x and y): ");
    scanf("%f %f",&x2,&y2);

    solve(x, y, x1, y1, y2, x2);
    return 0;
}

int solve(float x, float y, float x1, float y1, float y2, float x2) 
{ 
    
    if ((x-x1)/(x2-x1)==(y-y1)/(y2-y1))
        prfloatf("Pofloat in line");
    else
        prfloatf("pofloat out line");
    return 0;
}