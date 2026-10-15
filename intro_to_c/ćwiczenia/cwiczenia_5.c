#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// definiujemy alias
typedef int key_type;

// definiujemy struktury reprezentujace drzewo
typedef struct node {
    key_type key;
    struct node *left;
    struct node *right;
    struct node *up;
} node, *tree;

// tworzenie nowego wierzchołka
tree new_vertex(key_type a){
    tree u;
    u=malloc(sizeof(node));
    u->key=a;
    u->left=NULL;
    u->right=NULL;
    u->up=NULL;
    return u;
}

/* Zadanie 2 (29.03.2021) Napisz program, który zaimplementuje procedury na drzewach BST o kluczach caªkowitych:
(a) inicjalizuj¡c¡ drzewo BST;
(b) dodajac¡ w¦zeª o podanym kluczu;
(c) obliczaj¡c¡ wysoko±¢ drzewa BST;
(d) czyszcz¡c¡ caªe drzewo, tzn. usuwajac¡ wszystkie wierzchoªki drzewa.
Nast¦pnie stwórz drzewa o 10, 100, 1000, 10000 losowych kluczach caªkowitych
oraz oblicz i wypisz ich wysoko±ci.
*/

// (a) inicjalizacja drzewa
void init_BST(tree *r){
    *r=NULL;
}

// (b) funkcja, ktora dodaje wezel o podanym kluczu
void add_vertex_BST(tree *r, tree v){
    // prośba o pokazanie dla tree current
    tree *current = r;
    tree upper = NULL;

    while (*current != NULL){
        upper = *current;
        if ((*current)->key >= v->key){
            current = &(*current)->left;
        }else{
            current = &(*current)->right;
        }
    }
    *current = v;
    v->up = upper;
}

// (c) funkcja, ktora liczy wysokosc drzewa
int height_BST(tree r){
    int l, p;

    if (r==NULL){
        return 0;
    } else {
        l = height_BST(r->left); // na przykladzie z wykladu = 4
        p = height_BST(r->right); // na przykladzie z wykladu = 3

        if (l < p){
            l = p;
        }
        return l + 1;
    }
}

// (d) funkcja, ktora usuwa wszystkie wirzchołki drzewa
void del_BST(tree *r){

    if (*r != NULL){
        del_BST(&((*r)->left)); // krok rekurencyjny dla lewego drzewa
        del_BST(&((*r)->right)); // krok rekurencyjny dla prawego drzewa
        free(*r);
        *r = NULL;
    }
}

/* Zadanie 3 (29.03.2021)  Napisz funkcj¦, która obliczy dla drzewa BST o kluczach caªkowitych
(a) liczb¦ li±ci w drzewie;
(b) liczb¦ wierzchoªków o tym samym kluczu k;
(c) liczb¦ wierzchoªków które maj¡ dokªadnie jednego syna;
(d) liczb¦ wierzchoªków o kluczach parzystych.
*/

// (a) funckja, ktora zwraca liczbe lisci w drzewie
int leaves_num_BST(tree r){
    if (r == NULL){
        return 0;
    } else {
        if (r->left == NULL && r->right == NULL)
            return 1;
        else
            return leaves_num_BST(r->left) + leaves_num_BST(r->right);
    }
}


int main()
{
    tree bst;
    int s, k;

    srand(time(NULL)); // do doczytania samodzielnie
    init_BST(&bst);
    for (k = 0; k < 1000; ++k){
        add_vertex_BST(&bst, new_vertex(rand() % 1000));
    }

    printf("wysokosc mojego drzewa to: %d\n", height_BST(bst));
    printf("wysokosc mojego drzewa to: %d\n", leaves_num_BST(bst));
    printf("\n Usuwamy wszystkie wezly z drzewa\n");
    del_BST(&bst);
    printf("wysokosc mojego drzewa to: %d\n", height_BST(bst));
    printf("wysokosc mojego drzewa to: %d\n", leaves_num_BST(bst));

    return 0;
}
