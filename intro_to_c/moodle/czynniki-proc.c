#include <stdio.h>

void Cpierwsze (int n)
{
  printf("\n Rozklad na czynniki pierwsze %d = ",n);
  int i=n;
  int j=2;
  while(i>1)
        {
                while(i%j==0) //dopóki liczba i jest podzielna przez j
                {
                        printf("%d ",j);
                        i=i/j;
                }
                j++;
        }

}

void Dzielniki (int n)
{printf("\n Wszystkie dzielniki %d to: ",n);
for(int i=1;i<=n;i++)
    if (n%i==0) printf("%d, ",i);
}

void Rpierw (int n)
{
    printf("\n Rozne czynniki pierwsze w rozkladzie %d to: ",n);

  int i=n;
  int j=2;
  while(i>1)
        {
                if (i%j==0)  printf("%d ",j);
                while(i%j==0) //dopóki liczba i jest podzielna przez j
                {
                       i=i/j;
                }
                j++;
        }
}



int main()
{ int a;
  printf("To jest program wyliczajacy dzielniki i rozklad na czynniki pierwsze\n ");
  printf("Podaj liczbe calkowita z zakresu 1-1000 i nacisnij Enter:");
  scanf("%d",&a);

  Cpierwsze(a);
  Dzielniki(a);
  Rpierw(a);

    return 0;
}
