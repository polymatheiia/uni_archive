#include <iostream>
#include <utility>
#include <vector>

using namespace std;

enum Poziom {poczatkujacy, sredniozaawansowany, zaawansowany};

class Zajecia;
class Personel;
class Grupa;
class Szkola {
protected:
    vector<Zajecia*> zajecia; //Pracownik musi miec dostep, uczen nie
    vector<Personel*> kadra;
public:
    virtual ~Szkola() {
        for (auto i: zajecia) delete i;
        for (auto i: kadra) delete i;
    } //destruktor
    void wypisz();
};

class Grupa;
class Zajecia: public Szkola {
public: //lista zajec jest protected, klient sie nie dostanie
    string instrument;
    Poziom poziom;
    pair<int, int> limit_miejsc; //first - min, second - max
    int lba_godzin;
    vector<Grupa*> grupy;
    Zajecia() = delete;
    Zajecia(string _instrument, Poziom _poziom, pair<int, int> limit, int _lba_godzin):
    instrument(_instrument), poziom(_poziom), limit_miejsc(limit), lba_godzin(_lba_godzin) {zajecia.push_back(this);} //konstruktor
    ~Zajecia() {
        for (auto i: grupy) delete i;
        for(auto it = zajecia.begin(); it != zajecia.end(); ++it){
            if (this == (*it)) zajecia.erase(it);

        }
    } //destruktor
    Zajecia(const Zajecia& s) = delete;//zakazane kopiowania
    Zajecia& operator = (const Zajecia& s) = delete; //i przypisania
    void dodaj (Grupa* grupa) {grupy.push_back(grupa);}
};

class Osoba;
class Grupa: public Szkola {
protected:
    vector<Osoba*> zapisani;
public: //uczen ma prawo wiedziec, gdzie i kiedy ma przyjsc
    string kod;
    pair<string, int> termin;//pierwszy el - dzien, drugi - godzina
    int sala;
    string prowadzacy;
    int cena;
    Zajecia* program;

    Grupa() = delete;
    Grupa(Zajecia* _program, string _kod, pair<string, int> _termin, int _sala, string _prowadzacy, int _cena):
    program(_program), kod(_kod), termin(_termin), sala(_sala), prowadzacy(_prowadzacy), cena(_cena) {
        for (auto i: zajecia){
            if (i == program) program->dodaj(this);
        }
    }
    ~Grupa() {
        for(auto it = program->grupy.begin(); it != program->grupy.end(); ++it){
            if (this == (*it)) program->grupy.erase(it);
        }
        delete program;
    }
    Grupa(const Grupa& s) = delete;//zakazane kopiowania
    Grupa& operator = (const Grupa& s) = delete; //i przypisania

    int getilosc() {return zapisani.size();}
    void zapisz(Osoba* kandydat){zapisani.push_back(kandydat);}
    void wypiszuczestnikow(){
        for (auto i: zapisani) {
            // wypisz każdego
        }
    }
};




class Osoba {
protected:
    string imie;
    string nazwisko;
    string email;
    string instrument;
    Poziom poziom;
public:
    Osoba() = delete;
    Osoba(string _imie, string _nazwisko, string _email, string _instrument, Poziom _poziom):
    imie(std::move(std::move(_imie))), nazwisko(std::move(std::move(_nazwisko))), email(std::move(_email)), instrument(std::move(_instrument)), poziom(_poziom) {}; //konstruktor
    ~Osoba() = default; //destruktor
    Osoba(const Osoba& s) = delete;//zakazane kopiowania
    Osoba& operator = (const Osoba& s) = delete; //i przypisania

    vector<string> getInfo(){
        vector<string> ankieta;
        ankieta.push_back(imie);
        ankieta.push_back(nazwisko);
        ankieta.push_back(email);
        ankieta.push_back(instrument);
        return ankieta;
    }
    Poziom getPoziom() { return poziom;};
    //spotkanie?
    virtual string wybierz(vector<Grupa*> _propozycja) = 0; //osoba wybiera grupe z zaproponowanych
};

class Pracujacy_i_studenci: public Osoba {
public:
    string wybierz(vector<Grupa*> _propozycja) override {
        vector<Grupa*> propozycja = _propozycja;
        string wybor = " ";
        int godzina = 0;
        for(auto i: propozycja){
            int tmp = i->termin.second;
            if (tmp > godzina) {
                godzina = tmp;
                wybor = i->kod;
            }
        }
        return wybor;
    }
};

class Zapracowani: public Osoba {
public:
    string wybierz(vector<Grupa*> _propozycja) override {
        vector<Grupa*> propozycja = _propozycja;
        string wybor = " ";
        for(auto i: propozycja){
            string tmp = i->termin.first;
            if (tmp == "sobota" || tmp == "niedziela") {
                wybor = i->kod;
            }
        }
        return wybor;
    }
};

class Zamozni: public Osoba {
public:
    string wybierz(vector<Grupa*> _propozycja) override {
        vector<Grupa*> propozycja = _propozycja;
        string wybor = " ";
        int cena = 0;
        for(auto i: propozycja){
            int tmp = i->cena;
            if (tmp > cena) {
                cena = tmp;
                wybor = i->kod;
            }
        }
        return wybor;
    }
};

class Wielbiciele_talentu: public Osoba {
public:
    string fav_nauczyciel;
    //oddzielny konstruktor
    Wielbiciele_talentu(string _imie, string _nazwisko, string _email, string _instrument, Poziom _poziom, string _fav):
    Osoba(std::move(_imie), std::move(_nazwisko), std::move(_email), std::move(_instrument), _poziom), fav_nauczyciel(std::move(_fav)) {};
    string wybierz(vector<Grupa*> _propozycja) override {
        vector<Grupa*> propozycja = _propozycja;
        string wybor = " ";
        for(auto i: propozycja){
            string tmp = i->prowadzacy;
            if (tmp == fav_nauczyciel) {
                wybor = i->kod;
            }
        }
        return wybor;
    }
};

class Personel: public Szkola {
public:
    string imie;
    Personel() = delete;
    Personel(string _imie): imie(_imie) {kadra.push_back(this);}
    ~Personel(){
        for(auto it = kadra.begin(); it != kadra.end(); ++it){
            if (this == (*it)) kadra.erase(it);
        }
    }
    Personel(const Personel& s) = delete;//zakazane kopiowania
    Personel& operator = (const Personel& s) = delete; //i przypisania
};


class Muzyk: public Personel {
public:
    string instrument; //nie ma sensu tego ukrywac
    Muzyk() = delete;
    Muzyk(string _imie, string _instrument): Personel(_imie), instrument(_instrument) {};
    ~Muzyk() = default;
    //kopiowania!
    vector<Grupa*> zaproponuj(Osoba* kandydat){ //zwraca propozycje, co z parametrami
        vector<Grupa*> propozycja;
        Poziom stopien = kandydat->getPoziom();
        for (auto i: zajecia){
            if(i->poziom == stopien) {
                for (auto j: i->grupy) {propozycja.push_back(j);}
            }
        }
        return propozycja;
    }
};
class Administracja: public Personel {
public:
    vector<Osoba*> kandydaci;
    vector<Muzyk*> pracownicy;
    Administracja()=delete;
    Administracja(string _imie): Personel(_imie) {}; //konstruktor
    ~Administracja() {
        for(auto i: kandydaci) delete i;
        for(auto i: pracownicy) delete i;
    } //destruktor

    string wyznacz (string _instrument) {
        for(auto i: pracownicy){ if (i->instrument == _instrument) return i->imie;}
    }
    string rekrutuj (Osoba* kandydat) {
        vector<string> dane = kandydat->getInfo();
        string egzaminator = wyznacz(dane.at(3)); //zwraca imie muzyka
        vector<Grupa*> modified_propozycja;
        for(auto i: pracownicy){
            if(i->imie == egzaminator) modified_propozycja = i->zaproponuj(kandydat);
        }
        //czyscimy, jesli nie ma miejsc
        for(auto it = modified_propozycja.begin(); it != modified_propozycja.end(); ++it){
            if ((*it)->program->limit_miejsc.second <= (*it)->getilosc()) modified_propozycja.erase(it);
        }
        string grupa = kandydat->wybierz(modified_propozycja); //kod grupy

        if (grupa!= " ") {
            for (auto i: modified_propozycja) {
                if (grupa == i->kod) i->zapisz(kandydat);
            }
        } //jesli cos wybral, to zapisz do grupy
    }
};

void Szkola::wypisz() {
    for (auto i: zajecia){
        cout << i->instrument << ", " << i->poziom << ", grupa ";
        cout << i->limit_miejsc.first<< "-"<< i->limit_miejsc.second << " osob "<< i->lba_godzin<< " godzin"<< '\n';
        for (auto j: i->grupy) {
            cout << j->kod << ", "<< j->termin.first << j->termin.second<< ",  sala " << j->sala;
            cout << ", "<< j->prowadzacy<< ", "<< j->cena<< " zl"<< '\n';
            j->wypiszuczestnikow();
        }
    }

}


int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}
