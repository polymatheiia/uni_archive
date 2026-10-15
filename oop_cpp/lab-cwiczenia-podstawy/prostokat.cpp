#include <iostream>
#include<memory>

using namespace std;

class Prostokat {
public:
    Prostokat() = default;
    Prostokat(int _wys, int _szer): wys(_wys), szer(_szer) {}
    ~Prostokat() = default;
    Prostokat(const Prostokat& p) = default;
    Prostokat& operator=(const Prostokat&) = default;
    int pole() {return wys*szer;};
    void ustaw_wys(int _wys) {wys = _wys;};
private:
    int wys;
    int szer;
};

int main() {
    unique_ptr<Prostokat> p1(new Prostokat(10,5));
    //auto p1 = make_unique<Prostokat>(10,5);
    cout <<"Pole pod naszym unique pointerem p1: " << p1-> pole() <<"\n";

    // co sie stanie?
    //unique_ptr<Prostokat> p2(p1);

    // a tu co sie stanie?
    unique_ptr<Prostokat> p2;
    p2 = move(p1);

    //cout <<"Pole pod naszym unique pointerem p1: " << p1-> pole() <<"\n";
    cout <<"Pole pod naszym unique pointerem p2: " << p2-> pole() <<"\n";

    // shared pointer
    shared_ptr<Prostokat> p3(new Prostokat(2,10));
    //auto p3 = make_shared<Prostokat>(2,10);
    cout <<"Pole pod naszym shared pointerem:" <<p3->pole() <<"\n";
    cout <<"Shared pointer wspoldzieli zasob z: " <<p3.use_count() <<"innymi.\n";


    shared_ptr<Prostokat> p4(p3);
    //shared_ptr<Prostokat> p4 = p3;

    cout <<"Pole pod shared pointerem p4: " <<p4->pole() <<"\n";


    p4->ustaw_wys(10);
    cout <<"Pole pod shared pointerem p4 (po ustawieniu): " <<p4->pole() <<"\n";
    cout <<"Pole pod shared pointerem p3 (po ustawieniu): " <<p3->pole() <<"\n";

    cout <<p3.use_count() <<"\n";
    cout <<p4.use_count() <<"\n";

    p2 = move(p4);


}
