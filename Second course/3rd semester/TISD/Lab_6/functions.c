#include "tree.h"
#include "btree.h"
#include "functions.h"

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

unsigned long long tick(void){
    unsigned long long d;
    __asm__ __volatile__ ("rdtsc" : "=A" (d) );
    return d;
}

void showHTableOpen(char *table[][LINKLIST_SIZE], size_t size){
	printf("\nKey\t\tData");
	for (size_t i = 0; i < size; i++){
		if (table[i][0]) { printf("\n%d\t\t%s", (int) i, table[i][0]); }
		for (size_t j = 1; j < LINKLIST_SIZE; j++)		{ if (table[i][j]) {printf("\t%s", table[i][j]);} }
	}
}

void showHTableClose(char **table, size_t size){
	printf("\nKey\t\tData");
	for (size_t i = 0; i < size; i++) { if (table[i]) {printf("\n%d\t\t%s", (int) i, table[i]);}}
}

int hash(char *data){
	int hash = 0;
	int len = strlen(data);
	for (int i = 0; i < len; i++) { hash += data[i] - 'A'; }
	hash %= 25;
	if (hash + len < HTABLE_SIZE) {hash += len;}
	if (hash < 0) {
		printf("\nInvalid data (key < 0,  returned 0)");
		return 0;
	}
	return hash;
}

void nodeToHTableOpen(tree_node *node, char *htable[][LINKLIST_SIZE]){
	if (node){
		int key = hash(node->name);
		int i = 0;
		while (htable[key][i] && i < LINKLIST_SIZE) { i++; }
		htable[key][i] = node->name;
		nodeToHTableOpen(node->left, htable);
		nodeToHTableOpen(node->right, htable);
	}
}

void nodeToHTableClosed(tree_node *node, char **htable){
	if (node){
		int key = hash(node->name);
		while (htable[key]) { key++; }
		htable[key] = node->name;
		nodeToHTableClosed(node->left, htable);
		nodeToHTableClosed(node->right, htable);
	}
}

void printTreeXfix(tree_node *node, short int direction){
	if (node){
		if (direction == -1) {printf("\n'%s'", node->name);}
		printTreeXfix(node->left, direction);
		if (direction == 0) {printf("\n'%s'", node->name);}
		printTreeXfix(node->right, direction);
		if (direction == 1) {printf("\n'%s'", node->name);}
	}
}

void compare(){
    char* word = "unborn";
    unsigned long long start, end;
    unsigned long long t1, t2, t3, t4;
    int count_t, count_b, count_h = 1, count_c = 1;
    
    char * buf = malloc(sizeof(char)*LEN);
    
    struct tree_node *root = NULL;
    struct tree_node *node;
    
    FILE *f = fopen("tree.txt","r");
    
    while (fscanf(f,"%s", buf) != EOF){
        node = create_node(buf);
        assert(node);
        assert(lookup_2(root, node->name) == NULL);
        root = insert(root, node); 
        buf = malloc(LEN * sizeof(char));
    }    
   
    B_node *b_tree = NULL;
	nodeToBnode(root, &b_tree);
    
    char *hash_table_open[HTABLE_SIZE][LINKLIST_SIZE];
	char *hash_table_close[HTABLE_SIZE];

	for (int i = 0; i < HTABLE_SIZE; i++){
		hash_table_close[i] = NULL;
		for (int j = 0; j < LINKLIST_SIZE; j++) {hash_table_open[i][j] = NULL;}
	}

	nodeToHTableClosed(root, hash_table_close);
	nodeToHTableOpen(root, hash_table_open);
    
    start = tick();
    findnode(root, word, &count_t);
    end = tick();
    t1 = end - start;
    
    start = tick();
    findBNode(b_tree, word, &count_b);
    end = tick();
    t2 = end - start;


    char **linked_list = hash_table_open[hash(word)];
    start = tick();
    while (*linked_list && strcmp(*linked_list, word)){
        linked_list++;
        count_h++;
    }
    end = tick();
    t3 = end - start;

    
    int key = hash(word);
    start = tick();
    while (hash_table_close[key] && strcmp(hash_table_close[key], word)){
        key++;
        count_c++;
    }
    end = tick();
    t4 = end - start;
    
    float time1 = t1 / pow(10, 6);
    float time2 = t2 / pow(10, 6);
    float time3 = t3 / pow(10, 6);
    float time4 = t4 / pow(10, 6);

    printf("\n\nSearch time:\n");
    printf("Tree:           %f\n", time1);
    printf("Balanced tree:  %f\n", time2);
    printf("Open table:     %f\n", time3);
    printf("Closed table:   %f\n", time4);
    
    printf("\nIterations:\n");
    printf("Tree:           %d\n", count_t);
    printf("Balanced tree:  %d\n", count_b);
    printf("Open table:     %d\n", count_h);
    printf("Closed table:   %d\n", count_c);
    
    free(root);
    root = NULL;
    
    free(b_tree);
    b_tree = NULL;
}
