#include <stdio.h>
#include <stdlib.h>
#include <string.h>
//#include <math.h>
#include <ctype.h>

#define ZAKRES 1000

// Tu powinny byc deklaracje funkcji

int main()
{
  int a; int i;
  int T[ZAKRES];
  FILE* plik;
  plik=fopen("wyniki.txt","w");

  printf("To jest program na sito Eratostenesa.\n ");
  printf("Podaj liczbe calkowita z zakresu 2-999 i nacisnij Enter:");
  scanf("%d",&a);
  for(i=0;i<a;i++) T[i]=1; // wypełniamy tablicę jedynkami
  for (int i=2; i*i<a; i++)
    if (T[i]==1)
    for (int j=2; i*j<a; j++) T[i*j]=0;
    // pod T[i] mamy 1 gdy i jest liczba  pierwsza, w przeciwnym wypadku 0
    for (int i=2; i<a; i++)
    {
    if (T[i]==1) fprintf(plik,"%d - pierwsza\n", i);
    else fprintf(plik,"%d - zlozona\n", i);
    }
    fclose(plik);
return 0;
}
