#include <stdio.h>
#include <stdlib.h>

// struktura wierzcholka w liscie incydencji
typedef struct adj_list_node {
    int id;
    struct adj_list_node *next;
} adj_list_node, *adj_list_node_p;

// struktura listy incydencji
typedef struct adj_list {
    adj_list_node_p head;
} adj_list, *adj_list_p;

// struktura reprezentujaca graf
typedef struct graph {
    int V;
    adj_list_p array;
} graph, *graph_p;

// funkcja, ktora inicjalizuje graf
graph_p create_graph(int V){
    graph_p g = malloc(sizeof(graph_p));
    g->V = V;

    g->array = malloc(V * sizeof(adj_list));
    int i;
    for(i = 0; i < V; i++){
        g->array[i].head = NULL;
    }
    return g;
}

// funkcja, ktora tworzy nowy element, ktory nastepnie bedzie dodawany do odpowiedniej listy
adj_list_node_p new_adj_node(int id){
    adj_list_node_p new_node = malloc(sizeof(adj_list_node));
    new_node->id = id;
    new_node->next = NULL;
    return new_node;
}

// procedura, ktora dodaje krawedzie w grafie
void add_edge(graph_p g, int src, int dest){
    // 1. tworzymy wierzcholek o zadanym id
    // 2. dodajemy wierzcholek do odpowiedniej listy
    adj_list_node_p new_node = new_adj_node(dest);
    new_node->next = g->array[src].head;
    g->array[src].head = new_node;
    // w przypadku grafu nieskierowanego moglibysmy jeszcze "w druga strone" do "dest" dodac element "src"
}

// funkcja, ktora drukuje liste incydencji
void print_graph(graph_p g){
    int v;
    for(v = 0; v < g->V; v++){
        adj_list_node_p act_list = g->array[v].head;
        printf("Source vertex: %d \n", v);
        while (act_list){
            printf("%d ", act_list->id);
            act_list = act_list->next;
        }
        printf("\n");
    }
}

// Zadanie 1(d) 10.05.2021 - sprawdzenie, czy para (u, v) jest krawędzią grafu
// funkcja, ktora zwraca wierzcholek o zadanym id z danej listy incydencji
adj_list_node_p search(adj_list_node_p h, int v){
    while (h != NULL && h->id != v)
        h = h->next;
    return h;
}

// funkcja glowna, ktora zwraca 1 jesli krawedz istnieje oraz 0 jesli nie istnieje
int if_edge(graph_p g, int u, int v){
    return search(g->array[u].head, v) != NULL;
}

// Zadanie 1(e) 10.05.2021 - obliczenie stopnia wej±ciowego i wyj±ciowego ka»dego wierzchoªka grafu
// funkcja pomocnicza, ktora zwraca dlugosc listy
int size(adj_list_node_p h){
    int a = 0;
    while(h != NULL){
        a++;
        h = h->next;
    }
    return a;
}

// funkcja do wyznaczania stopnia wyjscia wierzcholka u
int out_deg(graph_p g, int u){
    if (u >= 0 && u < g->V){
        return size(g->array[u].head);
    }else
        return -1;
}

// funkcja do wyznaczania stopnia wejscia wierzcholka v
int in_deg(graph_p g, int v){
    // counter
    int a = 0;
    // będziemy przechodzić po całej tablicy list incydencji czyli przechodzi po liczbach od 0 do (g->V - 1)
    // potrzebujemy funkcja, która sprawdza, czy istnieje wierzcholek w danej liscie incydencji (inaczej: czy istnieje krawedz) - czyli korzystamy z funkcji search lub if_edge
    if (v >= 0 && v < g->V){
        for (int i = 0; i < g->V; i++){
            if (if_edge(g, i, v))
                a++;
        }
    }else
        a = -1;
    return a;
}

// Zadanie 2 10.05.2021 - Napisz procedur¦, która dla danego grafu G o n wierzchoªkach i tablicy zawieraj¡cej permutacj¦ zbioru {0, . . . , n − 1} sprawdzi czy tablica ta reprezentuje cykl Hamiltona grafu G.
int hamiltonian_cycle(graph_p g, int permutation[]){
    // w zadaniu będziemy przechodzić po kolejnych wierzcholkach zapisanych w tablicy oraz sprawdzac, czy istnieje krawedz pomiedzy nimi
    for (int i = 0; i < g->V - 1; i++){
        if (if_edge(g, permutation[i], permutation[i+1]) == 0)
            return 0;
    }
    return if_edge(g, permutation[g->V - 1], permutation[0]);
}

// [0, 2, 3, 1]



int main()
{
    int V = 7;
    graph_p g = create_graph(V);
    add_edge(g, 0, 1);
    add_edge(g, 1, 0);
    add_edge(g, 1, 2);
    add_edge(g, 1, 4);
    add_edge(g, 2, 5);
    add_edge(g, 2, 3);
    add_edge(g, 3, 0);
    add_edge(g, 3, 4);
    add_edge(g, 4, 4);
    add_edge(g, 4, 3);
    add_edge(g, 4, 5);
    add_edge(g, 5, 6);
    add_edge(g, 6, 6);
    add_edge(g, 6, 0);
    print_graph(g);

    printf("\n");
    printf("Czy istnieje krawedz (2, 5) - odp: %d", if_edge(g, 2, 5));
    printf("\n");
    printf("Czy istnieje krawedz (2, 3) - odp: %d", if_edge(g, 2, 3));
    printf("\n");
    printf("Stopień wyjścia wierzchołka 1 to: %d", out_deg(g, 1));
    printf("\n");
    printf("Stopień wyjścia wierzchołka 1 to: %d", in_deg(g, 1));
    printf("\n");

    int permutation[g->V];
    for (int j=0; j < g->V; j++)
        permutation[j] = j;
    printf("Czy istnieje w grafie g cykl [0, 1, 2, 3, 4, 5, 6] - odp: %d", hamiltonian_cycle(g, permutation));

    return 0;
}
