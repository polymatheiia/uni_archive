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

list new_element(info_type a){
    list u;
    u=malloc(sizeof(element));
    u->info=a;
    u->next=NULL;
    return u;
}

void push_back(list *q, info_type a){
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

int funkcja(list h){
    list t;
    t=h;
    int m;
    while (h!=NULL){
        m = h->info;
        if (check(m,t)==1) return m;
        h=h->next;
    }
    return 0;
}

int check(int m, list l){
    int licz2m = 0;
    int licz3m = 0;
    while (l!=NULL){
        if (l->info==2*m) licz2m=1;
        if (l->info==3*m) licz3m=1;
        if (licz2m==1 && licz3m==1){
            return 1;
        }
        l=l->next;
    }
    return 0;
}

int main(){
    list i;
    ini(&i);
    push_back(&i, 3);
    push_back(&i, 5);
    push_back(&i, 7);
    push_back(&i, 9);
    push_back(&i, 11);
    push_back(&i, 71);
    push_back(&i, 78);

    print_list(i);
    printf("\n%d\n", funkcja(i));
}
