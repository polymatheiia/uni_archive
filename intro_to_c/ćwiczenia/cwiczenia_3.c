#include <stdio.h>
#include <stdlib.h>

// tworzymy sobie alias
typedef int info_type;

// definiujmey element
typedef struct element{
    info_type info;
    struct element *next;
} element, *list;

// inicjalizacja listy
void ini(list *h){
    *h=NULL;
}

// drukowanie listy
void print_list(list h){
    if (h==NULL){
        printf("Lista jest pusta");
    }
    while(h!=NULL){
        printf("%d ", h->info);
        h=h->next;
    }
}

// dodawania elementu do konca listy
// potrzebujemy funkcji, która daje nowy element
list new_element(info_type a){
    list u;
    u=malloc(sizeof(element));
    u->info=a;
    u->next=NULL;
    return u;
}

void push_back(list *h, info_type a){
    list u;
    if (*h==NULL){
        // wykorzystamy funckje new_element
        *h=new_element(a);
    } else {
        u=*h;
        while(u->next != NULL){
            u=u->next;
        }
        // wykorzystamy funckje new_element
        u->next=new_element(a);
    }
}

// zadanie 2 (08.03.2021): napisz funkcje, ktory liczy dlugosc listy jednokierunkowej
int size_list(list h){
    int a = 0;
    // tutaj chcemy iterowac po liscie i zliczac elementy
    while (h != NULL){
        a+=1;
        h=h->next;
    }
    return a;
}

// zadanie 3 (08.03.2021): napisz funkcje, ktora dodaje do kazdego elementu listy jednokiernkowej liczbe calkowita
void add_value(list h, info_type a){
    while (h != NULL){
        h->info+=a; // dodajemy element
        h=h->next;
    }
}

// zadanie 5 (08.03.2021): napisz funkcje, ktora dla listy jednokierunkowej zwraca liczbe elementow, ktore sa podzielne przez liczbe calkowita k
int count_div(list h, int k){
    int a = 0;
    // przejdziemy po wszystkich elementach oraz w kazdym kroku bedziemy sprawdzac, czy el. jest podzielny przez k
    while (h != NULL){
        if (h->info % k == 0){
            a+=1;
        }
        h=h->next;
    }
    return a;
}

// zadanie 6 (08.03.2021): napisz funkcje, ktora usuwa wszystkie elementy z listy jednokierunkowej
// potrzebujemy empty
int empty(list h){
    return (h==NULL);
}

// potrzebujemy pop_front
info_type pop_front(list *h){
    info_type a = 0; // jesli lista jest pusta, to zwracamy 0

    if (!empty(*h)){
        list u; // potrzbujemy zmiennej na ktorej przechowamy to co zdejmiemy z listy
        u=*h;
        *h=(*h)->next;
        a=u->info;
        free(u);
    }
    return a;
}

// funkcja, ktora usuwa wszystkie elementy
void remove_all_elements(list *h){
    while (*h != NULL){
        pop_front(h);
    }
}

// zadanie 1 (15.03.2021): napisz funkcje, ktora scali dwie listy liczb calkowitych w jedna liste liczb calkowitych
// chcemy, zeby ostatni element pierwszej listy h1 wskazywał na pierwszy element drugiej listy h2
// po tym jak zlaczymy listy, to chce zeby glowa drugej listy wskazywala na NULL
void merge(list *h1, list *h2){
    list h = *h1;

    if (*h2 != NULL){
        if (*h1 == NULL){
            *h1 = *h2;
        } else {
            while (h->next != NULL){
                h = h->next;
            }
            h->next = *h2;
        }
        *h2 = NULL;
    }
}

// zadanie 2 (15.03.2021): napisz funkcje, ktora odwraca liste jednokierunkowa rekurencyjnie
// void ...



int main()
{
    // inicjalizujemy liste h1
    list h1;
    ini(&h1);

    // inicjalizujemy liste h2
    list h2;
    ini(&h2);

    // wstawmy elementy na listy h1 oraz h2 i wydrukujemy je
    int k;
    for (k=2; k<=10; k++){
        push_back(&h1, k);
        push_back(&h2, 2*k);
        print_list(h1);
        printf("\n");
    }



    printf("\n");
    // ad zadanie 2: wyznaczamy liczbe elementow
    // printf("Liczba elementow na liscie to: %d\n"); // przetrzymuje ostatnią wartość
    printf("Liczba elementow na liscie to: %d\n", size_list(h1));
    // printf("Liczba elementow na liscie to: %d\n"); // przetrzymuje ostatnią wartość

    printf("\n");
    // ad zadanie 3: dodajmy do kazdego elementu 8
    add_value(h1, 8);
    print_list(h1);

    printf("\n");
    // ad zadanie 5: policzmy ile jest liczb podzielnych przez 3
    printf("Liczba elementu na liscie podzielnych przez 3 to: %d\n", count_div(h1, 3));
    printf("\n");
    printf("Liczba elementu na liscie podzielnych przez 20 to: %d\n", count_div(h1, 20));

    printf("\n");
    // ad zadanie 6: usunmy wszystkie elementy
    // remove_all_elements(&h1);
    // print_list(h1);

    // ad zadanie 1 (15.03.2021): do listy h1 doczepimy liste h2
    printf("\n");
    printf("\n");
    printf("Wdyrukujemy sobie h1, h2\n");
    print_list(h1);
    printf("\n");
    print_list(h2);
    printf("\n");
    printf("\n");
    // polaczmy te listy
    merge(&h1, &h2);
    printf("Wdyrukujemy sobie h1, h2 po procedurze merge\n");
    print_list(h1);
    printf("\n");
    print_list(h2);



    return 0;
}
