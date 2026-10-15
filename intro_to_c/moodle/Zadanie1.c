//Zadanie 1
//Imiê: Danuta
//Nazwisko: Grabovska

#include<stdio.h>
#include<stdlib.h>

long long f(int n){
    //rozwiązanie iteracyjne
    int tab[n];
    tab[0]=0;
    tab[1]=1;
    tab[2]=2;
    for (int i=0;i<n+1;i++) {
        if (i<3) tab[i]=i;
        else tab[i]=tab[i-1]-2*tab[i-2]+tab[i-3]+1;
    }
    return tab[n];
}

int main(){
    printf("Wartosc funkcji f wynosi %d\n", f(4));
    return 0;
}

