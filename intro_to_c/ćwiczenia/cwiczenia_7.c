#include <stdio.h>
#include <stdlib.h>

// definiujemy alias
typedef int key_type;

// definiujemy struktury reprezentujace drzewo
typedef struct node {
    key_type key;
    struct node *left;
    struct node *right;
    struct node *up;
} node, *tree;

// funkcja, ktora wyznacza rozmiar drzewa - czyli zlicza wierzcholki
int size_bst(tree r){
    if (r == NULL){
        return 0;
    } else {
        return size_bst(r->right) + size_bst(r->left) + 1;
    }
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

// Zadanie 6 (12.04.2021)
// (a) Napisz funkcj¦, która sprawdza, czy dane drzewo binarne jest peªnym drzewem binarnym
int full_bst(tree r){
    if (r == NULL)
        return 1;
    else
        return full_bst(r->left) && full_bst(r->right) &&
        size_bst(r->right) == size_bst(r->left);
}

// (b)  Napisz funkcj¦, która zwraca wysoko±¢ maksymalnego peªnego poddrzewa binarnego
int height_max_full_bst(tree r){
    if (full_bst(r))
        return height_BST(r);
    else {
        int h_left = height_max_full_bst(r->left);
        int h_right = height_max_full_bst(r->right);
        if (h_left >= h_right)
            return h_left;
        else
            return h_right;
    }
}

// (c) Napisz funkcj¦, która zwraca wska¹nik do korzenia maksymalnego peªnego poddrzewa danego drzewa binarnego
// procedura pomocnicza
void pointer_max_full_bst_aux(tree r, tree *p, int *h){
    if (full_bst(r)){
        *p = r;
        *h = height_BST(r);
    } else {
        int h_left, h_right;
        tree p_left, p_right;
        pointer_max_full_bst_aux(r->left, &p_left, &h_left);
        pointer_max_full_bst_aux(r->right, &p_right, &h_right);
        if (h_left >= h_right){
            *p = p_left;
            *h = h_left;
        } else {
            *p = p_right;
            *h = h_right;
        }
    }
}

// funkcja glowna
tree pointer_max_full_bst(tree r){
    tree pointer;
    int height;
    pointer_max_full_bst_aux(r, &pointer, &height);
    return pointer;
}

// (d) Napisz funkcj¦, która dla danego drzewa binarnego zwraca licz¦ wierzchoªków, które s¡ korzeniami peªnych poddrzew binarnych tego drzewa o wysoko±ci k.
int num_nodes_full_bst(tree r, int k){
    int num_nodes;
    if (r == NULL)
        num_nodes = 0;
    else {
        int num_nodes_left = num_nodes_full_bst(r->left, k);
        int num_nodes_right = num_nodes_full_bst(r->right, k);
        num_nodes = num_nodes_left + num_nodes_right;
        if (full_bst(r) && height_BST(r) == k)
            num_nodes++; // i.e. num_nodes = num_nodes + 1;
    }
    return num_nodes;
}

// Zadanie 1 (19.04.2021) - Napisz funkcj¦, która sprawdza czy drzewo binarne (etykietowane liczbami caªkowitymi) jest drzewem BST, tzn. etykiety speªniaj¡ warunek drzewa binarnych poszukiwa«.
// potrzebujemy dwoch funkcji pomocniczych: max i min wartosc wdrzewach bst
int min_key_bst(tree r){
    if (r != NULL){
     while (r->left != NULL)
        r = r->left;
    return r->key;
    } else
        return 0;
}

int max_key_bst(tree r){
    if (r != NULL){
     while (r->right != NULL)
        r = r->right;
    return r->key;
    } else
        return 0;
}

int is_bst(tree r){

    if (r == NULL || (r->left == NULL && r->right == NULL))
        return 1;
    else {
        // przechodzimy rekurencyjnie na lewe i prawe poddrzewo
        // będziemy mieć instrukcje warunkowe (trzy) - sprawdzamy czy: jest bst, czy max/min jest w odpowiedniej relacji do klucza korzenia,
        int is_left_bst = (r->left == NULL);
        int is_right_bst = (r->right == NULL);

        if (is_bst(r->left) && max_key_bst(r->left) <= r->key && r->left != NULL)
            is_left_bst = 1;

        if (is_bst(r->right) && min_key_bst(r->right) >= r->key && r->right != NULL)
            is_right_bst = 1;

        return is_left_bst && is_right_bst;

    }
}


int main()
{
    printf("Hello world!\n");
    return 0;
}
