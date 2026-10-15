#include <stdio.h>
#include <stdlib.h>

int main()
{
    const int k = 10; // elementami tablicy T są liczby całkowite z
                              // z przedziału 0..76
const int n = 50;
int T[n]; // tablica zawierająca elementy do posortowania
int Tp[n]; // tablica zawierająca elementy posortowane
int TPom[k]; // zawiera liczbę elementów o danej wartości

int i; // zmienna pomocnicza
srand(1234); // seedujemy generator pseudolosowy

  for(i = 0 ; i < k ; ++i)
    TPom[i] = 0;                // zerowanie tablicy liczników

  for(i=0;i<n;i++) T[i]=rand()%k; //wypełnienie ciągu losowymi liczbami z zakresu 0-(K-1)
    printf("Ciag wejsciowy:\n ");
    for(i=0;i<n;i++) printf("%d, ", T[i]);

  for(i = 0 ; i < n ; ++i)
    ++TPom[T[i]];               // po tych operacjach TPom[i] będzie zawierała
                                // liczbę wystąpień kolejnego elementu o wartości T[i]
  for(i = 1 ; i < k ; ++i)
    TPom[i] += TPom[i-1];       // teraz TPom[i] zawiera pozycje w posortowanej
                                // tablicy ostatniego elementu o kluczu i
  for(i = n-1 ; i >= 0 ; --i)
     Tp[--TPom[T[i]]] = T[i];   // wstawienie elementu na odpowiednią pozycję
                                // i aktualizacja TPom
    printf("\nCiag wyjsciowy:\n ");
    for(i=0;i<n;i++) printf("%d, ", Tp[i]);

  return 0;
}
