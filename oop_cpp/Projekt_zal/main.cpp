#include<iostream>
#include<vector>
#include<algorithm>
#include"miasto.h"

//komunikaty errorów

using namespace std;


int main() {
    srand(time(nullptr)); // NOLINT(cert-msc51-cpp)

    //stworzenie co najmniej 6 sklepów
    auto r = new Sklep("Rossmann", 1, 1);
    auto h = new Sklep("Hebe", 2, 2);
    auto k  = new Sklep("Kontigo", 3, 1);
    auto s = new Sklep("Sephora", 1, 4);
    auto d = new Sklep("Douglas", 5, 2);
    auto n = new Sklep("Natura", 4, 3);

    //dodanie do każdego sklepu po conajmniej 3 towary
    r->dodaj_towar("Podklad", 30, 1);
    r->dodaj_towar("Swieca", 10, 1);
    r->dodaj_towar("Perfum", 50, 1);

    h->dodaj_towar("Swieca", 7, 1);
    h->dodaj_towar("Serum", 20, 1);
    h->dodaj_towar("Paleta", 40, 1);

    k->dodaj_towar("Odzywka", 40, 1);
    k->dodaj_towar("Serum", 50, 1);
    k->dodaj_towar("Paleta", 80, 1);

    s->dodaj_towar("Perfum", 200, 1);
    s->dodaj_towar("Podklad", 100, 1);
    s->dodaj_towar("Swieca", 50, 1);

    d->dodaj_towar("Perfum", 150, 1);
    d->dodaj_towar("Serum", 90, 1);
    d->dodaj_towar("Odzywka", 120, 1);

    n->dodaj_towar("Podklad", 15, 1);
    n->dodaj_towar("Paleta", 25, 1);
    n->dodaj_towar("Odzywka", 30, 1);


    //stworzenie 2 sieci
    auto a = new Siec("ALpha", 0.1);
    auto b = new Siec("Beta", 0.05);


    //każda przejmuje po 2 sklepy
    a->przejmij_sklep(r);
    a->przejmij_sklep(d);
    b->przejmij_sklep(h);
    b->przejmij_sklep(k);


    //jedna sieć przejmuje drugą
    //a->przejmij_siec(b);


    //stwórz każdego klienta
    auto e = new Maksymalista("Emilia", 80, "Hebe");
    auto f = new Minimalista("Franciszek", 50, "Rossmann");
    auto g = new Losowy("Gabriela", 150, "Sephora");
    auto j = new Oszczedny("Jan", 150, "Perfum");
    auto m = new Tradycjonalista("Maria", 40,"Podklad" , 3,2);

    //wypisz stan symulacji
    wypisz_stan();

    //każdy klient kupuje prezenty

    cout << '\n' << "SWIETA SIE ROZPOCZELY!!!" << '\n';
    for (auto i: lista_klientow){
        i->kup();
    }
    //wypisz
    wypisz_stan();
    cout << "<3" << '\n';
    return 0;
}
