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

// struktura pozwalajaca przechowywac informacje
// (dlugosc sciezki od wybranego wierzcholka, poprzednik na sciezce) o wierzcholkach
typedef struct graph_node{
    int dist;
    int prev_node;
} graph_node, *graph_node_p;

// struktura reprezentujaca graf
typedef struct graph {
    int V;
    graph_node_p info_v;
    adj_list_p array;
} graph, *graph_p;

// przypomnienie kolejek
typedef adj_list_node_p kolejka;
typedef adj_list_node_p list;

// sprawdzamy, czy kolejka jest pusta
int empty(kolejka q){
    return (q==NULL);
}

// inicjalizacja kolejki
void ini(kolejka *q){
    *q=NULL;
}

// utworzenie nowego elementu listy
list nowy_element(int a){
    list u;
    u=malloc(sizeof(kolejka));
    u->id=a;
    u->next=NULL;
    return u;
}

// wstawiamy wartość do kolejki
void push_back(kolejka *q, int a){
    list u;
    if (*q==NULL){
        *q=nowy_element(a);
    } else {
        u=*q;
        while (u->next != NULL){
            u=u->next;
        }
        u->next=nowy_element(a);
    }
}

// usuwamy wartość z początku kolejki i ją zwracamy - zwracamy 0, gdy kolejka jest pusta
int pop_front(kolejka *q){
    int a = 0;

    if (!empty(*q)){
        list u;
        u=*q;
        *q=(*q)->next;
        a=u->id;
        free(u);
    }
    return a;
}

// funkcja, ktora inicjalizuje graf
graph_p create_graph(int V){
    graph_p g = malloc(sizeof(graph_p));
    g->V = V;
    g->info_v = malloc(V * sizeof(graph_node));
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


void bfs(graph_p g, int s){
    // potrzebujemy kolejki - jedna kolejka na całe przeszukiwanie
    kolejka q;
    ini(&q);

    // inicjalizacja wartosci odleglosci (wstawiamy -1) oraz poprzednikow (wstawiamy -1)
    for (int k=0; k < g->V; k++){
        g->info_v[k].dist = -1;
        g->info_v[k].prev_node = -1;
    }
    // rozpoczynamy od wierzcholka s

    // nastepnie wchodzimy do while, gdzie wykonujemy do czasu gdy !empty(&q)
    // robimy pop_front
    // przechodzi "wszerch" po wszystkich sasiadach
    // bedziemy dodawac do kolejki; push_back

    g->info_v[s].dist=0;
    int u;
    adj_list_node_p act_list;
    push_back(&q, s);
    while (!empty(q)) {
        u = pop_front(&q);
        act_list = g->array[u].head;
        while (act_list != NULL) {
            if(g->info_v[act_list->id].dist == -1){
                push_back(&q, act_list->id);
                g->info_v[act_list->id].dist = g->info_v[u].dist + 1;
                g->info_v[act_list->id].prev_node = u;
            }
            act_list = act_list->next;
        }
    }
}



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
    bfs(g, 1);
    printf("\n");
    return 0;
}
