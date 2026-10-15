#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// definiujemy alias
typedef float key_type;

// definiujemy struktury reprezentujace drzewo
typedef struct node {
    key_type key;
    struct node *left;
    struct node *right;
    struct node *up;
} node, *tree;


// Zadananie 2 (19.04.2021) - Napisa¢ funkcj¦ w j¦zyku c, która dla danego drzewa BST o kluczach rzeczywistych zwraca wska¹nik do wierzchoªka poddrzewa, którego waga jest najbli»sza 0.
// funkcja pomocnicza, która zwraca wagę drzewa bst
// zakładamy, że dla r == NULL zwracamy 0
key_type weight_bst(tree r){
    if (r == NULL)
        return 0;
    else
        return r->key + weight_bst(r->left) + weight_bst(r->right);
}

// będziemy wykorzystywać fabs()
// procedura pomocniczna
void pointer_almost_zero_bst_aux(tree r, tree *p, float *w){
    *p = r;
    *w = weight_bst(r);
    if (r != NULL){
        float w_left, w_right;
        tree p_left, p_right;
        pointer_almost_zero_bst_aux(r->right, &p_right, &w_right);
        pointer_almost_zero_bst_aux(r->left, &p_left, &w_left);
        // co dalej? wykorzystam fabs(*w) - tzn. w sytuacji gdy fabs(w_left) (czy fabs(right)) jest mniejsze, to chcę przepiąć mój wskaźnik
        // dodatkowo w tej instrukcji warunkowej musimy uważać, żeby nie wskazac na NULL
        if (p_left != NULL && fabs(w_left) < fabs(*w)){
            *p = p_left;
            *w = w_left;
        }

        if (p_right != NULL && fabs(w_right) < fabs(*w)){
            *p = p_right;
            *w = w_right;
        }
    }
}

// funkcja glowna
tree pointer_almost_zero_bst(tree r){
    tree pointer;
    int weight;
    pointer_almost_zero_bst_aux(r, &pointer, &weight);
    return pointer;
}


// Zadanie 4 (19.04.2021) - Napisz funkcj¦, która dla danego drzewa BST o kluczach rzeczywistych i liczby rzeczywistej x zwraca wskaznik do wierzecholka o kluczu o najblizszej wartosci danej wartosci do x.
tree almost_x_bst(tree r, float x){
    if (r != NULL){
        tree l_almost_x = almost_x_bst(r->left, x);
        tree r_almost_x = almost_x_bst(r->right, x);
        if (fabs(l_almost_x->key - x) < fabs(r->key - x) && l_almost_x != NULL)
            r = l_almost_x;

        if (fabs(r_almost_x->key - x) < fabs(r->key - x) && r_almost_x != NULL)
            r = r_almost_x;
    }
    return r;
}



int main()
{
    printf("Hello world!\n");
    return 0;
}
