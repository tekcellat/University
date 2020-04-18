#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <assert.h>

#include "tree.h"
#include "btree.h"
#include "functions.h"

void print_b_tree(struct B_node *tree, int n){
    if (tree->left) print_b_tree(tree->left, n + 5);
    for (int i = 0; i < n; i++) printf("  ");
    printf("%s\n\n", tree->data);
    if (tree->right) print_b_tree(tree->right, n + 5);
}

void print_tree(struct tree_node *tree, int n){
    if (tree->left) print_tree(tree->left, n + 5);
    for (int i = 0; i < n; i++) printf("  ");
    printf("%s\n\n", tree->name);
    if (tree->right) print_tree(tree->right, n + 5);
}

int main(){
    
    struct tree_node *tree = NULL;
    struct tree_node *node;
    int size = 0;
    
    FILE *f1 = fopen("tree.txt", "r");
    char * buf = malloc(sizeof(char)*LEN);
    
    while (fscanf(f1,"%s", buf) != EOF){
        node = create_node(buf);
        assert(node);
        assert(lookup_2(tree, node->name) == NULL);
        tree = insert(tree, node); 
        buf = malloc(LEN * sizeof(char));
        size++;
    }
   
    B_node *b_tree = NULL;
	nodeToBnode(tree, &b_tree);

	char *hash_table_open[HTABLE_SIZE][LINKLIST_SIZE];
	char *hash_table_close[HTABLE_SIZE];
    
 
	for (int i = 0; i < HTABLE_SIZE; i++){
		hash_table_close[i] = NULL;
		for (int j = 0; j < LINKLIST_SIZE; j++) { hash_table_open[i][j] = NULL; }
	}

	nodeToHTableClosed(tree, hash_table_close);
	nodeToHTableOpen(tree, hash_table_open); 
   
    int choice = -1;
    setbuf(stdout, NULL);
    
    while(choice != 0){
        FILE *f = fopen("tree_dot.gv", "w");
        assert(f);  
        export_to_dot(f, "tree", tree);
        fclose(f);
        
        FILE *f2 = fopen("treeB_dot.gv", "w");
        assert(f2);  
        export_to_dot_b(f2, "balanced_tree", b_tree);
        fclose(f2);
        int count_t = 0;
        char * word = malloc(sizeof(char)*LEN);
        

        printf("\n\nShow tree/balanced tree/open hash table/closed hash table/compare time/search/exit (1/2/3/4/5/6/0): ");

        if(scanf("%d", &choice) == 1){
            if(0 <= choice && choice <= 6){
                switch (choice){
                    case 1:
                        printf("\n\n");
                        print_tree(tree, 5);
                        break; 
                    case 2:
                        printf("\n\n");
                        print_b_tree(b_tree, 5);
                        break;
                    case 3:
                        showHTableOpen(hash_table_open, HTABLE_SIZE);
                        break;		
                    case 4:
                        showHTableClose(hash_table_close, HTABLE_SIZE);
                        break;
                    case 5:
                        setbuf(stdout, NULL);
                        setbuf(stdin, NULL);
                        compare();
                        break;
                    case 6:
                        printf("Input word for seach: ");
                        scanf("%s", word);
                        tree_node *search = findnode(tree, word, &count_t);
                        if (search == NULL){
                            node = create_node(word);
                            assert(node);
                            assert(lookup_2(search, node->name) == NULL);
                            tree = insert(tree, node);
                            size++;
                            b_tree = NULL;
                            nodeToBnode(tree, &b_tree);
                            nodeToHTableClosed(node, hash_table_close);
                            nodeToHTableOpen(node, hash_table_open);
                            printf("Word doesn't exist. ");
                        }
                        else { printf("\nWord %s exist. \n", search->name); }
                        break;
                    case 0:
                        break;
                }
            }
            else
                printf("\nError\n");
        }
        else {printf("Error"); break;}
    }
    apply_post(tree, free_node, NULL);
    fclose(f1);
}
