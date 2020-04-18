#ifndef TREE_H
#define TREE_H

#include <stdlib.h>
#include <stdio.h>

typedef struct tree_node{
    char *name;
    struct tree_node *left;
    struct tree_node *right;
} tree_node;

tree_node* create_node(char *name);
void free_node(struct tree_node *node, void *param);
tree_node* insert(tree_node *tree, tree_node *node);
tree_node* del(tree_node *node, char* name);
tree_node* lookup_1(tree_node *tree, char *name);
tree_node* lookup_2(tree_node *tree, char *name);
char* find(tree_node *node, char c);
void apply_pre(tree_node *tree, void (*f)(tree_node*, void*), void *arg);
void apply_in(tree_node *tree, void (*f)(tree_node*, void*), void *arg);
void apply_post(tree_node *tree, void (*f)(tree_node*, void*), void *arg);
void print(struct tree_node *node, void *param);
void export_to_dot(FILE *f, char *tree_name, tree_node *tree);

void addNode(tree_node **head, char *data);
void delNode(tree_node **head, char *data);
tree_node *findnode(tree_node *head, char *data, int *count);

#endif