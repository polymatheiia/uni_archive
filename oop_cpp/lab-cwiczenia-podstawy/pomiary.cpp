#include<iostream>

class Pomiary {
public:
    //tworzenie
    Pomiary() = delete;
    Pomiary(int _rozmiar) {
        rozmiar = _rozmiar;
        tab = new double[rozmiar];
        liczbaPomiarow = 0;
    };

    //kasowanie
    ~Pomiary() {delete[] tab;};

    //kopiowanie -- DO NAPISANIA!
    //Pomiary(const Pomiary& pomiar);
    //Pomiary& operator=(const Pomiary& pomiar);

    //drukowanie
    void drukuj() const;

    void dodaj(double wartosc);
    int ilePomiarow() const;
    double srednia();
    double kwartyl(int numer);
    double std_dev();
    double max();
    Pomiary& polacz_proby(const Pomiary& p);

private:
    double* tab;
    int rozmiar;
    int liczbaPomiarow;
};

void Pomiary::drukuj() const {
    for (int i=0; i < liczbaPomiarow-1; ++i) {
        std::cout <<tab[i] <<",";
    }
    std::cout <<tab[liczbaPomiarow-1] <<"\n";
}

// ladnie byloby zeby zwracalo l-wartosc
// to ze w tresci zadania zwraca void to przypadek

void Pomiary::dodaj(double wartosc) {
    if (liczbaPomiarow != rozmiar) {
        tab[liczbaPomiarow] = wartosc;
        ++liczbaPomiarow;
    } else {
        std::cout <<"Przekroczono mozliwa liczbe pomiarow!\n";
    }
}

Pomiary& Pomiary::polacz_proby(const Pomiary& p) {
    std::cout <<"liczba pomiarow wywolywacza:" <<liczbaPomiarow <<" a rozmiar " <<rozmiar <<"\n";
    std::cout <<"liczba pomiarow drugiego: " <<p.liczbaPomiarow <<"\n";
    if (liczbaPomiarow + p.liczbaPomiarow > rozmiar) {
        rozmiar = liczbaPomiarow + p.liczbaPomiarow;
        double* nowa = new double[liczbaPomiarow+ p.liczbaPomiarow];
        for (int i =0; i<liczbaPomiarow; ++i) {
            nowa[i] = tab[i];
        }
        delete[] tab;
        tab = nowa;
    }
    for (int i = 0; i< p.liczbaPomiarow; ++i) {
        tab[liczbaPomiarow++] = p.tab[i];
    }
    std::cout <<"liczba pomiarow wywolywacza: " <<liczbaPomiarow <<"a rozmiar " <<rozmiar <<"\n";
    return *this;
}

int main() {
    Pomiary p(6);
    for (int i=0; i<6; ++i) {
        p.dodaj(double(i));
    }
    p.drukuj();
    Pomiary s(8);
    for (int i =0; i<8; ++i) {
        s.dodaj(double(i));
    }
    p.polacz_proby(s);
    p.drukuj();
    s.drukuj();
}
