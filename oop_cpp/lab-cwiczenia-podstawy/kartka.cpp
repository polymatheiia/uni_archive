//zamiast klasy moglaby byc struktura
class elt {
public:
    int cecha;
    elt *nast;
};

class posiadacz {
    int pole;
    elt *lista;
public:
    posiadacz() { pole = 0; lista = nullptr; }
    posiadacz(int cos) : pole(cos), lista(nullptr) {}
    void wstaw(int x) {
        lista = new elt{x, lista};
    }
    ~posiadacz() {
        while(lista) { elt *pom = lista->nast; delete lista; lista = pom; }
    }
};

class kartka {
    int y, x;
    int **t;
public:
    kartka(int _y, int _x) : y(_y), x(_x) {
        t = new int* [y];
        for(int i=0; i<y; i++) t[i] = new int[x];
    }
    ~kartka() {
        for(int i=0; i<y; i++) delete[] t[i];
        delete[] t;
    }
};

int main() {
    kartka k(20, 20);
    return 0;
}
