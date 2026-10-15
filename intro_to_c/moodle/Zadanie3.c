// Zadanie 3
//Imiê: Danuta
//Nazwisko: Grabovska

#include<stdio.h>
#include<stdlib.h>
#include<time.h>
#define N 20

int a[N];
void wpisz_tablice(int a[N])
{
    int i;
    srand(time(NULL));
    a[0]= (rand() % 20)-10;
    for (i=1;i<N;i++)
        a[i]=a[i-1]+(rand() % 3)+1;
}
int L=0;
int dl_najdl_sp_frag(){
    int uj=0; //liczba elebentów ujemnych
    int dod=0; //liczba elementów dodatnich
    int zero=0; //indykator obecności zera w tablicy
    int lok_0=0; //lokacja zera w tablicy
    for (int i=0;i<N;i++){
        if (a[i]<0) uj++;
        if (a[i]>0) dod++;
        if (a[i]=0){
            zero=1;
            lok_0=i;
        }
    }
    if (uj%2==0 && zero==0) L=N;
    if (uj%2==1 && zero==0) L=N-1;
    if (zero==1 && dod>uj) L=dod;
    if (zero==1 && uj%2==0 && uj>=dod) L=uj;
    if (zero==1 && uj%2==1 && uj-1>=dod) L=uj-1;
    return L;
}
void wypisz_tablice(int a[N])
{
    int i;
    for(i=0;i<N;i++)
        printf("%5d",a[i]);
    printf("\n");
}

int main()
{
    wpisz_tablice(a);
    wypisz_tablice(a);
    printf("Dlugosc najdluzszego spojnego fragmentu o dodatnim iloczynie wynosi %d\n", dl_najdl_sp_frag());
    return 0;
}
