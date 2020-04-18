#ifndef FUNCTIONS_H
#define FUNCTIONS_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LENGTH 15
#define HTABLE_SIZE 80
#define LINKLIST_SIZE 5
#define LEN 40

#define CMD_EXIT -38
#define CMD_SHOW_TREE 1
#define CMD_SHOW_B_TREE 2
#define CMD_SHOW_HASH_TABLE_OPEN 3
#define CMD_SHOW_HASH_TABLE_CLOSE 4
#define CMD_FIND_NODE 5


void printTreeXfix(tree_node *node, short int direction);

int hash(char *data);
void nodeToHTableOpen(tree_node *node, char *htable[][LINKLIST_SIZE]);
void nodeToHTableClosed(tree_node *node, char **htable);
void showHTableOpen(char *table[][LINKLIST_SIZE], size_t size);
void showHTableClose(char **table, size_t size);

void compare(void);

#endif
