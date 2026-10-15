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

// funkcja, ktora wyznacza rozmiar drzewa - czyli zlicza wierzcholki
int size_bst(tree r){
    if (r == NULL){
        return 0;
    } else {
        return size_bst(r->right) + size_bst(r->left) + 1;
    }
}

// Zadanie 1 (12.04.2021) - Napisz funkcje, która sprawdzi, czy dane drzewo binarne jest k-zbalansowane.
int k_balanced_bst(tree r, int k){
    if (r == NULL){
        return 1;
    } else {
        return abs(size_bst(r->left) - size_bst(r->right)) <= k &&
        k_balanced_bst(r->left, k) &&
        k_balanced_bst(r->right, k);
    }
}

// Zadanie 2 (12.04.2021) -  Napisz funkcje, która sprawdzi, czy dane drzewo binarne jest zbalansowane wzgl¦dem li±ci
int leaf_balanced_bst(tree r){
    if (r == NULL){
        return 1;
    } else {
        return abs(leaves_num_BST(r->left) - leaves_num_BST(r->right)) <= 1 &&
        leaf_balanced_bst(r->left) &&
        leaf_balanced_bst(r->right);
    }
}

// Zadanie 3 (12.04.2021) - Napisz funkcje, która sprawdzi, czy dane drzewo BST jest prawe.
int right_balanced(tree r) {
    if (r == NULL) {
        return 1;
    } else {
        return (size_bst(r -> right) >= size_bst(r -> left)) &&
        right_balanced(r -> left) &&
        right_balanced(r -> right);
    }
}

// Zadanie 5 (12.04.2021) - Drzewo binarne jest cienkie, je±li ka»dy wierzchoªek w tym drzewie ma co najwy»ej jedno dziecko.
// (a) Napisz funkcj¦, która sprawdza, czy dane drzewo binarne jest cienkie.
int thin_bst(tree r){
    if (r == NULL){
        return 1;
    } else {
        return (r->left == NULL || r->right == NULL) &&
        thin_bst(r->left) &&
        thin_bst(r->right);
    }
}

// (b) Napisz funkcje, która dla danego drzewa binarnego zwraca wysoko±¢ jego maksymalnego poddrzewa cienkiego
int height_max_thin_bst(tree r){
    if (thin_bst(r)){
        return height_BST(r);
    } else {
        int height_bst_left = height_max_thin_bst(r->left);
        int height_bst_right = height_max_thin_bst(r->right);

        if (height_bst_left >= height_bst_right)
            return height_bst_left;
        else
            return height_bst_right;
    }
}

// (c) Napisz funkcj¦, która dla danego drzewa binarnego zwraca wska¹nik do korzenia maksymalnego poddrzewa cienkiego tego drzewa.
// procedura pomocnicza
void pointer_max_thin_bst_aux(tree r, tree *p, int *h){
    if (thin_bst(r)){
        *p = r;
        *h = height_BST(r);
    } else {
        int h_left, h_right;
        tree p_left, p_right;
        pointer_max_thin_bst_aux(r->left, &p_left, &h_left);
        pointer_max_thin_bst_aux(r->right, &p_right, &h_right);
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
tree pointer_max_thin_bst(tree r){
    tree pointer;
    int height;
    pointer_max_thin_bst_aux(r, &pointer, &height);
    return pointer;
}

// (d) Napisz funkcj¦, która dla danego drzewa binarnego zwraca licz¦ wierzchoªków, które s¡ korzeniami poddrzew cienkich tego drzewa o wysoko±ci co najmniej k.
int num_nodes_thin_bst(tree r, int k){
    int num_nodes;
    if (r == NULL){
        num_nodes = 0;
    } else {
        int num_nodes_left = num_nodes_thin_bst(r->left, k);
        int num_nodes_right = num_nodes_thin_bst(r->right, k);
        num_nodes = num_nodes_left + num_nodes_right;
        if (thin_bst(r) && height_BST(r) >= k)
            num_nodes++; //num_nodes = num_nodes + 1;
    }
    return num_nodes;
}




int main()
{
    printf("Hello world!\n");
    return 0;
}
