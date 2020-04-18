#ifndef BTREE_H
#define BTREE_H

#include "tree.h"

typedef struct B_node{
    char *data;    
    int height;
    struct B_node *left;
    struct B_node *right;
} B_node;

B_node *new_node(char *data);
int max(int a, int b);
int height(B_node *p);
void recalc(B_node *p);
B_node *rotate_right(B_node* p);
B_node *rotate_left(B_node* p);
B_node *balance(B_node *p);
B_node *search(B_node *p, char *data);
B_node *B_insert(B_node *p, char *data);
B_node *find_min(B_node *p);
B_node *remove_min(B_node *p);
B_node *remove_item(B_node *p, char *data);
void free_tree(B_node *p);
void nodeToBnode(tree_node *node, B_node **b_tree);
B_node *findBNode(B_node *head, char *data, int *count);

void export_to_dot_b(FILE *f, char *tree_name, B_node *tree);


#endif