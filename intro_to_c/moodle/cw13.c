#include <stdio.h>
#include <assert.h>

char znakHex(int d) {
  // d=0 -> '0'
  // d=9 -> '9'
  // d=10 -> 'A'
  // d=15 -> 'F'
  assert(d>=0 && d<16);
  if (d>=10) return 'A'+(d-10);
  else return '0'+d;
}

void wypiszHex(char *filename) {
  // wypisz zawartosc pliku "filename" w kodzie szesnastkowym
  // po 16 znaków w wierszu, n.
  // 50 AF 5E 50 AF 5E 50 AF 5E 50 AF 5E 5E 50 AF 5E
  // 50 AF 5E 50 AF 5E 50 AF 5E 50 AF 5E 5E 50 AF 5E
  // AA EE 0A
  FILE *f=fopen(filename, "r"); 
  if (f==NULL) {
    printf("nie mozna otworzyc pliku: %s\n", filename);
    return;
  }
  char c;
  int i=0;
  while ((c=fgetc(f))!=EOF) {
    i++;
    char h1=znakHex(c/16);
    char h2=znakHex(c%16);
    printf("%c%c ", h1, h2);
    if (i%16==0) printf("\n");
  }
  printf("\n");
  fclose(f);
}

int liczbaPodciagow3(int a[], int n) {
  // tablica a[i] zawiera liczby {0,1,2}
  // ile jest roznych rosnacych podciagow 3-elementowych w a
  // (roznych w sensie indeksów wybranych elementów)
  // jeśli chodzi o wartości to wszystkie ciagi mają
  // wartosc=(0,1,2)
  // dla a={0,0,1,1,2,2} -> wynik=8
  // oczekiwana złożoność O(n)
  // dla a={1,1,0,0,2,2} -> wynik=0
  // wynik = | { (i, j, k) : 0<=i < j < k <= n-1 && a[i]=0 && a[j]==1 && a[k]==2} |

  // ile0(i) = {ile jest wartości 0 w przedziale 0..i}
  // ile0(i) = ile0(i-1) + (a[i]==0 ? 1 : 0)
  // ile01(i) = {ile jest różnych podciągów {0,1} w przedziale 0..i}
  // ile01(i) = ile01(i-1) + (a[i]==1 ? ile0(i-1) : 0)
  // ile012(i) = {ile jest różnych podciągów {0,1,2} w przedziale 0..i}
  // ile012(i) = ile012(i-1) + (a[i]==2 ? ile01(i-1) : 0)

  int ile0[n], ile01[n], ile012[n];
  ile0[0] = a[0]==0 ? 1 : 0;
  // notacja:
  // (WARTOSC_LOGICZNA ? WARTOSC_1 : WARTOSC 2)
  // jest rownowazna:
  // if (WARTOSC_LOGICZNA) 
  //    return WARTOSC_1
  // else
  //    return WARTOSC_2
  for(int i=1;i<n;i++) {
    ile0[i] = ile0[i-1] + (a[i]==0 ? 1 : 0);
    // if (a[i]==0) ile0[i] = ile0[i-1] + 0
    // else ile0[i] = ile0[i-1] + 1
  }

  ile01[0] = 0;
  for(int i=1;i<n;i++) {
    ile01[i] = ile01[i-1] + (a[i]==1 ? ile0[i-1] : 0);
  }

  ile012[0] = 0;
  for(int i=1;i<n;i++) {
    ile012[i] = ile012[i-1] + (a[i]==2 ? ile01[i-1] : 0);
  }

  return ile012[n-1];
  
  // alternatywne rozwiazanie
  // for(int i=1;i<n-1;i++) {
  //    if (a[i]==1) 
  //       wynik += #{liczba 0 w przedziale 0..(i-1)} * #{liczba 2 w przedziale (i+1)..n-1}
  // }
}

int liczbaPodciagow3alt(int a[], int n) {
  int ile0=0;
  int ile2=0;
  for(int i=0;i<n;i++) if (a[i]==2) ile2++;
  int wynik=0;
  for(int i=0;i<n;i++) {
    // niezmiennik, 
    // ile0 oznacza liczbe 0 w przedziale 0..(i-1)
    // ile2 oznacza liczbe 2 w przedziale i..(n-1)
    switch(a[i]) {
      case 0:
        ile0++;
        break;
      case 1:
        wynik += ile0 * ile2;
        break;
      case 2:
        ile2--;
        break;
    }
  }
  return wynik;
}

int znajdz_najmn(int a[], int od, int n)
{
  int m, indeks=od;
  m=a[od];
  for(int i=od+1; i<n; i++)
  {
    if(a[i]<m)
    {
      m=a[i];
      indeks=i;
    }
  }
  return indeks;
}

void uporzadkujTablice(int a[], int n, int k) {
  // czesciowo uporzadkuj tablice a (poprzestawiaj elementy w a), 
  // tak żeby po tej procedurze:
  // dla i=0..k a[i] <= a[k]
  // dla i=k+1..n-1 a[k] <= a[i]
  // oczekiwana zlozoność: O(n*k)
  int indeks, pom;
  for(int i=0; i<=k; i++)
  {
    indeks=znajdz_najmn(a, i, n);
    pom=a[indeks];
    a[indeks]=a[i];
    a[i]=pom;
  }
}

/**

Dana jest tablica n liczb całkowitych, w której dwie liczby występują ponad n/3 razy. Napisz funkcję, która zwróci większą z tych liczb. Np. dla tablicy 
A = [2, 3, 4, 5, 4, 5, 2, 5, 5, 5, 8, 4, 4, 5, 4, 4, 2] 
funkcja powinna zwrócić liczbę 5.

znajduje element który występuje > n/3 razy jeśli istnieje

kand1 = -1, licznik1=0
kand2 = -1, licznik2=0
for(i=0;i<n;i++) {
  if (a[i]==kand1) licznik1++;
  else if (a[i]==kand2) licznik2++;
  else if (licznik1==0) {
    kand1=a[i];
    licznik1++;
  } else if (licznik2==0) {
    kand2=a[i];
    licznik2++;
  } else {
    licznik1--;
    licznik2--;
  }
}
// hipoteza: po wyjsciu z algorytmu jeśli element występuje
// co najmniej n>3 razy to będzie to kand1 lub kand2
// trzeba policzyc ile razy wystepuje kand1 i kand2



-> rozwiązanie sprytne O(n)
-> rozwiązanie brutalne O(n^2)


Napisz funkcję typu void, która wartości n-elementowej (n>0) tablicy liczb całkowitych A, uporządkowanej niemalejąco, przepisze do tablicy B tak, aby tablica B była posortowana po wartościach bezwzględnych w sposób niemalejący. Elementy tablicy A o tych samych wartościach bezwzględnych mogą występować w tablicy B w dowolnej kolejności. Na przykład dla tablicy 
A = [−7, −4, −3, 0, 2, 5, 8] 
funkcja powinna zwrócić tablicę 
B = [0, 2, −3, −4, 5, −7, 8] .
Rozwiązanie powinno mieć złożoność czasową nie większą niż O(n).
*/


int main(void) {
  wypiszHex("dane.txt");
  int a[] = {0,0,0,1,1,2,2};
  printf("liczbaPodciagow3=%d\n", liczbaPodciagow3(a, 7));
  printf("liczbaPodciagow3alt=%d\n", liczbaPodciagow3alt(a, 7));
  int b[] = {10,5,7,1,2,0,3,4,6,9,8};
  printf("przed: ");
  for(int i=0;i<11;i++) printf("%d ", b[i]);
  printf("\n");
  uporzadkujTablice(b, 11, 5);
  printf("po: ");
  for(int i=0;i<11;i++) printf("%d ", b[i]);
  printf("\n");
  return 0;
}
