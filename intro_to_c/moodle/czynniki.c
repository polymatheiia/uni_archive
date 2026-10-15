#include <stdio.h>
int main()
{ int a,i,j;
  printf("To jest program wyliczający dzielniki i rozkład na czynniki pierwsze\n ");
  printf("Podaj liczbe calkowita z zakresu 1-1000 i nacisnij Enter:");
  scanf("%d",&a);
  printf("\n Rozklad na czynniki pierwsze %d = ",a);
  i=a;
  j=2;
  while(i>1)
        {
                while(i%j==0) //dopóki liczba i jest podzielna przez j
                {
                        printf("%d ",j);
                        i=i/j;
                }
                j++;
        }
 printf("\n Wszystkie dzielniki %d to: ",a);
for(int i=1;i<=a;i++)
    if (a%i==0) printf("%d, ",i);

 printf("\n Rozne czynniki pierwsze w rozkladzie %d to: ",a);
  i=a;
  j=2;
  while(i>1)
        {
                if (i%j==0)  printf("%d ",j);
                while(i%j==0) //dopóki liczba i jest podzielna przez j
                {
                       i=i/j;
                }
                j++;
        }

    return 0;
}
