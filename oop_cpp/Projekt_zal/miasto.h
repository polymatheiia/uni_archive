#ifndef PROJEKT_ZAL_MIASTO_H
#define PROJEKT_ZAL_MIASTO_H

using namespace std;

class Siec;
class Sklep;
class Obiekt_handlowy;
class Klient;
//rzeczy globalne
void wypisz_stan();
extern vector<Obiekt_handlowy*> lista_oh;
extern vector<Siec*> lista_sieci;
extern vector<Sklep*> lista_sklepow;
extern vector<Klient*> lista_klientow;

class Loc {
public:
    int x;
    int y;
    Loc() = delete;
    Loc(int _x, int _y): x(_x),y(_y) {};
    [[nodiscard]] double dist(const Loc& b) const;
}; //klasa dla definiowania położenia sklepów i Tradycjonalisty

class Towar {
private:
    int cena;
    int ilosc;
public:
    string nazwa;
    Towar() = delete;
    explicit Towar(string _nazwa, int _cena = 1,int _ilosc = 1): nazwa(std::move(_nazwa)), cena(_cena), ilosc(_ilosc) {};
    ~Towar() = default;

    [[maybe_unused]] void setCena(int _cena);
    void setIlosc(int _ilosc);
    [[nodiscard]] int getCena() const;
    [[nodiscard]] int getIlosc() const;
};

class Obiekt_handlowy {
public:
    string nazwa; //nazwa jest polem publicznym dla kazdego obiektu z oczywistych powodow

    explicit Obiekt_handlowy(string _nazwa): nazwa(std::move(_nazwa)){}; //konstruktor
    virtual ~Obiekt_handlowy() = default; //destruktor
    virtual void sprzedaj(string _nazwa) = 0;
    [[nodiscard]] virtual pair<int, string> sprawdz(string _nazwa) const = 0; //zwraca cenę i towar/sklep
    virtual void wypisz() const = 0;
};
class Sklep: public Obiekt_handlowy {
protected:
    vector<Towar*> oferta; //lista towarów
public:
    Loc polozenie; //LOKALIZACJA
    Siec* wlasciciel = nullptr;
    //konstruktor
    Sklep() = delete;
    Sklep(string _nazwa, int _x, int _y);

    //destruktor
    ~Sklep() override;

    //zakazane kopiowania i przypisania
    Sklep(const Sklep& s) = delete;
    Sklep& operator = (const Sklep& s) = delete;

    //metody
    [[nodiscard]] vector<Towar*> getOferta() const;
    void dodaj_towar(string _nazwa, int _cena, int _ilosc);
    void setWlasciciel (Siec* net);
    [[nodiscard]] pair<int, string> sprawdz(string _nazwa) const override;
    void wypisz() const override;
    void sprzedaj(string _nazwa) override;
    void uniezaleznij();
};

class Siec: public Obiekt_handlowy {
protected:
    double marza; //wartość dziesietna np. 0.3 lub 1.6, zalezy od zachlannosci sieci
public:
    Siec() = delete;
    Siec(string _nazwa, double _marza); //konstruktor
    ~Siec() override; //destruktor
    Siec(const Siec& s) = delete; //zakazać kopiowań
    Siec& operator = (const Siec& s) = delete; //i przypisań

    vector<Sklep*> wlasnosc; //wektor wskaźników na sklepy

    //metody
    [[nodiscard]] pair<int, string> sprawdz(string _nazwa) const override;
    void sprzedaj(string _nazwa) override;
    void przejmij_sklep (Sklep* sklep);
    void przejmij_siec (Siec* siec);
    void wypisz() const override;
};
class Klient {
protected:
    int budzet;
    const string strategia;
    bool czy_ma_prezent = false;
public:
    string nazwa; //nazwa jest polem publicznym dla kazdego obiektu z oczywistych powodow

    Klient() = delete;
    Klient(string _nazwa, int _budzet); //konstruktor
    ~Klient();//destruktor
    Klient(const Klient& k) = delete;//zakazać kopiowań
    Klient& operator = (const Klient& k) = delete;//i przypisań

    //metody
    virtual void wypisz() const = 0;
    virtual void kup() = 0; //wybierz swój towar/sklep i zaplac
    [[nodiscard]] virtual pair<int, string> wybierz() const = 0; //zdecyduj jak i co wybierasz wg swojej strategii
    void zaplac(const string& sklep, const string& towar, int cena);
    [[nodiscard]] bool check_sklep(const string& sklep) const; // sprawdza czy istnieje niezrzeszony sklep o tej nazwie
    [[nodiscard]] bool check_sklep_ist(const string& sklep) const;
};
class Ulubiony_sklep: public Klient {
protected:
    string fav_sklep;
public:
    Ulubiony_sklep() = delete;
    Ulubiony_sklep(string _nazwa, int _budzet, string _fav_sklep);//konstruktor
    //destruktor jest w Kliencie
    void kup() override;
    [[nodiscard]] vector<Towar*> zdobytaLista() const; //musimy zdobyć listę towarów
    void wypisz() const override;
};
class Maksymalista: public Ulubiony_sklep {
public:
    const string strategia = "Maksymalista";
    Maksymalista(string _nazwa, int _budzet, string _fav_sklep); //konstruktor
    //destruktor jest w Kliencie
    [[nodiscard]] pair<int, string> wybierz() const override;
};
class Minimalista: public Ulubiony_sklep {
public:
    const string strategia = "Minimalista";
    Minimalista(string _nazwa, int _budzet, string _fav_sklep); //konstruktor
    //destruktor jest w Kliencie
    [[nodiscard]] pair<int, string> wybierz() const override;
};
class Losowy: public Ulubiony_sklep {
private:
    int szanse;
public:
    const string strategia = "Losowy";
    Losowy(string _nazwa, int _budzet, string _fav_sklep, int _szanse = 3); //konstruktor
    //destruktor jest w Kliencie
    [[nodiscard]] pair<int, string> wybierz() const override;
};
class Konkretny_produkt: public Klient {
protected:
    string fav_towar;
public:
    Konkretny_produkt(string _nazwa, int _budzet, string _fav_towar); //konstruktor
    //destruktor jest w Kliencie
    void kup() override;
    void wypisz() const override;
};
class Oszczedny: public Konkretny_produkt {
public:
    const string strategia = "Oszczedny";
    Oszczedny(string _nazwa, int _budzet, string _fav_towar); //konstruktor
    //destruktor jest w Kliencie
    [[nodiscard]] pair<int, string> wybierz() const override;
};
class Tradycjonalista: public Konkretny_produkt {
private:
    Loc polozenie;
public:
    //konstruktor z polozeniem
    Tradycjonalista(string _nazwa, int _budzet, string _fav_towar, int _x, int _y);
    //destruktor jest w Kliencie
    const string strategia = "Tradycjonalista";
    [[nodiscard]] pair<int, string> wybierz() const override;
};

#endif //PROJEKT_ZAL_MIASTO_H
