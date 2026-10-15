#include <stdio.h>

int main()
{ int i,n;
printf("To jest pierwszy program!\n ");
printf("Hello World!\n");
printf("Podaj liczbe z zakresu 1-10 i nacisnij Enter:");
scanf("%d",&n);
for(i=0;i<n;i++)
    printf("\n Witaj swiecie po raz %d ",i+1);
return 0;
}
