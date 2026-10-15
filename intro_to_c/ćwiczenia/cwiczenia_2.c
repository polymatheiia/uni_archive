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
    while(h!=NULL){
        printf("%d ", h->info);
        h=h->next;
    }
}

// Zadanie 1: zaimplementować kolejkę liczb całkowitych uzywajac listy jednokierunkowej
typedef list queue;

// funkcja, ktora sprawdza, czy kolejka jest pusta
int empty(queue q){
    return (q==NULL);
}

// usuwamy wartosc z poczatku kolejki oraz zwracamy te wartosc; jesli kolejka jest pusta to zwracamy 0
info_type pop_front(queue *q){
    info_type a = 0;

    if (!empty(*q)){
        list u;
        u=*q;
        *q=(*q)->next;
        a=u->info;
        free(u);
    }
    return a;
}

// wstawiamy wartosc do kolejki (na koniec). Obserwacje:
// 1. chce wiedziec jaka wartosc dodam na koniec kolejki (info_type a)
// 2. musimy przejsc po calej liscie i dodac na koncu element

// potrzebujemy funkcji, która daje nowy element
list new_element(info_type a){
    list u;
    u=malloc(sizeof(element));
    u->info=a;
    u->next=NULL;
    return u;
}

void push_back(queue *q, info_type a){
    list u;
    if (*q==NULL){
        // wykorzystamy funckje new_element
        *q=new_element(a);
    } else {
        u=*q;
        while(u->next != NULL){
            u=u->next;
        }
        // wykorzystamy funckje new_element
        u->next=new_element(a);
    }
}

// Zadanie 4: napisz funkcje, ktora odwraca liste jednokierunkowa
void reverse_list(list *h){
    list u;
    list rev_list = NULL;


    while ((*h)->next != NULL){
        u=(*h)->next;
        (*h)->next=rev_list;
        rev_list=*h;
        *h=u;
    }
    (*h)->next=rev_list;
}



int main()
{
    // inicjalizujemy kolejke
    queue q;
    ini(&q);

    // wstawmy elementy na kolejke i wydrukujemy je
    int k;
    for (k=1; k<=10; k++){
        push_back(&q, k);
        print_list(q);
        printf("\n");
    }

    // usunmy trzy elementy
    int i;
    info_type a;
    for (i=0; i<3; i++){
        a = pop_front(&q);
        printf("usuwamy: %d\n", a);
        print_list(q);
        printf("\n");
        printf("chce dodac element, ktory zdjalem na koniec kolejki");
        printf("\n");
        push_back(&q, a);
        print_list(q);
        printf("\n");
    }


    return 0;
}
