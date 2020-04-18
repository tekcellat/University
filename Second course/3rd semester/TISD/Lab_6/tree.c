#include "tree.h"

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

tree_node* create_node(char *name)
{
    tree_node *node = malloc(sizeof(tree_node));
    if (node){
        node->name = name;
        node->left = NULL;
        node->right = NULL;
    }

    return node;
}

tree_node* insert(tree_node *tree, tree_node *node)
{
    int cmp;

    if (tree == NULL) return node;

    cmp = strcmp(node->name, tree->name);
    if (cmp == 0) assert(0);
    
    else if (cmp < 0) tree->left = insert(tree->left, node);
    
    else tree->right = insert(tree->right, node);

    return tree;
}

tree_node* del(tree_node *node, char* name) 
{
    int cmp = strcmp(node->name, name);
    
    if (cmp == 0)
    {
        if (node->left == NULL && node->right == NULL) {free(node); node = NULL;}
        
        else if (node->left == NULL){
            tree_node *tmp = node;
            node = node->right;
            free(tmp);
            tmp = NULL;

        }
        else if (node->right == NULL){
            tree_node *tmp = node;
            node = node->left;
            free(tmp);
            tmp = NULL;
        }
 
        else{
            tree_node *tmp = node->right;
            while (tmp->left != NULL) tmp = tmp -> left;
            node->name = tmp->name;
            node->right = del(node->right, tmp->name);
        }
    }

    else if (node->left != NULL && cmp > 0) node -> left = del(node->left, name);
    else if (node->right != NULL && cmp < 0) node -> right = del(node->right, name);
    else printf("\nNot found\n");
    
    return node;
}

tree_node* lookup_1(tree_node *tree, char *name){
    int cmp;

    if (tree == NULL) return NULL;

    cmp = strcmp(name, tree->name);
    if (cmp == 0) return tree;
    else if (cmp < 0) return lookup_1(tree->left, name);
    else return lookup_1(tree->right, name);
}

tree_node* lookup_2(tree_node *tree, char *name){
    int cmp;

    while (tree != NULL){
        cmp = strcmp(name, tree->name);
        if (cmp == 0) return tree;
        else if (cmp < 0) tree = tree->left;
        else tree = tree->right;
    }

    return NULL;
}

char* find(tree_node *tree, char c){
    int cmp;
    char * buf;
    buf = malloc(sizeof(char) * 256);
    strcpy(buf, " ");
    if (tree != NULL){
        cmp = strncmp(&c, tree->name, 1);
        if (cmp == 0){
            strcat(buf, tree->name);
            strcat(buf, "[color = red]\n");
            strcat(buf, find(tree->left, c));
            strcat(buf, find(tree->right, c));
        }
        
        
        else if (cmp < 0) strcat(buf, find(tree->left, c));
        else strcat(buf, find(tree->right, c));
    }
    return buf;
}

void apply_pre(tree_node *tree, void (*f)(tree_node*, void*), void *arg){
    if (tree == NULL) return;

    f(tree, arg);
    apply_pre(tree->left, f, arg);
    apply_pre(tree->right, f, arg);
}

void apply_in(tree_node *tree, void (*f)(tree_node*, void*), void *arg){
    if (tree == NULL) return;

    apply_in(tree->left, f, arg);
    f(tree, arg);
    apply_in(tree->right, f, arg);
}

void apply_post(tree_node *tree, void (*f)(tree_node*, void*), void *arg){
    if (tree == NULL) return;

    apply_post(tree->left, f, arg);
    apply_post(tree->right, f, arg);
    f(tree, arg);
}

void print(struct tree_node *node, void *param){
 
    char *fmt = param;

    printf(fmt, node->name);
}

void free_node(struct tree_node *node, void *param) { free(node);}


void to_dot(tree_node *tree, void *param){
    FILE *f = param;

    if (tree->left) fprintf(f, "%s -> %s;\n", tree->name, tree->left->name);

    if (tree->right) fprintf(f, "%s -> %s; \n", tree->name, tree->right->name);
}

void export_to_dot(FILE *f, char *tree_name, tree_node *tree){
    fprintf(f, "digraph %s {\n", tree_name);
    
    apply_pre(tree, to_dot, f);

    fprintf(f, "}\n");
}

tree_node *findnode(tree_node *head, char *data, int *count){
    int i = 0;
	if (!head) return NULL;
	tree_node *current_node = head;
	while (current_node){
		int res = strcmp(data, current_node->name);
        i++;
		if (res == 0){
            *count = i;
			return current_node;
		}
		else if ((res > 0) && (current_node->right)) { current_node = current_node->right;}
		else if ((res < 0) && (current_node->left)) { current_node = current_node->left;}
		else {break;}
	}
	//t2 = tick();
	//tree_t += t2 - t1;
	return NULL;
}