#include <iostream>
using namespace std;

// mamy zwierzeta
// kazde zwierze ma swoj wzrost i liczbe zebow
// kazde zwierze potrafi sie odezwac daj_glos()
// interesuje nas pies i kot
// przeciętny pies mierzy 80 cm, ma 42 zeby
// przeciętny kot mierzy 60 cm, ma 30 zebow

class Zwierze{
protected:
    int liczba_zebow;
    double wzrost;
    bool* zeby;
public:
    Zwierze(int _liczba_zebow, double _wzrost): liczba_zebow(_liczba_zebow), wzrost(_wzrost) { zeby= new bool[liczba_zebow];}
    // virtual pozwala nam na definiowanie destruktorow w klasach pochodnych
    // jesli zalozylibysmy, ze jakas klasa pochodna moze miec nietrywialne do usuniecia pole
    // na tym etapie zadania, zadna z podklas takiego pola nie ma
    virtual ~Zwierze() {delete[] zeby;};
    virtual void daj_glos(ostream& os) const= 0;
    friend ostream& operator<<(ostream& os, const Zwierze& b);
    bool& operator[] (int nr) { return zeby[nr]; } //zalozenie o sensownosci danych
};

class Pies: public Zwierze{
public:
    Pies(double _wzrost = 80.0): Zwierze(42, _wzrost) {};
    void daj_glos(ostream& os) const override {os << "Hau";};
};

class Kot:public Zwierze{
    double wasy;
public:
    Kot(double _wzrost=60.0, double _wasy=0.1): Zwierze{30,_wzrost}, wasy(_wasy) {};
    void daj_glos(ostream& os) const override {os<<"Miau";};
};

ostream& operator<<(ostream& os, const Zwierze& b) {
    b.daj_glos(os);
    return os;
}

int main()
{
    Zwierze* Kleks = new Pies(100);
    Zwierze* Rudy = new Kot(40);
    cout <<"Kleksie, odezwij sie! " <<*Kleks <<"\n";
    cout <<"Rudy, odezwij sie! " <<*Rudy <<"\n";
    delete Rudy;
    delete Kleks;
}

