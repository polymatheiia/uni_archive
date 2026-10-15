#include<stdio.h>
#include<stdlib.h>

void wskazniki()
{
    int *x;
    int a;
    a=5;
    x=&a;
    printf("%d\n", a);
    printf("%d\n", x);
    printf("%d\n", *x);
    printf("%d\n", &a); // tutaj będzie to samo co x
    printf("%d\n", &x);
}

//// stosy

// moze sobie stworzyc alias, ktora będzie wykorzystywany dalej w programie
typedef int info_type;

// definiujemy sobie zdefiniować element
typedef struct element{
    info_type info;
    struct element *next;
} element, *list;

// definiujemy głowę
list head;

// inicjalizacja stosu
void ini(list *h){
    *h=NULL;
}

// dodawanie elementu do stosu
// potrzebuje 'stosu', czyli w zasadzie głowy (to na co wskazuje nam głowa); potrzebujemy jeszcze zmiennej typu info_type
void push(list *h, info_type a){
    list u;
    u=malloc(sizeof(element));
    u->info=a; // czyli (*u).info=a;
    u->next=*h;
    *h=u;
}

// usuwanie elementu zes stosu
// potrzebuje
info_type pop(list *h){
    list u;
    info_type a;
    u=*h;
    *h=(*h)->next;
    a=u->info;
    free(u);
    return a;
}

// drukowanie stosu
void drukuj_stos(list h){
    while(h!=NULL){
        printf("%d ", h->info);
        h=h->next;
    }
}

// funkcja, która testuje, czy stos jest pusty
int empty(list h){
    return (h==NULL);
}


int main()
{
    // wskazniki();

    // definiujemy stos
    ini(&head);

    // dodajemy elementy
    push(&head, 5);
    push(&head, 10);
    push(&head, 15);
    push(&head, 20);
    drukuj_stos(head);

    // teraz usuwamy element oraz go drukujemy
    info_type a;
    a=pop(&head);
    printf("\nzdejmujemy element: %d", a);
    printf("\n");
    drukuj_stos(head);
    printf("\n");

    // sprawdzmy, czy jest pusty
    info_type test;
    test=empty(head);
    printf("%d", test);

}
