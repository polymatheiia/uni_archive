/* Zajecia WI, gr. 5, prowadzacy: Marcin Szczuka
Szablon programu do operowania na plikach tekstowych
Zawiera wiele komentarzy i nadmiarowych elementow */


#include <stdio.h>
#include <ctype.h>
#define DL_NAZPLIKU 30 /* maksymalna dlugosc nazwy pliku */
#define TRUE 1 /* do symulacji .......... */
#define FALSE 0 /* ... wartosci logicznych. */

main() {

char nazwapliku[DL_NAZPLIKU+1]; /* nazwa przetwarzanego pliku */
FILE * we ; /* wskaznik do przetwarzanego pliku */
char c ; /* biezacy znak */
int liczby[26], /* liczniki liter, zakladamy ze mamy tylko 26 */
    numl, /* numer litery w alfabecie */
    lbrazem, /* liczba wszystkich odczytanych znakow*/
    lbinnych, /* liczba znakow spoza alfabetu */
    lbslow, /* licznik slow - slowo to ciag dowolnych znakow zakonczony spacja lub koncem linii*/
    lbwierszy, /* licznik wierszy */
    w_slowie, /* znacznik znalezienia slowa */
    i ; /* iterator */
/* pobieramy nazwe pliku do przetwarzania */
/* Uwaga: tryb otwarcia do czytania to czasem r lub rb zamiast rt */
/* Tryb rt oznacza plik otwarty do czytania (r=read) w trybie tekstowym (t) */
/* Ponizsza petla sluzy zabezpieczeniu sie przed sytuacja nieprawidlowej nazwy pliku / nieistnienia pliku */
do
    { printf ("podaj nazwe pliku do odczytu: ") ;
      gets (nazwapliku) ; /* funkcja gets() pobiera napis (string = tablica elementow typu char) ze standardowego wejscia czyli klawiatury */
      if ( ( we = fopen (nazwapliku, "rt")) == NULL)
      printf ("***** nie ma takiego pliku\n") ;
    }
while (we == NULL);
/* Jezeli nie dbamy o zabezpieczenia to wystarczy zrobic: we = fopen (nazwapliku, "rt"); */

/* inicjalizacje zmiennych */
for (i=0 ; i<26 ; i++) liczby[i]=0;
lbrazem = 0;
lbinnych = 0;
lbslow = 0;
lbwierszy = 0;
w_slowie = FALSE;

/* petla odczytu i badania znakow z tekstu, liczenia slow i (koncow) linii */
while (c = fgetc (we), ! feof (we) ) /* ten warunek petli wymusza czytanie jednego znaku z pliku i jednoczesne sprawdzanie czy plik sie nie skonczyl
    Alternatywa jest czytanie */
  {
    if (c == '\n') lbwierszy++; /* sprawdzamy czy przeczytany znak jest koncem linii, jesli tak - zwiekszamy licznik linii, jesli nie - idziemy dalej*/
    else
      { lbrazem++ ; /* zwiekszamy licznik znaków "wlasciwych" w pliku; */
        numl = tolower(c) -'a' ;/* funkcja tolower() zwraca mala litere odpowiadaj¹ca argumentowi, my liczymy duze i male tak samo */
        if (numl >=0 && numl <= 26) liczby[numl]++ ;
        else lbinnych++ ;
      }
    if (c ==' '|| c=='\0') /*tu sprawdzamy czy slowo sie konczy, w tym kontekscie koniec linii odpowiada '\0' */
        { if (w_slowie)
            { lbslow++;
              w_slowie = FALSE;
            }
        }
    else w_slowie = TRUE;
  }
/* wyprowadzenie wynikow */
printf("\n tekst zawiera %d wierszy, %d slow\n", lbwierszy, lbslow);
printf("oraz %d znakow w tym:\n", lbrazem);
for (i=0 ; i<26 ; i++)
printf("%d razy litere %c\n", liczby[i], 'a'+i);
printf("\ni %d innych znakow\n", lbinnych) ;
fclose(we);
}



/*Uwagi dodatkowe:
Zalo¿ono, ze przetwarzany plik jest rzeczywiscie plikiem tekstowym, tj. konczy siê znakiem koñca wiersza. Je¿eli tak nie jest, to:
-ostatni wiersz nie jest liczony;
-ostatnie s³owo tak¿e nie jest liczone, je¿eli nie ma za nim spacji.
*/
