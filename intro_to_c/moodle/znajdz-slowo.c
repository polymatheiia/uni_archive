/* Zajecia WI, gr. 5, prowadzacy: Marcin Szczuka
Program rozwiązujący 1 zadanie domowe */

#include <stdio.h>
#include <ctype.h>
#include<string.h>
#define DL_NAZPLIKU 30 /* maksymalna dlugosc nazwy pliku */
#define BUFFERSIZE /*maksymalna długość stringu wczytywanego z pliku*/
#define TRUE 1 /* do symulacji .......... */
#define FALSE 0 /* ... wartosci logicznych. */


main() {

char nazwapliku[DL_NAZPLIKU+1]; /* nazwa przetwarzanego pliku */
char slowo[DL_NAZPLIKU+1];/*szukane slowo/imię */
FILE * we ; /* wskaznik do przetwarzanego pliku */
char c ; /* biezacy znak */
int dlslowa=0,licznik=1,czyjest=FALSE;

do
    { printf ("podaj nazwe pliku do odczytu: ") ;
      gets (nazwapliku) ; /* funkcja gets() pobiera napis (string = tablica elementow typu char) ze standardowego wejscia czyli klawiatury */
      if ( ( we = fopen (nazwapliku, "rt")) == NULL)
      printf ("***** nie ma takiego pliku\n") ;
    }
while (we == NULL);

    printf ("podaj slowo do wyszukania: ") ;
    gets(slowo);
    dlslowa=strlen(slowo);

    while (c = fgetc (we), ! feof (we) )
{
    if (tolower(c) == tolower(slowo[licznik])) licznik++; //uzywamy tolower by nie zwracac uwagoi na duze/male litery
    else licznik = 1;
    //if (licznik == dlslowa) czyjest = TRUE; //wersja nie sprawdzajaca czy slowo jest samodzielne
     if (licznik == dlslowa)  //wersja sprawdzajaca czy slowo jest samodzielne
      if ((fgetc (we)=='\n')||(fgetc (we)==' '))
        czyjest = TRUE;
}


/* wyprowadzenie wynikow */
if (czyjest) printf("Slowo %s wystepuje w pliku %s.\n",slowo,nazwapliku);
else printf("Slowo %s nie wystepuje w pliku %s.\n",slowo,nazwapliku);
fclose(we); // na konic zamykamy plik
}


