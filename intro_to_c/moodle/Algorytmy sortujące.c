#include <stdio.h>
#include <stdlib.h>
#include <time.h>

typedef long long lint; //definiujemy long long jako int w celu ułatwienia zapisu i odczytu

#define QUICK 0
#define HEAP 1
#define INSERT 2
#define MERGE 3
#define MAX_SORTS 4

int min(int a, int b);
void QuickSort(lint a[], lint min, lint max);
void merge(lint a[], lint l, lint m, lint r);
void MergeSort(lint a[], lint l, lint r);
void InsertSort(lint a[], lint rozmiar);
void kopcuj(lint a[], lint i, lint j);
void buduj_kopiec(lint a[], lint rozmiar);
void HeapSort(lint a[], lint rozmiar);

lint *randomArr(lint len);
lint *increasingArr(lint len);
lint *decreasingArr(lint len);
void reverseArr(lint arr[], lint len);
void arrCpy(lint *dest, lint *source, lint len);
void sortPerformance(lint arr[], lint len, float results[]);
void wynikTestu(float results[]);


int main(){
    srand(time(0));
    float wyniki[MAX_SORTS]; //tablica dla zapisywania czasu wykonywania algorytmów
    lint rozmiar; //rozmiar tablicy do posortowania
    lint *tab;
    char wybor; //dla wprowadzenia monotoniczności ciągu

    printf("Wprowadz rozmiar danych do posortowania (max.: 200 000):\n");
    //liczba 200 000 została wyznaczona eksperymentalnie: dla większych liczb występuje sygnał SIGSEGV
    scanf("%lld", &rozmiar);
    printf("Wprowadz monotoniczność (r - rosnacy, m - malejacy, l - losowy):\n");
    scanf(" %c", &wybor);

    switch(wybor){
        case 'r':
            tab = increasingArr(rozmiar); //sortowanie tablicy o losowych wartościach
            break;
        case 'm':
            tab = decreasingArr(rozmiar); //sortowanie i odwrócenie tablicy o losowych wartościach
            break;
        case 'l':
            tab = randomArr(rozmiar); //przyswojenie tablicy o rozmiarze dynamicznym losowych wartości
            break;
        default:
            fprintf(stderr, "Prosze wprowadzic poprawne dane!");
            exit(1);
    }
    sortPerformance(tab, rozmiar, wyniki);
    //wyznacza czas wykonywania od razu wszystkich algorytmów
    wynikTestu(wyniki);
    //porównuje i wypisuje czas wykonywania

    free(tab);

    exit(0);
}
int min(int a, int b){ //ta funkcja szuka minimum wśród wyników algorytmów w procedurze wynikTestu()
    return a<b ? a : b;
}
void QuickSort(lint a[], lint min, lint max){ //algorytm sortowania szybkiego
    long long i, j, pivot, temp;

    if(min < max){
        pivot=min;
        i = min;
        j = max;

        while(i < j){
            while(a[i] <= a[pivot] && i < max)
                i++;
            while(a[j] > a[pivot])
                j--;
            if(i < j){
                temp = a[i];
                a[i] = a[j];
                a[j] = temp;
            }
        }

        temp = a[pivot];
        a[pivot] = a[j];
        a[j] = temp;
        QuickSort(a, min,j - 1);
        QuickSort(a,j + 1, max);
    }
}

void merge(lint a[], lint l, lint m, lint r){ //element algorytmu sortowania przez scalanie
    lint i, j, k;
    lint n1 = m - l + 1;
    lint n2 =  r - m;

    lint L[n1], R[n2];

    for (i = 0; i < n1; i++)
        L[i] = a[l + i];
    for (j = 0; j < n2; j++)
        R[j] = a[m + 1+ j];

    i = 0;
    j = 0;
    k = l;
    while (i < n1 && j < n2){
        if (L[i] <= R[j]){
            a[k] = L[i];
            i++;
        }
        else{
            a[k] = R[j];
            j++;
        }
        k++;
    }
    while (i < n1){
        a[k] = L[i];
        i++;
        k++;
    }
    while (j < n2){
        a[k] = R[j];
        j++;
        k++;
    }
}

void MergeSort(lint a[], lint l, lint r){ //algorytm sortowania przez scalanie
    if (l < r){
        lint m = l+(r-l)/2;

        MergeSort(a, l, m);
        MergeSort(a, m+1, r);

        merge(a, l, m, r);
    }
}

void InsertSort(lint a[], lint rozmiar) { //algorytm sortowania przez scalanie
    lint i, j;
    lint wartosc;

    for (i = 1; i < rozmiar; i++) {
        wartosc = a[i];
        for (j = i - 1; j >= 0 && a[j] > wartosc; j--) {
            a[j + 1] = a[j];
        }
        a[j + 1] = wartosc;
    }

}

void kopcuj(lint a[], lint i, lint j){ //element algorytmu sortowania przez kopcowanie
    lint k,x;
    if ((2 * i + 1 < j) && (a[i] < a[2 * i + 1])){
        k = 2 * i + 1;
    }
    else{
        k = i;
    }
    if ((2 * i + 2 < j) && (a[k] < a[2 * i + 2])){
        k = 2 * i + 2;
    }
    if (i != k){
        x = a[i];
        a[i] = a[k];
        a[k] = x;
        kopcuj(a, k ,j);
    }
}

void buduj_kopiec(lint a[], lint rozmiar){ //element algorytmu sortowania przez kopcowanie
    for (lint i = rozmiar / 2; i >= 0; i--) {
        kopcuj(a, i, rozmiar);
    }
}

void HeapSort(lint a[], lint rozmiar){ //algorytm sortowania przez kopcowanie
    buduj_kopiec(a, rozmiar);
    for (lint i = rozmiar - 1, x; i > 0; i--){
        x = a[0];
        a[0] = a[i];
        a[i] = x;
        kopcuj(a,0, i);
    }
}

lint *randomArr(lint len){ //funkcja przyswajająca tablicy rozmiar dynamiczny i losowe wartości
    lint *arr = malloc(len * sizeof(lint));
    for (uint i = 0; i < len; i++){
        arr[i] = (rand() % (rand() + 1));
    }
    return arr;
}

lint *increasingArr(lint len){ //funkcja sortująca tablicę o losowych wartościach
    lint *arr = randomArr(len);
    QuickSort(arr, 0, len - 1);
    return arr; //wynikiem jest ciąg rosnący
}

void reverseArr(lint arr[], lint len){ //funkcja odwracająca wartości tablicy
    uint start = 0, end = len - 1;
    lint temp;

    while (start < end)
    {
        temp = arr[start];
        arr[start] = arr[end];
        arr[end] = temp;
        start++;
        end--;
    }
}
lint *decreasingArr(lint len){ //wynikiem tej funkcji jest ciąg malejący
    lint *arr = increasingArr(len);
    reverseArr(arr, len);
    return arr;
}

void arrCpy(lint *dest, lint *source, lint len){
    //funkcja kopiująca wartości z tablicy dynamicznej do tablic statycznych
    for (int i = 0; i < len; i++){
        dest[i] = source[i];
    }
}

void sortPerformance(lint arr[], lint len, float results[]){
    lint quick_arr[len], heap_arr[len], insert_arr[len], merge_arr[len];
    //oddzielne statyczne tablice dla każdego algorytmu
    arrCpy(quick_arr, arr, len);
    arrCpy(heap_arr, arr, len);
    arrCpy(insert_arr, arr, len);
    arrCpy(merge_arr, arr, len);
    //wypełnianie tablic wartościami z podstawowej tablicy

    lint quick_start = clock(); //mierzenie czasu procesora przed wykonaniem algorytmu
    QuickSort(quick_arr, 0, len - 1);
    float duration_q = (float)(clock() - quick_start)/(float)(CLOCKS_PER_SEC);
    //łączny czas procesora zużyty przez program i wyrażony w sekundach, wartość rzeczywista
    results[QUICK] = duration_q; //zapisywanie tej wartości do tablicy wyników

    lint heap_start = clock();
    HeapSort(heap_arr, len);
    float duration_h = (float)(clock() - heap_start)/(float)(CLOCKS_PER_SEC);
    results[HEAP] = duration_h;

    lint insert_start = clock();
    InsertSort(insert_arr, len);
    float duration_i = (float)(clock() - insert_start)/(float)(CLOCKS_PER_SEC);
    results[INSERT] = duration_i;

    lint merge_start = clock();
    MergeSort(merge_arr, 0, len - 1);
    float duration_m = (float)(clock() - merge_start)/(float)(CLOCKS_PER_SEC);
    results[MERGE] = duration_m;

}

void wynikTestu(float results[]){

    int zwyciezca = results[QUICK];
    for(lint i = 0; i < MAX_SORTS; i++){ //wyznaczanie algorytmu o najmniejszym czasie wykonania
        zwyciezca = min(zwyciezca, results[i]);
    }

    printf("Wyniki naszego testu: \n"); //wypisywanie wszystkich wyników
    printf("- QuickSort: %f\n", results[QUICK]);
    printf("- HeapSort: %f\n", results[HEAP]);
    printf("- InsertionSort: %f\n", results[INSERT]);
    printf("- MergeSort: %f\n\n", results[MERGE]);

    printf("Tym razem "); //wypisywanie nazwy "zwycięskiego" algorytmu
    switch(zwyciezca)
    {
        case QUICK:
            printf("zwyciezyl QuickSort.\n");
            return;
        case HEAP:
            printf("zwyciezyl HeapSort.\n");
            return;
        case INSERT:
            printf("zwyciezyl InsertSort.\n");
            return;
        case MERGE:
            printf("zwyciezyl MergeSort.\n");
            return;
        default:
            printf("cos poszlo nie tak.\n");
            return;
    }
}
