// Zadanie 4
//Nazwisko: Grabovska

#include<stdio.h>
#include<stdlib.h>
#include<time.h>
#define N 30

int a[N];
void wpisz_tablice01(int a[N])
{
    int i;
    srand(time(NULL));
    for (i=0;i<N;i++)
        a[i]=rand() % 2;
}
int licznik=0;
int liczba_par(int k){
    if (k<=1|k>N){
        printf ("Liczba k nie jest zgodna z trescia zadania!");
        return 0; //sprawdzamy czy 1<k<=N
    }
    int i=0;
    int j=0;
    int end=N;
    while (a[i]==0){
        //sprawdzamy tylko pary, gdzie i-k<j<i+k
        // czyli i-k+1<=j<=i+k-1
        if ((i-k+1)>0){
            j=i-k+1;
        }
        if ((i+k-1)<N){
            int end=i+k-1;
        }
        for (j; j<end;j++){
            if (a[j]==1) licznik++;
        }
        i++;
    }
    return licznik;
}
void wypisz_tablice(int a[N])
{
    int i;
    for(i=0;i<N;i++)
        printf("%d ",a[i]);
    printf("\n");
}

int main()
{
    wpisz_tablice01(a);
    printf("Liczba takich par wynosi %d\n", liczba_par(3));
    wypisz_tablice(a);
    return 0;
}
