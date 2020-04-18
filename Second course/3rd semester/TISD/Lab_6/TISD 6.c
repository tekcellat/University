#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 3

unsigned long tick(void)
{
    unsigned long d;
    __asm__ __volatile__ ("rdtsc" : "=A" (d) );
    return d;
}

enum type
{
    plus,
    minus,
    multiplication,
    devision,
    number
};

typedef struct Tree {
    enum type type;
    int data;
    struct Tree *left;
    struct Tree *right;
    struct Tree *parent;
}Tree;

struct NewNode {
    int data;
    struct NewNode *current;
    struct NewNode *next;
} *Node = NULL;

typedef struct {
    int *array[9];
    unsigned head;
} ArrayStack;

struct Tree **add_node(Tree **tree, char symbol, int A, int B, int C, int D, int E, int F, int G, int H, int I)
{
    if (symbol == '(')
    {
        Tree *tmp = (Tree*)malloc(sizeof(Tree));
        tmp->data = -1;
        tmp->left = NULL;
        tmp->right = NULL;
        tmp->parent = *tree;
        (*tree)->left = tmp;
        *tree = tmp;
    }
    else if (symbol != '+' && symbol != '-' && symbol != '*' && symbol != '/' && symbol != ')')
    {
        if (symbol == 'A')
            (*tree)->data = A;
        if (symbol == 'B')
            (*tree)->data = B;
        if (symbol == 'C')
            (*tree)->data = C;
        if (symbol == 'D')
            (*tree)->data = D;
        if (symbol == 'E')
            (*tree)->data = E;
        if (symbol == 'F')
            (*tree)->data = F;
        if (symbol == 'G')
            (*tree)->data = G;
        if (symbol == 'H')
            (*tree)->data = H;
        if (symbol == 'I')
            (*tree)->data = I;
        (*tree)->type = number;
        tree = &(*tree)->parent;
    }
    else if (symbol == '+' || symbol == '-' || symbol == '*' || symbol == '/')
    {
        if (symbol == '+')
            (*tree)->type = plus;
        if (symbol == '-')
            (*tree)->type = minus;
        if (symbol == '*')
            (*tree)->type = multiplication;
        if (symbol == '/')
            (*tree)->type = devision;
        //printf("%c", symbol);
        (*tree)->data = symbol;
        Tree *tmp = (Tree*)malloc(sizeof(Tree));
        tmp->data = -1;
        tmp->left = NULL;
        tmp->right = NULL;
        tmp->parent = *tree;
        (*tree)->right = tmp;
        tree = &tmp;
    }
    else if (symbol == ')')
        tree = &(*tree)->parent;
    return tree;
}

void addToStack(int data)
{
    struct NewNode *newNode;
    newNode = (struct NewNode*)malloc(sizeof(struct NewNode));
    newNode->current = newNode;
    if (Node == NULL)
        newNode->next = NULL;
    else
        newNode->next = Node;
    newNode->data = data;
    Node = newNode;
}

int deleteFromStack()
{
    int result = 0;
    if (Node == NULL)
        printf("Stack is empty.");
    else
    {
        struct NewNode *t = Node;
        result = Node->data;
        Node = t->next;
        free(t);
    }
    return result;
}

void lastInStack(int prev, int data)
{
    if (Node == NULL)
        printf("Stack is empty.");
    else
    {
        if (data == '+')
            Node->data = Node->data + prev;
        if (data == '-')
            Node->data = Node->data - prev;
        if (data == '*')
            Node->data = Node->data * prev;
        if (data == '/')
            Node->data = Node->data / prev;
    }
}

void build_tree(int A, int B, int C, int D, int E, int F, int G, int H, int I, Tree **tree)
{
    char expression[33] = "(A+(B*(C+(((D*(E+F))-(G-H))+I))))";
    char symbol = 1;
    for (int i = 0; i<29; i++)
    {
        symbol = expression[i];
        tree = add_node(tree, symbol, A, B, C, D, E, F, G, H, I);
    }
}

void print_tree(struct Tree *tree, int n)
{
    if (tree->left)
        print_tree(tree->left, n + 3);
    for (int i = 0; i < n; i++)
        printf(" ");
    if (tree->data != '+' && tree->data != '-' && tree->data != '*' && tree->data != '/' && tree->data != ')')
        printf("%d\n", tree->data);
    else
        printf("%c\n", tree->data);
    if (tree->right)
        print_tree(tree->right, n + 3);
}

void pre_order(Tree* tree)
{
    if (tree) {
        if (tree->data != '+' && tree->data != '-' && tree->data != '*' && tree->data != '/' && tree->data != ')')
            printf("%d ", tree->data);
        else
            printf("%c ", tree->data);
        pre_order(tree->left);
        pre_order(tree->right);
    }
}

void in_order(Tree* tree)
{
    if (tree) {
        in_order(tree->left);
        if (tree->data != '+' && tree->data != '-' && tree->data != '*' && tree->data != '/' && tree->data != ')')
            printf("%d ", tree->data);
        else
            printf("%c ", tree->data);
        in_order(tree->right);
    }
}

void post_order(Tree* tree)
{
    if (tree) {
        post_order(tree->left);
        post_order(tree->right);
        if (tree->data != '+' && tree->data != '-' && tree->data != '*' && tree->data != '/' && tree->data != ')')
            printf("%d ", tree->data);
        else
            printf("%c ", tree->data);
    }
}

void polish_note(Tree* tree)
{
    char expression[17] = "123456+*78--9++*+";
    for (int i = 0; i < 17; i++)
    {
        if (expression[i] != '+' && expression[i] != '-' && expression[i] != '*' && expression[i] != '/' && expression[i] != ')')
        {
            addToStack(expression[i]-'0');
        }
        else
        {
            int prev = deleteFromStack();
            lastInStack(prev, expression[i]);
        }
    }
}

int tree_result(Tree* tree)
{
    if (tree->type != number)
    {
        if (tree->type == plus)
            tree->data = tree_result(tree->left) + tree_result(tree->right);
        if (tree->type == minus)
            tree->data = tree_result(tree->left) - tree_result(tree->right);
        if (tree->type == multiplication)
            tree->data = tree_result(tree->left) * tree_result(tree->right);
        if (tree->type == devision)
            tree->data = tree_result(tree->left) / tree_result(tree->right);
    }
    return tree->data;
}

struct Tree* lookup_1(struct Tree *tree, int name)
{
    if (tree == NULL)
        return NULL;
    
    if (name == tree->data)
    {
        return tree;
    }
    else
    {
        if (lookup_1(tree->left, name) != NULL)
            return lookup_1(tree->left, name);
        else if (lookup_1(tree->right, name) != NULL)
            return lookup_1(tree->right, name);
        else
            return NULL;
    }
}

int main(int argc, const char * argv[]) {
    
    printf("Expression: A + (B * (C + (D * (E + F) - (G - H)) + I))\n\n");
    int A = 1;
    int B = 2;
    int C = 3;
    int D = 4;
    int E = 5;
    int F = 6;
    int G = 7;
    int H = 8;
    int I = 9;
    printf("Input A, B, C, ... (9 numbers): ");
    scanf("%d%d%d%d%d%d%d%d%d", &A, &B, &C, &D, &E, &F, &G, &H, &I);
    Tree *tmp = (Tree*)malloc(sizeof(Tree));
    printf("\n");
    tmp->data = -1;
    tmp->left = NULL;
    tmp->right = NULL;
    tmp->parent = NULL;
    Tree* tree = tmp;
    build_tree(A, B, C, D, E, F, G, H, I, &tree);
    tree = tree->parent;
    
    print_tree(tree, 4);
    
    printf("\nSearch: ");
    Tree *search = tree;
    int find = 0;
    printf("Input element: ");
    scanf("%d", &find);
    search = lookup_1(search, find);
    if (search == NULL)
        printf("Element %d doesn't exist\n", find);
    else
        printf("Element %d exist\n", find);
    //printf("%d\n", search->data);
    
    printf("\nIn order: \n");
    in_order(tree);
    printf("\n\nPre order: \n");
    pre_order(tree);
    printf("\n\nPost order: \n");
    post_order(tree);
    printf("\n\n");
    unsigned long tb1, te1;
    tb1 = tick();
    polish_note(tree);
    te1 = tick();
    //printf("Result = %d\n", Node->data);
    printf("\nTime of polish note = %lu\n", (te1 - tb1) / N);
    unsigned long tb2, te2;
    tb2 = tick();
    int result = tree_result(tree);
    te2 = tick();
    printf("\nTime of tree note   = %lu\n\n", (te2 - tb2) / N);

    printf("Result = %d\n\n", result);
    return 0;
    
}
