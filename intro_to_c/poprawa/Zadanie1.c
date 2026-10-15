//Zadanie 1
//Imie: Danuta
//Nazwisko: Grabovska

#include<stdio.h>
#include<stdlib.h>
#include<time.h>

typedef struct element{
    int info;
    struct element *next;
} element, *list;

void ini(list *h)
// inicjalizacja listy 1-kierunkowej
{
    *h=NULL;
}

list nowy (int a)
//tworzenie elementu listy 1-kierunkowej
{
    list u;
    u=malloc(sizeof(struct element));
    u->next=NULL;
    u->info=a;
    return u;
}

void dodaj(list *h, list u)
//dodawanie elementu do listy 1-kierunkowej
{
    u->next=*h;
    *h=u;
}

void druk(list u)
//wypisanie_listy_1-kierunkowej_
{
    while (u!=NULL)
    {
        printf("%d ",u->info);
        u=(*u).next;
    }
    printf("\n");
}

void make_lists(list *h1, list *h2)
//generuje dwie listy losowe uporzadkowana scisle roznaca o wspolnej koncowej czesci
{
    list head1, head2;
    int d=40, d1, d2;
    srand(time(NULL));
    d1=(rand()%d)/3;
    d2=(rand()%d)/3;
    d=d+rand()%d;
    ini(&head1); ini(&head2);
    for(int i=d; i>d/2; i=i-3) dodaj (&head1,nowy(i-(rand()%3)));
    head2=head1;
    druk(head1);
    for(int i=d/2; i>d1; i=i-(3+(rand()%4))) dodaj (&head1,nowy(i-(rand()%3)));
    for(int i=d/2; i>d2; i=i-(3+(rand()%4))) dodaj (&head2,nowy(i-(rand()%3)));
    *h1=head1; *h2=head2;
}


void push_back(list *h, int a){
    list u;
    if (*h==NULL){
        // wykorzystamy funckje new_element
        *h=nowy(a);
    } else {
        u=*h;
        while(u->next != NULL){
            u=u->next;
        }
        // wykorzystamy funckje new_element
        u->next=nowy(a);
    }
}


int list_size(list h){
    int size = 0;

    while(h != NULL){
        size += 1;
        h = h->next;
    }
    return size;
}

//szukamy wartoœæ klucza, od którego zaczyna siê czêœæ wspólna
int find_first_joint_el(list h1, list h2){
    int size_h1;
    int size_h2;
    size_h1 = list_size(h1);
    size_h2 = list_size(h2);
    int size_diff;

    // na h1 bêdziemy trzymaæ d³u¿sz¹ listê
    list tmp_h;
    if (size_h2 > size_h1){
        tmp_h = h1;
        h1 = h2;
        h2 = tmp_h;
        size_diff = size_h2 - size_h1;
    } else {
        size_diff = size_h1 - size_h2;
    }


    int k = 0;
    while (k < size_diff){
        h1 = h1->next;
        k += 1;
    }

    while (h1 != h2){
        h1=h1->next;
        h2=h2->next;
    }
    return h1->info;
}

//³¹czymy obie listy, dopóki nie dotrzemy do czêœci wspólnej, a tam przenosimy j¹ z którejœ listy
void merge_till_common(list h1, list h2, list tmp){
    while (h1->info!=find_first_joint_el(h1, h2) || h2->info!=find_first_joint_el(h1, h2)){
        if (h1->info<h2->info){
            push_back(&tmp,h1->info);
            h1=h1->next;
        }
        else {
            push_back(&tmp, h2->info);
            h2=h2->info;
        }
    }
    while (h1!=NULL){
        push_back(&tmp,h1->info);
        h1=h1->next;
    }
}

int main()
{
    list head1, head2;
    make_lists(&head1,&head2);
    druk(head1); druk(head2);
    printf("Scalona lista:\n");
    list tmp;
    ini(&tmp);
    merge_till_common(head1,head2,tmp);
    druk(tmp);
    return 0;
}
