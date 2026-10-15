#include <stdio.h>
#include <stdlib.h>

// moze sobie stworzyc alias, ktora będzie wykorzystywany dalej w programie
typedef int info_type;

// definiujemy sobie zdefiniować element
typedef struct element{
    info_type info;
    struct element *next;
} element, *list;

// usuwanie elementu ze stosu
info_type pop(list *h){
    list u;
    info_type a;
    u=*h;
    *h=(*h)->next;
    a=u->info;
    free(u);
    return a;
}

// dodawanie elementu do stosu
void push(list *h, info_type a){
    list u;
    u=malloc(sizeof(element));
    u->info=a; // czyli (*u).info=a;
    u->next=*h;
    *h=u;
}

// funkcja, która testuje, czy stos jest pusty
int empty(list h){
    return (h==NULL);
}

// zadanie 4 (15.03.2021) - Zaimplementuj kolejk¦ u»ywaj¡c dwóch stosów, tzn. u»ywaj¡c operacji stosu (push, pop, empty) dla dwóch stosów zasymuluj operacje kolejki:
// wstaw_na_koniec
// usun_z_poczatku
// test_pustosci
typedef list queue;

info_type usun_z_poczatku(queue *q){
    return pop(q);
}

int test_pustosci(queue q){
    return empty(q);
}

void wstaw_na_koniec(queue *q, info_type a){
    // 1. stworzmy sobie pomocniczy stos - tmp_stack
    // 2. zdejmujmy elementy z kolejki i wsadzajmy je na tmp_stack - potrafimy to zrobic, bo mamy: usun_z_poczatku, push
    // 3. jak juz zdejmiemy wszystkie elementy, to dodajmy ten element z wartoscia a - potrafie to zrobic, bo mam: push
    // 4. analogicznie, w petli, bedziemy zdejmowac elemnty ze stosu i wsadzac do kolejki: pop, push
    list tmp_stack = NULL;
    while(!empty(*q)){
        push(&tmp_stack, pop(q));
    }
    push(q, a);
    while(!empty(tmp_stack)){
        push(q, pop(&tmp_stack));
    }
}

// zadanie 2 (15.03.2021) - Napisz funkcj¦, która odwraca list¦ jednokierunkow¡ rekurencyjnie
void reverse_list(list *h){
    if (*h !=NULL && (*h)->next != NULL){
        list rest_h = (*h)->next;
        reverse_list(&rest_h);
        (*h)->next->next = *h;
        (*h)->next = NULL;
        (*h) = rest_h;
    }
}

// zadanie 4 (22.03.2021) -  Napisz funkcj¦, która znajdzie pierwszy wspólny element na dwóch listach o niepustej wspólnej cz¦±ci:
// 1. wyznaczmy dlugosci list i znajdzmy dluzsza z nich
// 2. przejdziemy pod dluzszej liscie do momentu, w ktorym sciezka do konca jest tej samehj dlugosci
// 3. przejdziemy wspolnie przez h1, h2, w kazdym kroku sprawdzajmy, czy trafiamy na ten sam element, jesli tak, to koniec
int list_size(list h){
    int size = 0;

    while(h != NULL){
        size += 1;
        h = h->next;
    }
    return size;
}

list find_first_joint_el(list h1, list h2){
    int size_h1;
    int size_h2;
    size_h1 = list_size(h1); // zgodnie z przykladem mamy: 8
    size_h2 = list_size(h2); // mamy 6
    int size_diff;

    // na h1 będziemy trzymać dłuższą listę
    list tmp_h;
    if (size_h2 > size_h1){
        tmp_h = h1;
        h1 = h2;
        h2 = tmp_h;
        size_diff = size_h2 - size_h1;
    } else {
        size_diff = size_h1 - size_h2;
    }

    // przechodzimy po liscie h1 o size_diff
    int k = 0;
    while (k < size_diff){
        h1 = h1->next;
        k += 1;
    }

    // teraz ostatnia faza, czyli przechodzimy po elementach az dostaniemy znajdziemy ten sam element
    while (h1 != h2){
        h1=h1->next;
        h2=h2->next;
    }
    return h1;
}

//// LISTY DWUKIERUNKOWE
// definiujmey element
typedef struct element_2{
    info_type info;
    struct element_2 *next;
    struct element_2 *prev;
} element_2, *list_2;

// inicjalizacja listy dwukierunkowej
void ini_list_2(list_2 *h){
    *h=NULL;
}

// inicjaliazcji listy dwukierunkowej z wartownikiem
void ini_list_2_wartownik(list_2 *h){
    (*h)=malloc(sizeof(element_2));
    (*h)->next=*h;
    (*h)->prev=*h;
}

// tworzenie nowego elemetu
list_2 new_element_2(info_type a){
    list_2 u;
    u=malloc(sizeof(element_2));
    u->info=a;
    u->next=NULL;
    u->prev=NULL;
    return u;
}

// dodawanie nowego elementu na początek listy_2
void add_list_2(list_2 *h, list_2 u){
    if ((*h)!=NULL) ((*h)->prev=u);
    u->next=*h;
    *h=u;
}

// dodawanie elemtnu do listy z wartownikiem
void add_list_2_wartownik(list_2 h, list_2 u){
    h->next=u->next;
    h->prev=u;
    (u->next)->prev=h;
    u->next=h;
}

// usuwanie elementu z listy_2
void del_el_from_list_2(list_2 *h, list_2 v){
    if (v->prev!=NULL) {
        v->prev->next=v->next;
    } else {
        (*h)=v->next; if ((*h)!=NULL) (*h)->prev=NULL;
    }
    if (v->next!=NULL) {
        v->next->prev=v->prev;
    }
}

// usuwanie elementu z listy z wartownikiem
void del_el_from_list_2_wartownik(list_2 v){
    v->prev->next=v->next;
    v->next->prev=v->prev;
}


int main()
{
    printf("Hello world!\n");
    return 0;
}
