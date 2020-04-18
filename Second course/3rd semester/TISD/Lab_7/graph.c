#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdbool.h>
 
//Max value = 100
#define INF 50
 
double minBetween(double a, double b) {return a<b ? a : b;}
 
void printMatrix(int** matrix, int numberOfVert){
    printf("\n     ");
    for(int i = 0; i < numberOfVert; i++) printf("%3d ", i);
    printf("\n    ");
    for(int i = 0; i < numberOfVert; i++) printf("----");
    printf("\n");
    for(int i = 0; i < numberOfVert; i++)
    {
        printf("%3d| ", i);
        for(int j = 0; j < numberOfVert; j++) {
            if(matrix[i][j] == INF) {printf("%3c ", '-');}
            else {printf("%3d ", matrix[i][j]);}
        }
        printf("\n");
    }
    printf("\n\n");
}
                        
void floydWarshall(int **matrix, int numberOfVert){
    for(int k = 0; k < numberOfVert; k++)
        for(int i = 0; i < numberOfVert; i++)
            for(int j = 0; j < numberOfVert; j++) matrix[i][j] = minBetween(matrix[i][j], matrix[i][k] + matrix[k][j]);
    return;
}
 
int minKey(int key[], bool mstSet[], int numberOfVert){
    int min = INF, min_index;
     
    for (int v = 0; v < numberOfVert; v++)
        if (mstSet[v] == false && key[v] < min) min = key[v], min_index = v;
     
    return min_index;
}
 
// A utility function to print the constructed MST stored in parent[]
void printOstav(int parent[], int **graph, int numberOfVert){
    printf("Spanning:    Value:\n\n");
    int count = 0;
    for (int i = 1; i < numberOfVert; i++) printf(" %d - %d       %d \n", parent[i], i, graph[i][parent[i]]);
    printf("\n\n");
}
 
void prim(int **graph, int numberOfVert){
    int parent[numberOfVert];
    int key[numberOfVert];
    bool mstSet[numberOfVert];
     
    for (int i = 0; i < numberOfVert; i++) key[i] = INF, mstSet[i] = false;
     
    key[0] = 0;
    parent[0] = -1;
     
    for (int count = 0; count < numberOfVert-1; count++){
        int u = minKey(key, mstSet, numberOfVert);
        mstSet[u] = true;
        for (int v = 0; v < numberOfVert; v++)
            if (graph[u][v] && mstSet[v] == false && graph[u][v] <  key[v]) parent[v]  = u, key[v] = graph[u][v];
    }
    printOstav(parent, graph, numberOfVert);
}
 
void dfs(int **matrix, int numberOfVert, int start, int *visited){
    visited[start] = 1;
    for (int j = start; j < numberOfVert; j++)
        if (matrix[start][j] != INF && start != j) dfs(matrix, numberOfVert, j, visited);
}
 
int main(int argc, char** argv) {
    FILE *f;
    f = fopen("matrix.txt", "r");
    int numberOfVert;
    fscanf(f, "%d", &numberOfVert);
     
    int **matrix = (int**)malloc(sizeof(int)*numberOfVert);
    for(int i = 0; i < numberOfVert; i++)
        matrix[i] = (int *) malloc(sizeof(int) * numberOfVert);
     
    //Считываем матрицу весов ребер
    for(int i = 0; i < numberOfVert; i++)
        for(int j = 0; j < numberOfVert; j++) {fscanf(f, "%d", &matrix[i][j]);}
     
    fclose(f);
     
    printf("-------------------------------------------\n");
    printf("Graph: \n");
    printMatrix(matrix, numberOfVert);
 
    printf("-------------------------------------------\n");
     
    int *visited = (int*)malloc(sizeof(int)*numberOfVert);
    for (int i = 0; i < numberOfVert; i++) *(visited+i) = 0;
    dfs(matrix, numberOfVert, 0, visited);
 
    int flag = 0;
    printf("Checked points: \n\n");
    printf("%3c %3c %3c %3c \n", '0', '1', '2', '3');
    for (int i = 0; i < numberOfVert; i++){
        if (*(visited+i) == 0){ flag = 1; printf("%3c ",'-'); }
        else printf("%3c ",'+');
    }
    if (flag == 0){
        printf("\n\nGraph is connected. \n\n\n");
        printf("-------------------------------------------\n");
        prim(matrix, numberOfVert);
    }
    else printf("\n\nGraph is not connected. \n\n");
    printf("-------------------------------------------\n");

    /*int start = 0;
    printf("Enter the initial top of the minimum value spanner tree: ");
    scanf("%d", &start);
    prim(matrix, numberOfVert, start);
    printf("-------------------------------------------\n");*/
 
  
    floydWarshall(matrix, numberOfVert);
    printf("Count of shortest paths between all points: \n");
    printMatrix(matrix, numberOfVert);
     
    return 0;
}