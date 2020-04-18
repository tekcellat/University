#include "tree.h"
#include "btree.h"
#include "functions.h"

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

B_node *new_node(char *data){
    B_node* node = malloc(sizeof(*node));

    node->data = strdup(data);
    node->height = 1;
    node->left = NULL;
    node->right = NULL;

    return node;
}

int max(int a, int b) {return a > b ? a : b;}

int height(B_node *node) {return node ? node->height : 0;}

void recalc(B_node *node) {node->height = 1 + max(height(node->left), height(node->right));}

B_node *rotate_right(B_node* node){
    B_node *q = node->left;

    node->left = q->right;
    q->right = node;

    recalc(node);
    recalc(q);

    return q;
}

B_node *rotate_left(B_node* node){
    B_node *q = node->right;
    node->right = q->left;
    q->left = node;

    recalc(node);
    recalc(q);

    return q;
}

B_node *balance(B_node *node){
    recalc(node);

    if (height(node->left) - height(node->right) == 2){
        if (height(node->left->right) > height(node->left->left)) node->left = rotate_left(node->left);
        return rotate_right(node);
    }
    else if (height(node->right) - height(node->left) == 2){
        if (height(node->right->left) > height(node->right->right)) node->right = rotate_right(node->right);
        return rotate_left(node);
    }

    return node;
}

B_node *search(B_node *node, char *data)
{
    if (!node) return NULL;
    B_node *current_node = node;
    while (current_node)
    {
        int res = strcmp(data, current_node->data);
        if (res == 0) {return current_node;}
        else if ((res > 0) && (current_node->right)) { current_node = current_node->right;}
        else if ((res < 0) && (current_node->left)) {current_node = current_node->left;}
        else {break;}
    }
    return NULL;
}

B_node *B_insert(B_node *node, char *data){
    if (!node) return new_node(data);

    int res = strcmp(data, node->data);
    if (res < 0) node->left = B_insert(node->left, data);
    else if (res > 0) node->right = B_insert(node->right, data);
    else node->data = strdup(data);

    return balance(node);
}

B_node *find_min(B_node *node){
    if (node->left) return find_min(node->left);
    else return node;
}

B_node *remove_min(B_node *node){
    if (!node->left) return node->right;

    node->left = remove_min(node->left);
    return balance(node);
}

B_node *remove_item(B_node *node, char *data){
    if (!node) return NULL;

    int res = strcmp(data, node->data);
    if (res < 0) node -> left = remove_item(node -> left, data);
    else if (res > 0) node -> right = remove_item(node -> right, data);
    else{
        B_node *l = node->left;
        B_node *r = node->right;
        free(node);

        if (r) return l;

        B_node *m = find_min(r);
        m->right = remove_min(r);  
        m->left = l;       

        return balance(m);
    }
    return balance(node);
}

void free_tree(B_node *node){
    if (!node) return;

    free(node->data);
    free_tree(node->left);
    free_tree(node->right);
    free(node);
}

void B_print(B_node *node){
	if (!node) return;
	printf("\n'%s'", node->data);
	B_print(node->left);
	B_print(node->right);
}

void nodeToBnode(tree_node *node, B_node **b_tree){
	if (node){
		*b_tree = B_insert(*b_tree, node->name);
		nodeToBnode(node->left, b_tree);
		nodeToBnode(node->right, b_tree);
	}
}

B_node *findBNode(B_node *head, char *data, int *count){
    int i = 0;
	//unsigned long long t1 = 0, t2 = 0;
	//t1 = tick();
	if (!head) return NULL;
	B_node *current_node = head;
	while (current_node)
	{
		//btree_cmp++;
		int res = strcmp(data, current_node->data);
        i++;
		if (res == 0){
			//t2 = tick();
			//btree_t += t2 - t1;
            *count = i;
			return current_node;
		}
		else if (res > 0) {current_node = current_node->right;}
		else if (res < 0) {current_node = current_node->left;}
		else {break;}
	}
	//t2 = tick();
	//btree_t += t2 - t1;
	return NULL;
}

void apply_pre_b(B_node *tree, void (*f)(B_node*, void*), void *arg){
    if (tree == NULL) return;

    f(tree, arg);
    apply_pre_b(tree->left, f, arg);
    apply_pre_b(tree->right, f, arg);
}

void to_dot_b(B_node *tree, void *param){
    FILE *f = param;

    if (tree->left) fprintf(f, "%s -> %s;\n", tree->data, tree->left->data);

    if (tree->right) fprintf(f, "%s -> %s; \n", tree->data, tree->right->data);
}

void export_to_dot_b(FILE *f, char *tree_name, B_node *tree){
    fprintf(f, "digraph %s {\n", tree_name);
    
    apply_pre_b(tree, to_dot_b, f);

    fprintf(f, "}\n");
}