//Zadanie 2
//Imię: Danuta
//Nazwisko: Grabovska

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

typedef struct node {
  int key;
  struct node *left;
  struct node *right;
  struct node *up;
} node, *tree;

void iniBST(tree *r)
// inicjalizacja drzewa
{
  *r = NULL;
}

void spacje(int n)
{
  int i;
  for (i = 1; i <= n; ++i) printf(" ");
}

void rysuj(tree t, int n)
// rysowanie 'malego' drzewa BST
{
  if (t != NULL)
  {
    rysuj(t->right, n + 3);
    spacje(n);
    printf("%d\n", t->key);
    rysuj(t->left, n + 3);
  }
}

tree nowy(int a)
// tworzenie wierzcholka drzewa o zadanym kluczu
{
  tree u;
  u = malloc(sizeof(node));
  u->key = a;
  u->left = NULL;
  u->right = NULL;
  u->up = NULL;
  return (tree)u;
}

void dodajBST(tree *r, tree v)
// dodawanie wierzcholka wskazywanego przez v do drzewa BST o korzeniu *r
{
  if ((*r) == NULL) *r = v;
  else
  {
    if ((*r)->key < v->key)
    {
      if ((*r)->right != NULL) dodajBST(&((*r)->right), v);
      else { v->up = *r; (*r)->right = v; }
    }
    else
    {
      if ((*r)->left != NULL) dodajBST(&((*r)->left), v);
      else { v->up = *r; (*r)->left = v; }
    }
  }
}

tree make_tree()
//tworzenie losowego drzewa
{
    tree root;
    int n = 10 + rand() % 20,i,m;
    int a[100];
    for (i=0;i<n;i++)
        a[i]=0;
    iniBST(&root);
    for (i = 0; i < n; i++)
        {
            do
            {
                m = rand() % 100;
            } while (a[m] != 0);
            dodajBST(&root, nowy(m));
            a[m]=1;
        }
    return root;
}
pomocnicza(tree d,tree *t,int *n) //funkcja do wygenerowania poddrzewa
{

    if (d!=NULL)
    {
        pomocnicza(d->left,t,n);
        *n=*n-1;
        if(*n==0) return *t=d;
        else pomocnicza(d->right,t,n);
    }
}

//szukamy w drzewie y wierzchołka o kluczu z korzenia x
tree search(tree y, int x){
    if (y==NULL || x==NULL) return NULL;
    if (y->key>x) search(y->left, x);
    if (y->key<x) search(y->right, x);
    else {
        if (y->key==x) return y;
    }
}

void check_bst(tree y, tree x){
   int i=0;
   if(y!=NULL){
        do{
          if(y->key!=x->key){
              printf("To drzewo nie jest poddrzewem naszego drzewa!\n");
              x=1;
          }
          check_bst(y->left, (x->left)->key);
          check_bst(y->right, (x->right)->key);
       }while(y!=NULL && x!=NULL && i!=1);
       if(i==0)
           printf("To drzewo jest poddrzewem naszego drzewa!\n");
   } else ("To drzewo nie jest poddrzewem naszego drzewa!\n");
}

int main()
{
  tree root, root_d;
  srand(time(NULL));
  int n=rand()%10;// do poddrzewa
  //srand(1234); //do testowania na stalym drzewie

  root = make_tree();
  printf("Drzewo BST z roznymi kluczami w roznych wezlach:\n");
  rysuj(root, 3);
  //przypadek negatywny
  //tworzenie drzewa BST, ktore nie jest poddrzewem root
  printf("drugie drzewo przypadek 1:\n");
  root_d = make_tree();
  rysuj(root_d,3);
  //tu wywolanie zad 2
  check_bst(search(root, root_d), root_d);
  //tworzenie drzewa, ktore jest poddrzewem root
  printf("poddrzewo od elementu n=%d\n",n);
  pomocnicza(root,&root_d,&n);
  printf("drugie drzewo przypadek 2:\n");
  rysuj(root_d,3);
  //tu wywolanie zad 2
  check_bst(search(root, root_d), root_d);
  return 0;
}
