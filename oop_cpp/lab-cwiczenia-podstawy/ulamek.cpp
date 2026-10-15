#include <iostream>
using namespace std;

// przeciazac operatory mozemy na dwa sposoby
// 1. dodac metode w klasie
// 2. dodac funkcje poza klasa
// w przypadku drugiego sposobu, jesli funkcja ma miec dostep do pol prywatnych
// nalezy te funkcje zaprzyjaznic z dana klasa

// niestety, nie dotyczy to <<... to zawsze zaprzyjazniamy
// tak -- to jest przyklad slabej decyzji projektowej w cpp

class Ulamek {
    int licznik;
    int mianownik;

    void skroc();

public:
    //konstruktory
    Ulamek(): licznik(0), mianownik(1) {};
    Ulamek(int _licznik, int _mianownik);

    //destruktor
    ~Ulamek() = default;

    //kopiowanie
    Ulamek(const Ulamek& u) = default;
    Ulamek& operator= (const Ulamek& u) = default;

    //void drukuj();
    friend ostream& operator<< (ostream& os, const Ulamek& u) {
        os <<u.licznik <<'/' <<u.mianownik;
        return os;
    }

    // Ulamek nie zawiera zadnej "problematycznej" struktury danych
    // dlatego mozna podawac argument nie jako const referencje
    Ulamek dodaj(const Ulamek& u);
    Ulamek& dodaj_przypisz(const Ulamek& u);

    //przeciazyc dodawanie
    //przeciazyc dodawanie i przypisanie
    //przeciazyc odejmowanie
    //przeciazyc odejmowanie i przypisanie
    //przeciazyc mnozenie
    //przeciazyc mnozenie i przypisanie
    //przeciazyc dzielenie /
    //przeciazyc dzielenie / i przypisanie
    //przeciazyc >
    //przeciazyc >=
    //przeciazyc ==
    //przeciazyc <=
    //przeciazyc <
    //przeciazyc !=

    // gettery
    int get_licznik() const;
    int get_mianownik() const;

    //settery
    void set_licznik(int _licznik);
    void set_mianownik(int _mianownik);
    void set_licznik_mianownik(int _licznik, int _mianownik);
};

Ulamek::Ulamek(int _licznik, int _mianownik) {
    licznik = _licznik;
    mianownik = _mianownik;
}

int Ulamek::get_licznik() const {
    return licznik;
}

int Ulamek::get_mianownik() const {
    return mianownik;
}


int main() {
    Ulamek u1(1,2);
    Ulamek w2(1,2);
    cout <<u1 <<'\n';
    cout <<u1+w2;
    return 0;

}
