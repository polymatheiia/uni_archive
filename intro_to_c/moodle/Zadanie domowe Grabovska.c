#include<stdio.h>
#include<assert.h>

long long fib_rek(int n){
    if (n==0) return 0;
    if (n==1) return 1;
    if (n<0){
        printf("Prosimy o wprowadzenie liczby nieujemnej \n");
        return 0;
        }
    else return fib_rek(n-1)+fib_rek(n-2);
    }

long long fib_dyn(int n){
    if (n==0) return 0;
    if (n==1) return 1;
    if (n<0){
        printf("Prosimy o wprowadzenie liczby nieujemnej \n");
        return 0;
        }
    long long F[n];
    F[0]=0;
    F[1]=1;
    for (int i=2;i<=n;i++) F[i]=F[i-1]+F[i-2];
    return F[n];
    }

int main(){
    printf("%d-ty wyraz ciagu Fibonacciego (rekurencyjnie) stanowi %lld\n",42, fib_rek(42));
    printf("%d-ty wyraz ciagu Fibonacciego (dynamicznie) stanowi %lld\n",100, fib_dyn(100));
    return 0;
    }
