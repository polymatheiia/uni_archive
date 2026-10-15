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

// transponowanie grafu
void transpose_graph(graph_p g, graph_p g_t){
    int v;
    for (v = 0; v < g->V; v++){
        adj_list_node_p act_list = g->array[v].head;
        while (act_list){
            add_edge(g_t, act_list->id, v);
            act_list = act_list->next;
        }
    }
}

// read graph
graph_p read_graph(FILE *f){
    // 1. czytamy pierwsza linie i inicjalizujemy graf
    // 2. czytamy linijka po linijce
    // 3. dla kazdej linii wykorzystujemy add_edge, gdzie source jest pierwszym integerem - to robimy w while + while wewnątrz do dodawania krawedzi

    //graph_g g =
    //char line[128];
    //int v;
    //while (fgets(line, sizeof(line), f) != NULL)
    //    fscanf(f, "%i", &v);
    //    printf("%i", v);
    //fclose(f);
    //return g;
}


int main()
{
    int V = 7;
    graph_p g = create_graph(V);
    add_edge(g, 0, 1);
    add_edge(g, 1, 0);
    add_edge(g, 1, 4);
    add_edge(g, 2, 5);
    add_edge(g, 3, 0);
    add_edge(g, 4, 4);
    add_edge(g, 4, 3);
    add_edge(g, 6, 6);
    print_graph(g);

    // transponowanie grafu
    printf("\n Transponowanie grafu \n");
    graph_p g_t = create_graph(g->V);
    transpose_graph(g, g_t);
    print_graph(g_t);

    // read graph from file
    //FILE *f;
    //f = fopen("graph.txt", "r");
    //g = read_graph(f);

    return 0;
}
