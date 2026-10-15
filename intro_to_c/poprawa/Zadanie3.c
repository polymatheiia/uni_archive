//Zadanie 3
//Imiê: Danuta
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
    iniBST(&root);
    for (i = 0; i < n; i++)
        dodajBST(&root, nowy(m=rand() % 100));
    return root;
}

tree make_dense_tree()
//tworzenie losowego drzewa
{
    tree root;
    int n = 10;
    int a[]={14, 11, 8, 7, 10, 12, 16, 15, 18, 19};
    iniBST(&root);
    for (int i = 0; i < n; i++) dodajBST(&root, nowy(a[i]));
    return root;
}
//funkcje pomocnicze: funkcje size_bst i height_bst pojawiały się na ćwiczeniach
int min(tree r){
    if (r!=NULL){
        if (r->left!=NULL) min(r->left);
        else return r->key;
    }
}
int max(tree r){
    if (r!=NULL){
        if (r->right!=NULL) max(r->right);
        else return r->key;
    }
}
int size_bst(tree r){
    if (r == NULL){
        return 0;
    } else {
        return size_bst(r->right) + size_bst(r->left) + 1;
    }
}
int height_BST(tree r){
    int l, p;

    if (r==NULL){
        return 0;
    } else {
        l = height_BST(r->left);
        p = height_BST(r->right);

        if (l < p){
            l = p;
        }
        return l + 1;
    }
}

void dosc_geste(tree r){
    if ((max(r)-min(r)-height_BST(r)+1)<=size_bst(r)) printf ("To drzewo jest dosc geste!\n");
    else printf ("To drzewo nie jest dosc geste. \n");
}

int main()
{
  tree root, root_d;
  srand(time(NULL));
  //srand(1234); //do testowania na stalym drzewie

  root = make_tree();
  printf("Drzewo BST:\n");
  rysuj(root, 3);
    dosc_geste(root);

  root_d = make_dense_tree();
  printf("Drzewo dosc geste BST:\n");
  rysuj(root_d, 3);
  dosc_geste(root_d);

  return 0;
}
