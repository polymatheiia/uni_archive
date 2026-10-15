#include<iostream>
#include<string>
#include<utility>
#include<vector>
#include<cmath>
#include<algorithm>
#include"miasto.h"

using namespace std;

//tu deklaruję rzeczy globalne
vector<Obiekt_handlowy*> lista_oh;
vector<Siec*> lista_sieci;
vector<Sklep*> lista_sklepow;
vector<Klient*> lista_klientow;
void wypisz_stan() {
    cout << "Stan symulacji w tej chwili jest nastepujacy: " << '\n';
    for (auto i: lista_oh) i->wypisz();
    for (auto i: lista_klientow) i->wypisz();
}

//Loc
[[nodiscard]] double Loc::dist(const Loc& b) const {return(sqrt(pow(x-b.x,2)+pow(y-b.y,2)));} //odległość

//Towar
[[maybe_unused]] void Towar::setCena(int _cena) {cena = _cena;}
void Towar::setIlosc(int _ilosc) {ilosc = _ilosc;}
int Towar::getCena() const { return cena;}
int Towar::getIlosc() const { return ilosc;}

//Sklep
Sklep::Sklep(string _nazwa, int _x, int _y): Obiekt_handlowy(std::move(_nazwa)), polozenie(_x, _y) {
    //dodajemy sklep do listy obiektów i listy sklepów
    lista_oh.push_back(this);
    lista_sklepow.push_back(this);
} //konstruktor
Sklep::~Sklep() {
    //usuwamy sklep z listy obiektów i listy sklepów
    for(auto it = lista_oh.begin(); it != lista_oh.end(); ++it){
        if (nazwa == (*it)->nazwa) lista_oh.erase(it);
    }
    for(auto it = lista_sieci.begin(); it != lista_sieci.end(); ++it){
        if (nazwa == (*it)->nazwa) lista_sieci.erase(it);
    }
} //destruktor
[[nodiscard]] vector<Towar*> Sklep::getOferta() const {return oferta;} //eksport listy towarów
void Sklep::dodaj_towar(string _nazwa, int _cena, int _ilosc) {
    oferta.push_back(new Towar(std::move(_nazwa), _cena, _ilosc));
} //dodawanie towaru do sklepu
void Sklep::setWlasciciel (Siec* net){
    wlasciciel = net;
} //zmiana wLaściciela
pair<int, string> Sklep::sprawdz(string _nazwa) const {
    pair<int, string> wynik = {0, " "};
    for(auto i: oferta){
        if(i->nazwa == _nazwa) {
            wynik.first = i->getCena();
            return wynik;
        }
    }
    return wynik;
} //input - towar, output - cena i nazwa
void Sklep::sprzedaj(string _nazwa) {
    for(auto it = oferta.begin(); it != oferta.end(); ++it){
        if (nazwa == (*it)->nazwa) {
            int il = (*it)->getIlosc() - 1;
            (*it)->setIlosc(il); //zmniejszamy ilość towaru: to nie działa i nie wiem dlaczego
            if ((*it)->getIlosc() == 0) oferta.erase(it); //jeśli towar się wyczerpał, to usuwamy
            break;
        }
    }
} //zmniejszanie liczbę towaru - to z jakiegoś powodu nie działa
void Sklep::uniezaleznij() {
    for(auto it = wlasciciel->wlasnosc.begin(); it != wlasciciel->wlasnosc.end(); ++it){
        if (nazwa == (*it)->nazwa) wlasciciel->wlasnosc.erase(it); //usuwamy element z wlasnosci sieci
    }
    wlasciciel = nullptr; //tracimy wlasciciela
} //wyjście z sieci
void Sklep::wypisz() const {
    cout << "Sklep " << nazwa;
    if (wlasciciel== nullptr) cout << " (niezrzeszony)";
    else cout << " w sieci " << wlasciciel->nazwa;
    cout << " polozony w (" << polozenie.x << "," << polozenie.y << ") ";
    cout << "ma do dyspozycji takie towary: "<<'\n';
    for (auto i: oferta){
        cout << i->nazwa << " (cena: " << i->getCena() << ", ilość: " << i->getIlosc() << "), ";
    }
    cout << '\n';
} //drukowanie

//Siec
Siec::Siec(string _nazwa, double _marza): Obiekt_handlowy(std::move(_nazwa)), marza(_marza) {
    //dodajemy siec do listy obiektów i listy sieci
    lista_oh.push_back(this);
    lista_sieci.push_back(this);
} //konstruktor
Siec::~Siec() {
    //usuwamy siec z listy obiektów i listy sieci
    for(auto it = lista_oh.begin(); it != lista_oh.end(); ++it){
        if (nazwa == (*it)->nazwa) lista_oh.erase(it);
    }
    for(auto it = lista_sieci.begin(); it != lista_sieci.end(); ++it){
        if (nazwa == (*it)->nazwa) lista_sieci.erase(it);
    }
} //destruktor
pair<int, string> Siec::sprawdz(string _nazwa) const {
    pair<int, string> wynik = {0," "};
    for(auto i: wlasnosc){
        wynik = i->sprawdz(_nazwa);//zmuszamy sklep do wewnętrznego sprawdzenia
        if (wynik.first != 0) {
            wynik.second = i->nazwa; //jeśli znalazł, to musimy też zapamiętać ten sklep
            return wynik;
        }
    }
    if(wynik.first!=0) wynik.first += ceil(wynik.first*marza); //tak, moje sieci są złośliwe, biorą sufit!
    return wynik; //jak nie, no to zero
} //para {cena, sklep}
void Siec::sprzedaj(string _nazwa) {
    pair<int, string> zamowienie = sprawdz(_nazwa); //dostajemy nazwę sklepu
    if (zamowienie.first != 0) {
        for (auto i: wlasnosc) {
            if (i->nazwa == zamowienie.second) i->sprzedaj(_nazwa); //inicjujemy sprzedaż w tym sklepie
        }
    }
} //inicjuj sprzedaż w jednym ze sklepów
void Siec::przejmij_sklep (Sklep* sklep) {
    if(sklep->wlasciciel!=nullptr) sklep->uniezaleznij(); //najpierw usuwamy sklep z własności
    sklep->setWlasciciel(this); //ta sieć zostaje włascicielem
    wlasnosc.push_back(sklep); //dodajemy do listy własności
}
void Siec::przejmij_siec (Siec* siec){
    for(auto i: siec->wlasnosc){
        przejmij_sklep(i); //przejmij po kolei każdy sklep
    }
}
void Siec::wypisz() const {
    cout << "Siec " << nazwa << " zawierajaca sklepy: ";
    for (auto i: wlasnosc){
        cout << i->nazwa << ", ";
    }
    cout << "nalicza marze w rozmiarze " << marza*100 << "% od wartosci towaru." << '\n';
}

//Klient
Klient::Klient(string _nazwa, int _budzet): nazwa(std::move(_nazwa)), budzet(_budzet) {
    lista_klientow.push_back(this);
} //konstruktor
Klient::~Klient() {
    for(auto it = lista_klientow.begin(); it != lista_klientow.end(); ++it){
        if (nazwa == (*it)->nazwa) lista_klientow.erase(it);
    }

} //destruktor
void Klient::zaplac(const string& sklep, const string& towar, int cena) {
    for(auto & i : lista_oh){
        if (sklep == i->nazwa) {
            i->sprzedaj(towar); //inicjujemy sprzedaż w tym sklepie
            budzet -= cena; //płacimy
            czy_ma_prezent = true; //jesteśmy szczęśliwi
        }
    }
} //zapłać i dostań towar
bool Klient::check_sklep(const string& sklep) const {
    for(auto i: lista_sklepow) {if(sklep == i->nazwa && i->wlasciciel == nullptr) return true;}
    return false;
} //czy sklep istnieje i jest niezrzeszony
bool Klient::check_sklep_ist(const string& sklep) const {
    for(auto i: lista_sklepow) {if(sklep == i->nazwa) return true;}
    return false;
} //czy sklep istnieje

//Ulubiony_sklep
Ulubiony_sklep::Ulubiony_sklep(string _nazwa, int _budzet, string _fav_sklep):
        Klient(std::move(_nazwa),_budzet), fav_sklep(std::move(_fav_sklep))  {
    //w chwili tworzenia sklep powinien istnieć i nie być siecią
    if (!check_sklep_ist(fav_sklep)) {
        throw invalid_argument("Ulubiony sklep powinien istniec i nie być siecia!");
    }
} //konstruktor
void Ulubiony_sklep::kup() {
    auto wybr = wybierz();
    string wybr_towar = wybr.second; //zwraca nazwę towaru
    int wybr_cena = wybr.first;
    //jeśli wybral prezent, to placi
    if(check_sklep(fav_sklep) && wybr_towar != " ") {
        zaplac(fav_sklep, wybr_towar, wybr_cena);
        czy_ma_prezent = true; //i jest happy
    }
    //jak nie, no to czy_ma_prezent zostaje false
}
vector<Towar*> Ulubiony_sklep::zdobytaLista() const {
    vector<Towar*> zdobycz = {};
    if(check_sklep(fav_sklep)) { //jeśli nasz sklep jest sklepem
        for(auto i: lista_sklepow) {
            if (i->nazwa == fav_sklep) zdobycz = i->getOferta(); //to getterem
        }
    }
    return zdobycz;
} //importuj listę towarów z ulubionego sklepu

void Ulubiony_sklep::wypisz() const {
    cout<< "Klient " << nazwa << " o strategii " << strategia << " posiada " << budzet << " zl ";
    cout<< "i lubi kupowac w " << fav_sklep<< ". ";
    if(czy_ma_prezent) {cout << "Teraz posiada " << wybierz().second << " i cieszy się zyciem! "<<'\n';}
    else {cout << "Nie ma prezentu, wiec nie czuje sie najlepiej. "<<'\n';}
} //drukuj

//Maksymalista
Maksymalista::Maksymalista(string _nazwa, int _budzet, string _fav_sklep):
    Ulubiony_sklep(std::move(_nazwa),_budzet, std::move(_fav_sklep)) {} //konstruktor

pair<int, string> Maksymalista::wybierz() const {
    vector<Towar*> oferta = zdobytaLista();
    pair<int, string> wynik = make_pair(0, " "); //para sklep-sena
    for(auto i: oferta){
        int tmp_cena = i->getCena();
        if(tmp_cena<=budzet && tmp_cena>wynik.first){ //szukamy maksymalnej ceny mieszczącej się w budżecie
            wynik.first = tmp_cena;
            wynik.second = i->nazwa;
        }
    }
    return wynik;
}

//Minimalista
Minimalista::Minimalista(string _nazwa, int _budzet, string _fav_sklep):
        Ulubiony_sklep(std::move(_nazwa),_budzet, std::move(_fav_sklep)) {} //konstruktor
pair<int, string> Minimalista::wybierz() const {
    vector<Towar*> oferta = zdobytaLista();
    pair<int, string> wynik = make_pair(0, " "); //para sklep-sena
    for(auto i: oferta){
        int tmp_cena = i->getCena();
        if(tmp_cena<=budzet && (wynik.first == 0 || tmp_cena < wynik.first)){
            wynik.first = tmp_cena; //szukamy minimalnej ceny mieszczącej się w budżecie
            wynik.second = i->nazwa;
        }
    }
    return wynik;
}

//Losowy
Losowy::Losowy(string _nazwa, int _budzet, string _fav_sklep, int _szanse):
        Ulubiony_sklep(std::move(_nazwa),_budzet, std::move(_fav_sklep)), szanse(_szanse) {} //konstruktor
pair<int, string> Losowy::wybierz() const{
    vector<Towar*> oferta = zdobytaLista();
    pair<int, string> wynik = make_pair(0, " "); //para sklep-sena
    if (check_sklep(fav_sklep)){
        for(int i = 0; i < szanse; ++i){
            //losujemy towar z listy towarów
            int strzal = rand() % oferta.size(); // NOLINT(cert-msc30-c, cert-msc50-cpp)
            int tmp_cena = oferta[strzal]->getCena();
            if (tmp_cena<=budzet) { //jeśli się mieści w budżecie, to kupujemy
                wynik.second = oferta[strzal]->nazwa;
                wynik.first = tmp_cena;
                return wynik;
            }
        }
    }
    return wynik;
}

//Konkretny_produkt
Konkretny_produkt::Konkretny_produkt(string _nazwa, int _budzet, string _fav_towar):
    Klient(std::move(_nazwa), _budzet), fav_towar(std::move(_fav_towar)) {
    //świadomie pozostawiam opcję, że ten konkretny towar nigdzie jeszcze nie istnieje
    //ludzie bardzo często szukają czegoś co w tym mieście się nie sprzedaje
    //jakieś przyszłe wersje programu mogłyby zawierać funkcję importu towaru z innych miast na życzenie klienta
    //więc jak klient nie znajdzie towaru, to nie kupi i trudno, jego problem
} //konstruktor
void Konkretny_produkt::kup() {
    auto wybr = wybierz();
    string wybr_sklep = wybr.second; //zwraca nazwę towaru
    int wybr_cena = wybr.first;
    //jeśli wybral prezent, to placi
    if (wybr_sklep != " ") {
        zaplac(wybr_sklep, fav_towar, wybr_cena);
        czy_ma_prezent = true; //i jest happy
    }
    //jak nie, no to czy_ma_prezent zostaje false
}

void Konkretny_produkt::wypisz() const {
    cout<< "Klient " << nazwa << " o strategii " << strategia << " posiada " << budzet << " zl ";
    cout<< "i ma zamiar kupic " << fav_towar<< ". ";
    if(czy_ma_prezent) {cout << "Ma ten prezent z '" << wybierz().second << "' i cieszy się zyciem! "<<'\n';}
    else {cout << "Nie ma prezentu, wiec nie czuje sie najlepiej. "<<'\n';}
} //drukuj

//Oszczedny
Oszczedny::Oszczedny(string _nazwa, int _budzet, string _fav_towar):
    Konkretny_produkt(std::move(_nazwa),_budzet,std::move(_fav_towar)) {} //konstruktor
pair<int, string> Oszczedny::wybierz() const {
    //przechodzi po liscie obiektow
    pair<int, string> wynik = make_pair(0," "); //para cena-sklep
    for(auto i: lista_oh) {
        pair<int, string> tmp = i->sprawdz(fav_towar); //i wymaga od każdego sklepu cenę tego towaru
        if (tmp.first != 0 && (wynik.first == 0 || tmp.first <= wynik.first)){
            wynik.first = tmp.first; //przechowujemy w iteratorze min cenę
            wynik.second = i->nazwa; //przechowujemy też nazwę sklepu
        }
    }
    return wynik; //kupujemy w sklepie z najmniejszą ceną
}

//Tradycjonalista
Tradycjonalista::Tradycjonalista(string _nazwa, int _budzet, string _fav_towar, int _x, int _y):
Konkretny_produkt(std::move(_nazwa), _budzet, std::move(_fav_towar)), polozenie(_x, _y){} //konstruktor
pair<int, string> Tradycjonalista::wybierz() const {
    double odleglosc = -1;
    pair<int, string> wynik = make_pair(0, " "); //para sklep-sena
    for(auto i: lista_sklepow) { //przechodzimy po liscie sklepow
        double tmp_odl = polozenie.dist(i->polozenie);
        int tmp_cena = i->sprawdz(fav_towar).first;
        if(i->wlasciciel == nullptr && (odleglosc == -1 || tmp_odl<odleglosc) && tmp_cena != 0 && tmp_cena<=budzet) {
            //minimalizujemy odległość i sprawdzamy czy mieści się w budżecie
            odleglosc = tmp_odl;
            wynik.second = i->nazwa;
            wynik.first = tmp_cena;
        }
    }
    return wynik;
}
