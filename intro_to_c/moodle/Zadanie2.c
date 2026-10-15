//Zadanie 2
//Imiê: Danuta
//Nazwisko: Grabovska

#include<stdio.h>
#include<stdlib.h>
int max_licznik = 0; //licznik dla najdłużczej serii
int dlugosc_najdl_serii(){
    FILE *f =fopen("dane.txt", "r");
    if (f==NULL){
        fprintf(stderr, "nie udalo sie otworzyc pliku!\n");
        return 0;
    }
    int porown[2]; //tablica dla zapisywania 2 sąsiednich znaków
    porown[0]=0;
    porown[1]=0;
    int tmp_licznik = 1; //licznik bieżącej serii
    char c;
    while((c = fgetc(f)) != EOF){
        if (c=='\n') continue;
        porown[0]=porown[1];
        porown[1]=c;
        if (porown[0]==porown[1]) tmp_licznik++;
        else {
            if(max_licznik<tmp_licznik) max_licznik=tmp_licznik;
            tmp_licznik=1;
        }
    }
    //powtórka dla c=EOF
    porown[0]=porown[1];
    porown[1]=c;
    if (porown[0]==porown[1]) tmp_licznik++;
    else {
        if(max_licznik<tmp_licznik) max_licznik=tmp_licznik;
        tmp_licznik=1;
    }
    fclose(f);
    return max_licznik;
}

int main(){
    printf("Dlugosc najdluzszej serii takich samych znakow wynosi %d\n", dlugosc_najdl_serii());
    return 0;
}
