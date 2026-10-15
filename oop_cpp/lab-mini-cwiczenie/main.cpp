#include <complex>
#include <iostream>

using namespace std;

int main(int argc, char** argv) {

    for (int iter =0; iter <10; ++iter) {
        // tutaj powiekszylismy, ale wypisane jeszcze stare
        cout <<(iter++) <<" ";
        cout <<(iter) <<" ";
        // tutaj wypisalismy juz nowa wartosc
        cout <<(++iter) <<"\n";
    }
    return 0;
}