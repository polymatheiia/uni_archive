/* Zajecia WI, gr. 5, prowadzacy: Marcin Szczuka
Wyliczanie i operacje na wierszach w pliku tekstowym */

#include <stdio.h>
#include <ctype.h>
#include<string.h>
#define DL_NAZPLIKU 30 /* maksymalna dlugosc nazwy pliku */
#define TRUE 1 /* do symulacji .......... */
#define FALSE 0 /* ... wartosci logicznych. */

void najdluzszy_wiersz_przy_pomocy_fgets() {
    FILE * we;
    we = fopen ("dane.txt", "rt");
    int biezacyWiersz = 0;
    int najdluzszyWiersz = -1;
    int dlugoscNajdluszego = -1;
    while(!feof(we))
    {
        biezacyWiersz++;
        char s[10000];
        fgets(s, sizeof(s), we);
        int biezacaDlugosc = strlen(s);
        if (biezacaDlugosc > 0 && s[biezacaDlugosc - 1] == '\n') biezacaDlugosc--;
        //printf("wiersz %d, dlugosc %d\n", biezacyWiersz, biezacaDlugosc);
        if (biezacaDlugosc > dlugoscNajdluszego) {
            najdluzszyWiersz = biezacyWiersz;
            dlugoscNajdluszego = biezacaDlugosc;
        }
    }
    printf("Najdluzszy  wiersz %d, dlugosc %d\n", najdluzszyWiersz, dlugoscNajdluszego);
    fclose(we);
    }

void najdluzszy_wiersz() {
    FILE *f=fopen("dane.txt","rt");
    if (f==NULL) {
        fprintf(stderr, "nie udalo sie otworzyc pliku!\n");
        return;
    }
    int biezacyWiersz = 1;
    int najdluzszyWiersz = 1;
    int dlugoscNajdluszego = 0;
    int x =0;
    char c;
    while((c = fgetc(f)) != EOF) {
        if(c=='\n')
        {
          if(x > dlugoscNajdluszego)
          {
              dlugoscNajdluszego = x;
              najdluzszyWiersz = biezacyWiersz;
          }
            biezacyWiersz= biezacyWiersz + 1;
            x = 0;
        } else {
            x = x + 1;
        }
    }
    printf("najdluzszy wiersz %d, dlugosc %d\n", najdluzszyWiersz, dlugoscNajdluszego);
    fclose(f);

}

void najdluzsze_slowo() {
    FILE *f=fopen("dane.txt","rt");
    if (f==NULL) {
        fprintf(stderr, "nie udalo sie otworzyc pliku!\n");
        return;
    }

    char c;
    int dlugoscNajdluszego=0, l=0, wewnatrzSlowa=0;
    int MAX=1000;
    char biezaceSlowo[MAX];
    char najdluzszeSlowo[MAX+1];
    while((c = fgetc(f)) != EOF)
    {
        if (c=='\n' || c==' ') {
            if (wewnatrzSlowa==1 && l > dlugoscNajdluszego) {
                dlugoscNajdluszego=l;
                for(int i=0;i<l;i++) najdluzszeSlowo[i]=biezaceSlowo[i];
                najdluzszeSlowo[l]=0;
            }
            wewnatrzSlowa=0;
            l=0;
        } else {
            wewnatrzSlowa=1;
            if (l<MAX) {
                biezaceSlowo[l]=c;
                l++;
            }
        }
    }

    fclose(f);
    printf("dlugosc najdluzszego slowa: %d\n", dlugoscNajdluszego);
    printf("najdluzsze slowo: %s\n", najdluzszeSlowo);
}

void najwiecej_slow() {
    FILE *f=fopen("dane.txt","rt");
    if (f==NULL) {
        fprintf(stderr, "nie udalo sie otworzyc pliku!\n");
        return;
    }
    int licznik=0, maxlicznik=0, wslowie=FALSE;
    char c;
    while((c = fgetc(f)) != EOF)
      if (isalpha(c))
        {
        if(wslowie == FALSE)
            {//Poczatek slowa
              licznik += 1;
  wslowie = TRUE;
            }
  }
  else
  {
     wslowie = FALSE;
       if(c == '\n')
     {//Koniec linii
            if(licznik > maxlicznik)
          maxlicznik = licznik;
        licznik = 0;
      }
  }
fclose(f);
printf ("Najwieksza liczba slow w jednej linii pliku wynosi %d.\n",maxlicznik);

 return 0;
}




main() {

najdluzszy_wiersz_przy_pomocy_fgets();
najdluzszy_wiersz();
najdluzsze_slowo();
najwiecej_slow();
}



