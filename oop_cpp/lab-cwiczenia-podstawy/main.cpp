#include <iostream>
#include <utility>
#include <vector>

using namespace std;



class Afiliacja {

};

class Pax: public Afiliacja {

};

class TechnoCentrum: public Afiliacja {

};

class Mercantilus: public Afiliacja {

};

class WidmowaHelisa: public Afiliacja {

};

class Wektor{
public:
    int x;
    int y;
    int z;
    Wektor() = delete;
    Wektor(int _x, int _y, int _z): x(_x), y(_y), z(_z) {}
    ~Wektor() = default;
    //kopiowania?
    //dodawania!
};

class Kosmos {
public:
    vector<Kosmos*> zawartosc;
    void operator += (Kosmos* k) {zawartosc.push_back(k);}
    // operator +=
};

class Planeta: public Kosmos {
public:
    string nazwa;
    Wektor pozycja;
    Afiliacja* kolonia;
    Planeta() = delete;
    Planeta(string _nazwa, Wektor _pozycja, Afiliacja* _kolonia): nazwa(std::move(_nazwa)), pozycja(_pozycja), kolonia(_kolonia) {}
    ~Planeta() = default;//?
};

class Kapitan;
class Misja: public Kosmos {
public:
    vector<Misja*> ekipa;
    Kapitan* wodz;
    void operator += (Misja* k) {ekipa.push_back(k);}
    void ruch(Wektor move) {

    };
    Misja(Kapitan* _wodz): wodz(_wodz){};
};

class Postac; //wstepna deklaracja
class Statek: public Misja {
public:
    string nazwa;
    Wektor pozycja;
    Postac* boss;
    Statek()=delete;
    Statek(string _nazwa, Wektor _pozycja): nazwa(std::move(_nazwa)), pozycja(_pozycja) {}
    ~Statek() = default;
    void dowodca(Postac* _boss) {boss = _boss;};
};

class StatekArchaniol: public Statek {
public:
    StatekArchaniol(string _nazwa, Wektor _pozycja): Statek(std::move(_nazwa),_pozycja){}
};

class StatekZwykly: public Statek {
public:
    StatekZwykly(string _nazwa, Wektor _pozycja): Statek(std::move(_nazwa),_pozycja){}
};

class Postac: public Misja {
public:
    string nazwa;
    Afiliacja* af;
    Postac()=delete;
    Postac(string _nazwa, Afiliacja* _af): nazwa(std::move(_nazwa)), af(_af) {}
};

class Kapitan: public Postac {
public:
    Kapitan()=delete;
    Kapitan(string _nazwa, Afiliacja* _af): Postac(_nazwa, _af) {}
};

class Dowodca: public Postac {
public:
    Dowodca()=delete;
    Dowodca(string _nazwa, Afiliacja* _af): Postac(_nazwa, _af) {}
};
int main() {
    Afiliacja* pax = new Pax;
    Afiliacja* tc = new TechnoCentrum;
    Afiliacja* mer = new Mercantilus;
    Afiliacja* wh = new WidmowaHelisa;

    Kosmos k;
    k += new Planeta ("Pacem", Wektor(10,20,30), pax);
    k += new Planeta ("Sol Draconi Septem", Wektor(100, 20, 3), nullptr);
    Statek* sp0 = new StatekArchaniol("Rafael", Wektor(0,0,0));
    Statek* sp1 = new StatekZwykly("Torus", Wektor(0,0,1));
    Statek* swh1 = new StatekZwykly("Hal-2", Wektor(13,14,15));
    Postac* deSoya = new Kapitan("de Soya", pax);
    Postac* kenzo = new Dowodca("Kenzo Isozaki", mer);
    Postac* demloa = new Dowodca("Dem Loa", wh);
    sp0->dowodca(deSoya);
    sp1->dowodca(kenzo);
    swh1->dowodca(demloa);
    k += sp0;
    k += sp1;
    k += swh1;
    // ...
    Misja m(deSoya);
    m += sp0;
    m += sp1;
    m += swh1;

    m.ruch(Wektor(3,4,5));
    //...
    cout << k << endl;
    cout << m << endl;
    std::cout << "Hello, World!" << std::endl;
    return 0;
}
