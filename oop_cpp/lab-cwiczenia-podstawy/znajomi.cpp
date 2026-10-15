#include <iostream>

class Znajomi {

private:

    int n;

    bool **tab_zna;

public:

    Znajomi(int _n) : n(_n) {
        tab_zna = new bool* [n];
        for(int i=0; i<n; i++) {
            tab_zna[i] = new bool [n];
            for(int j=0; j<n; j++) tab_zna[i][j] = false;
        }
    }

    bool zna(int a, int b) const { return tab_zna[a-1][b-1]; }
    void poznaj(int a, int b) { tab_zna[a-1][b-1] = tab_zna[b-1][a-1] = true; }
    void wspolniZnajomi(int a, int b) const;
    void spotkanie(int a);
    int max() const {
        int rekord = 0;
        for(int i=1; i<=n; i++) {
            int ile = 0;
            for(int j=1; j<=n; j++) if(zna(i, j)) ile++;
            if(ile > rekord) rekord = ile;
        }
        return rekord;
    }

    ~Znajomi() {
        for(int i=0; i<n; i++) delete[] tab_zna[i];
        delete[] tab_zna;
    }

    Znajomi(const Znajomi& z) = delete;
    Znajomi& operator = (const Znajomi& z) = delete;
    Znajomi(Znajomi&& z) { tab_zna = z.tab_zna; n = z.n; z.tab_zna = nullptr; z.n = 0; }
    Znajomi& operator = (Znajomi&& z) { tab_zna = z.tab_zna; n = z.n; z.tab_zna = nullptr; z.n = 0; return *this; }
};


void Znajomi::wspolniZnajomi(int a, int b) const {
    for(int c=1; c<=n; c++)
        if(zna(a, c) && zna(b, c)) std::cout << c << "\n";
}

void Znajomi::spotkanie(int a) {
    for(int c=1; c<=n; c++) {
        if(zna(a, c)) {
            for(int d=1; d<=n; d++) {
                if(zna(a, d) && c != d) poznaj(c, d);
            }
        }
    }
}

int main() {
    Znajomi z(10);
    z.poznaj(2, 4);
    z.poznaj(2, 6);
    z.spotkanie(2);

    z.wspolniZnajomi(2, 4);

    Znajomi z1 = std::move(z);

    z1.wspolniZnajomi(2, 4);

    return 0;
}
