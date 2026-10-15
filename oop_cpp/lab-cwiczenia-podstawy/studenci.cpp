#include<iostream>
#include<vector>
#include <stdlib.h>     /* srand, rand */
#include <time.h>       /* time */
#include <algorithm>
#include <string>

using namespace std;

const int czas_symulacji = 100;

enum Ruch {w, z};

// w przypadku tego zadania domyslne implementacje
// reguly trzech wystarcza
// dlatego dla zwiezlosci kodu ich nie definiuje;
// w egzaminie chcielibysmy, zeby Państwo jawnie sie
// do nich odniesli

class Student {
public:
    virtual Ruch graj() = 0;
    virtual void reakcja(Ruch r) = 0;
    virtual void debug() {};
    virtual ~Student() {};
    virtual void reset() {};
    virtual string nazwa() = 0;
};

class Student_o_dlugiej_pamieci: public Student {
protected:
    vector<Ruch> pamiec;
public:
    Student_o_dlugiej_pamieci() = default;
    void reakcja(Ruch r) override {pamiec.push_back(r);};
    void reset() override { pamiec = {}; }
};

class Student_o_krotkiej_pamieci : public Student {
protected:
    Ruch ost;
public:
    Student_o_krotkiej_pamieci(): ost(w) {};
    void reakcja(Ruch r) override {ost = r;};
    void reset() override { ost = w; }
};

class Student_licznik: public Student {
public:
    Student_licznik() = default;
};

class Student_bez_pamieci: public Student {
public:
    Student_bez_pamieci() = default;
    void reakcja(Ruch r) override {};
    void reset() override {};
};

// zawsze wspolpracuje
class Altruista: public Student_bez_pamieci {
public:
    Ruch graj() override {return w;};
    string nazwa() override { return "Altruista"; }
};

// zawsze zdradza
class Freerider: public Student_bez_pamieci {
    Ruch graj() override {return z;};
    string nazwa() override { return "Freerider"; }
};

// gra losowo, w zalozeniu wspolpraca i zdrada z pstwem 1/2
// moglibysmy np. zrobic niesymetrycznego trolla
// ustawiajac mu pole z pstwem zdrady
class Troll: public Student_bez_pamieci {
public:
    Ruch graj() override {
        int losowa = rand() % 2;
        if(losowa) return w;
        return z;
    };
    string nazwa() override { return "Troll"; }
};

// sprawdza, jak zachowywano sie wobec niego w przeszlosci
// zaczyna od wspolpracy
// jesli tyle samo razy go oszukiwano, jak i wspolpracowano z nim
// to wspolpracuje
// mozna byloby np ustawic czy optymista czy pesymista
// optymista wspolpracowalby, pesymista zdradzalby w przypadku remisu
class Zapobiegliwy: public Student_o_dlugiej_pamieci {
public:
    Ruch graj() override {
        int ileZdradzony = count(pamiec.begin(), pamiec.end(), z);
        int ileWspolpracowano = count(pamiec.begin(), pamiec.end(), w);
        if(ileZdradzony > ileWspolpracowano) return z;
        return w;
    };
    string nazwa() override { return "Zapobiegliwy"; }
};

// Ja Ci Pokaze == wet za wet, powtarza ostatni ruch przeciwnika
class WetZaWet: public Student_o_krotkiej_pamieci {
public:
    //uzupelnic strategie!
    Ruch graj() override {return ost == z ? z : w;};
    string nazwa() override { return "Wet za wet"; }
};

//raz zdradzony zdradza juz zawsze
class Msciwy: public Student_licznik {
private:
    bool czy_zdradzony;
public:
    Msciwy(): czy_zdradzony(false) {};
    // uzupelnic strategie!
    Ruch graj() override {return czy_zdradzony == true ? z : w;};
    void reakcja(Ruch r) override {if (czy_zdradzony==false && r==z) czy_zdradzony = true;};
    void debug() override {cout <<czy_zdradzony <<"\n";};
    void reset() override { czy_zdradzony = false; }
    string nazwa() override { return "Mściwy"; }
};

// wszystkie tury wspolpracuje, w ostatniej zdradza
class JakMogles: public Student_licznik {
private:
    int czas_do_zdrady;
public:
    JakMogles(): czas_do_zdrady(czas_symulacji) {};
    //uzupelnic strategie!
    Ruch graj() override {return czas_do_zdrady != 1 ? w : z;};
    void reakcja(Ruch r) override {--czas_do_zdrady;};
    void debug() override {cout <<czas_do_zdrady <<"\n";};
    void reset() override { czas_do_zdrady = czas_symulacji; }
    string nazwa() override { return "JakMogles"; }
};

class Gra {
private:
    pair<int, int> wyplaty[2][2];
public:
    pair<int, int> mecz(Student *a, Student *b);
    void ustaw(Ruch ra, Ruch rb, int wa, int wb) {
        wyplaty[int(ra)][int(rb)] = {wa, wb};
    }
    Gra() {
        ustaw(w, w, 4, 4);
        ustaw(z, z, 1, 1);
        ustaw(w, z, 0, 5);
        ustaw(z, w, 5, 0);
    }
    virtual ~Gra() {}
};

pair<int, int> Gra::mecz(Student *a, Student *b) {
    a->reset();
    b->reset();
    int wynik_a = 0, wynik_b = 0;
    for(int i=0; i<czas_symulacji; i++) {
        auto ruch_a = a->graj();
        auto ruch_b = b->graj();
        auto& wyp = wyplaty[(int)ruch_a][(int)ruch_b];
        wynik_a += wyp.first;
        wynik_b += wyp.second;
        a->reakcja(ruch_b);
        b->reakcja(ruch_a);
    }
    return {wynik_a, wynik_b};
};

class Turniej : public Gra {
private:
    vector<Student*> gracze;
public:
    Student *gracz(int i) { return gracze[i]; }
    Turniej(const vector<Student*>& v = {}) : gracze(v) {}
    vector<int> turniej();
    void dodaj(Student *s) { gracze.push_back(s); }
    ~Turniej() { for(auto s: gracze) delete s; }
};

vector<int> Turniej::turniej() {
    int N = gracze.size();
    vector<int> wyniki(N, 0);
    for(int i=0; i<N; i++)
        for(int j=0; j<i; j++) {
            auto wynik = mecz(gracze[i], gracze[j]);
            cout << gracze[i]->nazwa() << " vs " << gracze[j]->nazwa() << " : " << wynik.first << ":" << wynik.second << "\n";
            wyniki[i] += wynik.first;
            wyniki[j] += wynik.second;
        }
    return wyniki;
}

int main() {
    srand(time(NULL));
    Turniej t;
    t.dodaj(new Altruista);
    t.dodaj(new Msciwy);
    t.dodaj(new Zapobiegliwy);
    t.dodaj(new JakMogles);
    t.dodaj(new Freerider);
    t.dodaj(new Troll);
    t.dodaj(new WetZaWet);
    auto wynik = t.turniej();
    for(int i=0; i<wynik.size(); i++)
        cout << "gracz " << t.gracz(i)->nazwa() << " zdobyl " << wynik[i] << " punktow\n";
    return 0;
}

