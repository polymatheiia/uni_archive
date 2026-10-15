#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int NWD(int a,int b)
{   if (a == 0)
       return b;
    if (b == 0)
       return a;
    while (a!=b)
    {
        if(a>b)
            a-=b; // a=a-b
        else
            b-=a; // b=b-a
    }
    return a;
}

int NWD2(int a,int b)
{
    if (a == 0)
        return b;
    if (b == 0)
       return a;

    return NWD2(b % a, a);
}

double sredniaAR(int a ,int b)
{
    double c;
    c=(double)(a+b)/2;
    return c;
}

int main()
{
    int a,b;
    printf("Podaj dwie liczby calkowite dodatnie oddzielone spacja i nacisninij Enter\n");
    scanf("%d%d",&a, &b);
    printf("Najwiekszy wspolny dzielnik %d i %d to %d\n",a,b,NWD(a,b));
    printf("Najwiekszy wspolny dzielnik %d i %d to %d\n",a,b,NWD2(a,b));
    printf("Srednia arytmetyczna %d i %d to %f\n",a,b,sredniaAR(a,b));

return 0;
}
