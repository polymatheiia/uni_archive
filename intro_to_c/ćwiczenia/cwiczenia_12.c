#include <stdio.h>
#include <stdlib.h>

typedef enum{white, gray, black} colors;

// struktura wierzcholka w liscie incydencji
typedef struct adj_list_node {
    int id;
    struct adj_list_node *next;
} adj_list_node, *adj_list_node_p;

// struktura listy incydencji
typedef struct adj_list {
    adj_list_node_p head;
} adj_list, *adj_list_p;

// struktura pozwalajaca przechowywac informacje (dlugosc sciezki od wybranego wierzcholka, poprzednik na sciezce) o wierzcholkach
typedef struct graph_node{
    colors color;
    int d;
    int f;
    int prev_node;
} graph_node, *graph_node_p;

// struktura reprezentujaca graf
typedef struct graph {
    int V;
    graph_node_p info_v;
    adj_list_p array;
} graph, *graph_p;

// przypomnienie kolejek
typedef adj_list_node_p list;

// sprawdzamy, czy lista jest pusta
int empty(list q){
    return (q==NULL);
}

// usuwamy pierwszy element z listy
void pop_front(list *h){
    if (!empty(*h)){
        list u;
        u=*h;
        *h=(*h)->next;
        free(u);
    }
}

// wstawiamy wartość na początek listy
void push(list *h, int a){
    list u;
    u=malloc(sizeof(adj_list_node));
    u->id=a;
    u->next=*h;
    *h=u;
}

// usuwanie elementu ze srodka listy o podanym kluczu
void remove_from_list(list *h, int u){
    list act = *h;
    list prev = NULL;

    while (act != NULL && act->id != u){
        prev = act;
        act = act->next;
    }
    if (act != NULL){
        if (prev != NULL){
            prev->next = act->next;
            free(act);
        } else {
            pop_front(h);
        }
    }
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

// implementacja algorytmu dfs
void dfs(graph_p g){
    // inicjalizacja
    int time = 0;
    for (int k=0; k < g->V; k++){
        g->info_v[k].color = white;
        g->info_v[k].prev_node = -1;
        g->info_v[k].d = -1;
        g->info_v[k].f = -1;
    }

    // budowe kolejnych drzew lasu przeszukiwania wglab
    for (int k = 0; k < g->V; k++)
        if (g->info_v[k].color == white)
            dfs_visit(g, k, &time);
}


void dfs_visit(graph_p g, int u, int *time){
    // odwiedzamy wierzcholek u
    g->info_v[u].color = gray;
    (*time)++;
    g->info_v[u].d = *time;

    // przegladanie sasiadow u wraz z ich potomkami
    list act_list;
    act_list = g->array[u].head;
    while (act_list != NULL){
        if (g->info_v[act_list->id].color == white){
            g->info_v[act_list->id].prev_node = u;
            dfs_visit(g, act_list->id, time);
        }
        act_list = act_list->next;
    }

    // opuszczamy wierzcholek u
    g->info_v[u].color = black;
    (*time)++;
    g->info_v[u].f = *time;
}

/*
Napisz funkcje, ktora dla danego grafu zorientowanego silnie spojnego
G i krawedzi (u,v) sprawdzi, czy usuniecie tej krawedzi sprawi, ze graf
G przestanie byc silnie spojny.
*/
int strongly_connected(graph_p g, int u, int v){
    /*
    1. usuwamy krawedz - z LI(u) usuwamy element, ktory na kluczu ma v
    2. wykonujemy dfs_visit na wierzcholku u
    3. sprawdzic jaki kolor jest przypisany do v -
        jesli bialy, to graf nie jest silnie spojny,
        jesli czasrny, to graf pozostaje silnie spojny
    */

    // usuwamy krawedz
    remove_from_list(&g->array[u].head, v);

    // przeszukujemy
    // inicjalizacja
    int time = 0;
    for (int k=0; k < g->V; k++){
        g->info_v[k].color = white;
        g->info_v[k].prev_node = -1;
        g->info_v[k].d = -1;
        g->info_v[k].f = -1;
    }
    dfs_visit(g, u, &time);

    // dodajemy krawedz
    push(&g->array[u].head, v);
    // add_edge(g, u, v);

    return g->info_v[u].color == white;
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
    remove_from_list(&g->array[0].head, 1);
    remove_from_list(&g->array[3].head, 4);
    printf("\n");
    printf("Graf po usunieciu krawedzi (0,1) oraz (3,4)");
    printf("\n");
    print_graph(g);

    return 0;
}
