
#include<stdio.h>
#include<string.h>


// FILE typ danych służący do obsługi plików
// FILE *f = fopen(nazwa, tryb) - otwieranie pliku
// fclose(f) - zamykanie
// fprintf(f, format, agrumenty) - odpowiednik printf
// fscanf(f, format, argumenty) - odpowiednik scanf
// char c = fgetc(f) - wczytanie znaku
// feof(f) - sprawdzenie czy doszliśmy do końca pliku
// stałe EOF '\n' '\t'

void zadanie5_3_liczby_pierwsze(int n) {
    int A[n+1];
    for(int i=0;i<=n;i++) A[i] = 0;
    FILE *f = fopen("pierwsze.txt", "w");
    if (f==NULL) {
        // stdin, stdout, stderr
        fprintf(stderr, "nie udało się otworzyć pliku!\n");
        return;
    }
    for(int i=2; i<n+1; i++)
    {
        for(int j = 2*i; j<n+1; j+=i)
        {
            A[j]=1;
        }
    }
  
    for(int i=2; i<n+1; i++)
    {
        if(A[i]==0) fprintf(f, "%d\n", i);
    }
    fclose(f);
}

void zadanie5_5_liczba_znakow() {
    int n=0;
    FILE *f=fopen("dane.txt","r");
    if (f==NULL) {
        fprintf(stderr, "nie udało się otworzyć pliku!\n");
        return;
    }
    while(fgetc(f)!=EOF)
    {
        n++;
    }
    printf("%d\n",n);
    fclose(f);
}

// man fgets
void zadanie5_6_najdluzszy_wiersz_przy_pomocy_fgets() {
    FILE *f=fopen("dane.txt","r");
    if (f==NULL) {
        fprintf(stderr, "nie udało się otworzyć pliku!\n");
        return;
    }
    int biezacyWiersz = 0;
    int najdluzszyWiersz = -1;
    int dlugoscNajdluszego = -1;
    while(!feof(f)) {
        biezacyWiersz++;
        char s[10000];
        fgets(s, sizeof(s), f);
        int biezacaDlugosc = strlen(s);
        if (biezacaDlugosc > 0 && s[biezacaDlugosc - 1] == '\n') biezacaDlugosc--;
        printf("wiersz %d, dlugosc %d\n", biezacyWiersz, biezacaDlugosc);
        if (biezacaDlugosc > dlugoscNajdluszego) {
            najdluzszyWiersz = biezacyWiersz;
            dlugoscNajdluszego = biezacaDlugosc;
        }
    }
    printf("najdluzszyWiersz %d, dlugosc %d\n", najdluzszyWiersz, dlugoscNajdluszego);
    fclose(f);
    
}

void zadanie5_6_najdluzszy_wiersz() {
    FILE *f=fopen("dane.txt","r");
    if (f==NULL) {
        fprintf(stderr, "nie udało się otworzyć pliku!\n");
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
    printf("najdluzszyWiersz %d, dlugosc %d\n", najdluzszyWiersz, dlugoscNajdluszego);
    fclose(f);
    
}

void zadanie5_7_liczba_znakow_a() {
    int n=0;
    FILE *f=fopen("dane.txt","r");
    if (f==NULL) {
        fprintf(stderr, "nie udało się otworzyć pliku!\n");
        return;
    }
    char c;
    while((c = fgetc(f)) !=EOF)
    {
        if (c == 'a') {
            n++;
        } 
    }
    printf("%d\n",n);
    fclose(f);
}


// if (c >= 'b') ...
void zadanie5_8_liczba_malych_liter() {
    int n = 0;
    FILE *f=fopen("dane.txt","r");
    if (f==NULL) {
        fprintf(stderr, "nie udało się otworzyć pliku!\n");
        return;
    }
    
    char c;
    while((c = fgetc(f)) != EOF)
    {
        if('a' <= c && c <='z'){
            n++;
        }
    }
    
    fclose(f);
    printf("%d\n",n);
}

void zadanie5_9_liczba_slow() {
    FILE *f=fopen("dane.txt","r");
    if (f==NULL) {
        fprintf(stderr, "nie udało się otworzyć pliku!\n");
        return;
    }
    
    char c;
    int liczbaSlow=0, wewnatrzSlowa=0;
    while((c = fgetc(f)) != EOF)
    {
        if (c=='\n' || c==' ') {
            wewnatrzSlowa=0;
        } else {
            if (wewnatrzSlowa==0) liczbaSlow++;
            wewnatrzSlowa=1;
        }
    }
    
    fclose(f);
    printf("liczba slow: %d\n", liczbaSlow);
}

void zadanie5_11_najdluzsze_slowo() {
    FILE *f=fopen("dane.txt","r");
    if (f==NULL) {
        fprintf(stderr, "nie udało się otworzyć pliku!\n");
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


int main() {
    
    zadanie5_3_liczby_pierwsze(100);
    zadanie5_5_liczba_znakow();
    zadanie5_6_najdluzszy_wiersz();
    zadanie5_7_liczba_znakow_a();
    zadanie5_8_liczba_malych_liter();
    zadanie5_9_liczba_slow();
    zadanie5_11_najdluzsze_slowo();
    return 0;
    
}