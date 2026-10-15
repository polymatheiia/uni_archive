#include <stdio.h>
#include <stdlib.h>
#include <iostream>
using namespace std;

class Kostka {
    int scianki;
    int *jakie;

public:
    Kostka() {scianki = 0; jakie = nullptr; }

    Kostka(int s) {
        cout << "Konstruktor, " << s << " scianek\n";
        scianki = s;
        jakie = new int[s];
        for(int i=0; i<s; i++) jakie[i] = i+1;
    }

    int& operator[] (int ktora) {
        return jakie[ktora];
    }

    int operator() (int ile = 1) {
        int suma = 0;
        for(int i=0; i<ile; i++) suma += jakie[rand() % scianki];
        return suma;
    }

    ~Kostka() { cout << "Kostka o " << scianki << " sciankach sie psuje ):\n"; delete[] jakie; }

    //Kostka(const Kostka& a) = delete;
    //Kostka& operator=(const Kostka& a) = delete;


    Kostka(const Kostka& a) {
        cout << "konstruktor kopiujacy, " << a.scianki << " scianek\n";
        scianki = a.scianki;
        jakie = new int[scianki];
        for(int i=0; i<scianki; i++) jakie[i] = a.jakie[i];
    }

    Kostka& operator= (const Kostka& a) {

        if(&a == this) return *this;
        cout << "przypisanie, zwalniamy " << scianki << " scianek\n";
        delete[] jakie;

        scianki = a.scianki;

        cout << "alokujemy " << scianki << " scianek\n";
        jakie = new int[scianki];
        for(int i=0; i<scianki; i++) jakie[i] = a.jakie[i];

        return *this;
    }


    Kostka(Kostka&& a) {
        cout <<"Wywoluje konstruktor przenoszacy!" <<"\n";
        scianki = a.scianki;
        jakie = a.jakie;
        a.jakie = nullptr;
    }

    Kostka& operator= (Kostka&& a) {

        cout << "przenoszacy operator przypisania (obecnie = " << scianki << ", na tymczasowej = " << a.scianki << ")\n";
        /*
        swap(scianki, a.scianki);
        swap(jakie, a.jakie);
        */

        delete[] jakie;

        scianki = a.scianki;
        jakie = a.jakie;

        a.jakie = nullptr;
        a.scianki = 0;

        return *this;
    }

};

Kostka dziwna() {
    // tutaj nie ma kopiowania
    return Kostka(60);
}

Kostka dziwna2() {
    Kostka k(100);
    return k;

}

int main() {

    Kostka k(6);
    k[5] = 10;
    cout <<"Losuje pierwsza Kostka:\n";
    for(int a=0; a<30; a++) cout << k() << ", ";
    cout << "\n";


    cout <<"Pojawia sie druga Kostka:\n";
    Kostka druga = k;
    druga[4] = 20;

    cout <<"Losuje pierwsza Kostka (po pojawieniu sie drugiej):\n";
    for(int a=0; a<30; a++) cout << k() << ", ";
    cout << "\n";

    cout <<"Losuje druga Kostka:\n";
    for(int a=0; a<30; a++) cout << druga() << ", ";
    cout << "\n";


    cout <<"Pojawia sie trzecia Kostka:\n";
    Kostka k3(10);
    cout << "Przypisujemy wynik funkcji dziwna()\n";
    k3 = dziwna2();

    cout << "Po przypisaniu\n";

    cout <<"Bedzie move\n";
    Kostka k4 =  move(k3);

    cout << "Czyscimy:\n";

    return 0;
}
//
// Created by sool on 24.02.23.
//
