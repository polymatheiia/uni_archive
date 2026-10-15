/**
 * Plan zajęć
 * 
 * Zadanie 1
 * 
 * Wczytaj z pliku dane.txt dwie nieujemne liczby całkowite (max 1000 cyfr)
 * Policz ich sumę i wypisz wynik.
 * 
 * Zadanie 2
 * 
 * Wypisz wartości pierwszych 200 liczb Fibonacciego
 */
#include <stdio.h>

#define MAX_DL 1000
typedef int Liczba[MAX_DL]; 
// -> teraz można używać typu Liczba który jest równoważny z int[MAX_DL]
// jeśli Liczba A=1234, to tablica zawiera:
// [4,3,2,1,0,0,0,0,...]
// val(A) = \sum_{i=0}^{MAX_DL-1} 10^i * A[i]

void zerujLiczbe(Liczba A) {
  for (int i = 0; i < MAX_DL; ++i) A[i] = 0;
}

void wczytajLiczbe(FILE *f, Liczba A) {
  char c;
  int i = 0;
  zerujLiczbe(A);
  while ((c = fgetc(f)) != EOF)
  {
    if (c <= '9' && c >= '0')
    {
      A[i] = c - '0'; // konwertuje znak c na wartość liczbową
    } else {
      break;
    }
    ++i;
  }

  for (int j = 0; j < i; ++j , --i)
  {
    int tmp = A[j];
    A[j] = A[i - 1];
    A[i - 1] = tmp;
  }
}

int dlugoscLiczby(Liczba A) {
  // jeśli A=1234, czyli [4,3,2,1,0,0,0,0,0] -> funkcja zwraca 3
  // jeśli A=1000, czyli [0,0,0,1,0,0,0,0,0] -> funkcja zwraca 3
  // jeśli A=1, czyli [1,0,0,0,0,0,0] -> funkcja zwraca 0
  // jeśli A=0, czyli [0,0,0,0,0,0,0] -> funkcja zwraca 0
  int i = MAX_DL - 1;
  while (i > 0 && A[i] == 0){
    i--;
  }
  return i;
}

void wypiszLiczbe(Liczba A) {
  for (int i = dlugoscLiczby(A); i >=0; i--){
    printf ("%d", A[i]);
  }

  printf("\n");
}

void dodajLiczby(Liczba A, Liczba B, Liczba C) {
  // C := A + B
  int plusJeden = 0;
  for (int i = 0; i < MAX_DL; ++i)
  {
    int tmp = A[i] + B[i] + plusJeden;
    if (tmp > 9)
    {
      C[i] = tmp - 10;
      plusJeden = 1;
    } else {
      C[i] = tmp;
      plusJeden = 0;
    }
  }
}

void zadanieProsteDodawanie() {
  Liczba A, B, C;
  FILE *f = fopen("dane.txt", "r");
  wczytajLiczbe(f, A);
  wczytajLiczbe(f, B);
  fclose(f);

  printf("A="); wypiszLiczbe(A);
  printf("B="); wypiszLiczbe(B);
  dodajLiczby(A, B, C);
  printf("C="); wypiszLiczbe(C);
}

void kopiujLiczbe(Liczba A, Liczba B) {
  // A := B
  for (int i=0;i<MAX_DL;i++){
    A[i]=B[i];
  }
}

void liczbyFib(int n) {
  // Fib(1)=1
  // Fib(2)=1
  // Fib(3)=2
  // ...
  // Fib(100)=354224848179261915075
  /*int f0=0;
  int f1=1;
  for(int i=1;i<=n;i++) {
    printf("fib(%d)=", i);
    printf("%d", f1);
    printf("\n");
    int f=f0+f1;
    f0=f1;
    f1=f;
  }
  */
  Liczba f1 = {1}, f0 = {0}, f;
  for (int i = 1;i<=n;i++){
    printf("fib(%d)=", i);
    wypiszLiczbe (f1);
    // printf("\n");
    dodajLiczby (f1,f0,f);
    kopiujLiczbe(f0, f1);
    kopiujLiczbe(f1, f);
  }
}

int main(void) {
  zadanieProsteDodawanie();
  liczbyFib(200);
  return 0;
}