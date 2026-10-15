#include <stdio.h>
#include <stdlib.h>

typedef struct element{
 int info;
 struct element *next;
} element, *list;

list head;

void ini(list *h)
{
    *h=NULL;
}

int empty(list h)
{
    return (h==NULL);
}

int pop(list *h)
{
    list u;
    int a;
    u=*h;
    (*h)=(*h)->next;
    a=u->info;
    free(u);
    return a;
}

void push(list *h, int a)
{
    list u;
    u=malloc(sizeof(element));
    u->info=a;
    u->next=*h;
    *h=u;
}

void drukuj_stos(list h)
{
    printf("Stos: ");
    while (h!=NULL)
    {
        printf("%d ",h->info);
        h=h->next;   //(*h).next;
    }
    printf("\n");
}

int main()
{
    int i,a;
    ini(&head);
    for (i=0;i<10;i++)
    {
       push(&head,2*i);
    }
    drukuj_stos(head);
    a=pop(&head);
    printf("Zdjety element: %d\n",a);
    drukuj_stos(head);
    for (i=0;i<5;i++)
        a=pop(&head);
    drukuj_stos(head);
    for (i=0;i<4;i++)
        a=pop(&head);
    drukuj_stos(head);
    printf("Test pustosci %d.\n",empty(head));

    printf("Hello world!\n");
    return 0;
}
