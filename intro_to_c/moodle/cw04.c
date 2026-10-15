#include<stdio.h>

void cw04_3() {
    int a,b;
    scanf("%d%d",&a,&b);
    printf("suma=%d\n", a+b);
    printf("roznica=%d\n", a-b);
    printf("iloczyn=%d\n", a*b);
}

void cw04_4_sito(int n) {
    int pierwsza[n+1];
    for(int i=2;i<=n;i++) pierwsza[i]=1;
    for(int i=2;i<=n;i++) if (pierwsza[i]) {
        printf("%d\n", i);
        int j=i+i;
        while(j<=n) {
            pierwsza[j]=0;
            j+=i;
        }
    }
}

void cw04_5_czynniki_pierwsze(int n) {
    printf("%d = ", n);
    if (n==0 || n==1) printf("%d", n);
    int i=2, ile=0;
    while(n>1) {
        while(n%i==0) { 
            if (ile>0) printf("*");
            printf("%d",i);
            ile++;
            n=n/i; 
        }
        i++;
    }
    printf("\n");
}

void cw04_5_czynniki_pierwsze2(int n) {
    printf("%d = ", n);
    if (n==0 || n==1) printf("%d", n);
    long long i=2;
    while(i*i<=n) {
        while(n%i==0) { 
            printf("%lld",i);
            n=n/i; 
            if (n>1) printf("*");
        }
        i++;
    }
    if (n>1) printf("%d", n);
    printf("\n");
}

void cw04_6_dzielniki(int n) {
    printf("dzielniki %d =", n);
    for(int i=1;i<=n;i++) {
        if (n%i==0) printf(" %d", i);
    }
    printf("\n");
}

void cw04_7_rozne_dzielniki_pierwsze(int n) {
    printf("dzielniki pierwsze %d =", n);
    long long i=2;
    while(i*i<=n) {
        if (n%i==0) printf(" %d", i);
        while(n%i==0) n=n/i;
        i++;
    }
    if (n>1) printf(" %d", n);
    printf("\n");
}

void swap(int *a, int *b) {
    int c=*a;
    *a=*b;
    *b=c;
}

void cw04_8_sortuj(int arr[], int n) {
    printf("przed sortowaniem:");
    for(int i=0;i<n;i++) printf(" %d", arr[i]);
    printf("\n");
    for(int i=1;i<n;i++) {
        int j=i;
        while(j>0 && arr[j]<arr[j-1]) {
            swap(&arr[j], &arr[j-1]);
            j--;
        }
    }
    printf("po sortowaniu:");
    for(int i=0;i<n;i++) printf(" %d", arr[i]);
    printf("\n");
}


int main() {
    //cw04_3();
    cw04_4_sito(100);
    cw04_5_czynniki_pierwsze(5*5*7*11);
    cw04_5_czynniki_pierwsze2(5*5*7*11);
    cw04_6_dzielniki(2*2*2*3*3*5);
    cw04_7_rozne_dzielniki_pierwsze(2*2*2*3*3*5);
    int arr[] = {1,7,2,6,3,5,4};
    cw04_8_sortuj(arr,7);

    return 0;
}