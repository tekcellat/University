#include <stdio.h>
#include <stdlib.h>
#include <conio.h>
#include <malloc.h>
#include <time.h>

#define N 3

unsigned long tick(void)
{
  unsigned long d;
  __asm__ __volatile__ ("rdtsc" : "=A" (d) );
  return d;
}
//typedef int stackArray;

struct NewNode {
    struct NewNode *current;
    struct NewNode *next;
} *Node = NULL;

typedef struct {
	int *array[5];	
	unsigned head;
} ArrayStack;

void initStackArray(ArrayStack *stack);
void newElement(ArrayStack *stack);
int StackFull(ArrayStack *stack);
int StackEmpty(ArrayStack *stack);
void deleteElement(ArrayStack *stack);
void printElement(ArrayStack *stack);

void addToStack();
void deleteFromStack();
void printStack();

int main() {
	int flag = 0;
	printf("Array or list (array - 1 || list - 2): ");
	scanf("%d", &flag);
	if (flag == 1){
		unsigned long tb1, te1, tb2, te2, tb3, te3;
		printf("Array stack.\n");
		ArrayStack stack;
		int result;
		initStackArray(&stack);
		int action = -1;
		while (action != 0){
			printf("\nDo you want to add / delete / print elements? (1 / 2 / 3 / exit = 0): ");
			scanf("%d", &action);
			if (action == 1){
				tb1 = tick();
				newElement(&stack);
				te1 = tick();
			}
			else if (action == 2){
				tb2 = tick();
				deleteElement(&stack);
				te2 = tick();
			}
			else if (action == 3){
				tb3 = tick();
				printElement(&stack);
				te3 = tick();
			}
		}
		printf("\nTime add = %lu\n", ((te1 - tb1) / N));
		printf("\nTime delete = %lu\n", ((te2 - tb2) / N));
		printf("\nTime print = %lu\n", ((te3 - tb3) / N));
	}
	else if (flag == 2){
		unsigned long tb1, te1, tb2, te2, tb3, te3;
		printf("List stack.\n");
		printf("Input quantity of elements: ");
		int elements = 0;
		scanf("%d", &elements);
		for (int i = 0; i < elements + 1; i++){ addToStack(); }
		int j = 4;
		while (j != 0){
			printf("\nDelete / add / print elements? (1, 2, 3, exit = 0): ");
			scanf("%d", &j);
			if (j == 1){
				tb2 = tick();
				deleteFromStack();
				te2 = tick();
			}
			else if (j==2){
				tb1 = tick();
				addToStack();
				te1 = tick();
			}
			else if (j == 3){
				tb3 = tick();
				printStack();
				te3 = tick();
			}
		}
		printf("\nTime add = %lu\n", ((te1 - tb1) / N));
		printf("\nTime delete = %lu\n", ((te2 - tb2) / N));
		printf("\nTime print = %lu\n", ((te3 - tb3) / N));
	}
	getch();
	return 0;
}

void addToStack(){
    struct NewNode *newNode;
    newNode = (struct NewNode*)malloc(sizeof(struct NewNode));
    newNode->current = newNode;
    if (Node == NULL)
    	newNode->next = NULL;
    else
    	newNode->next = Node;
    Node = newNode;
}

void deleteFromStack(){
    if (Node == NULL) printf("Stack is empty.");
    else{
    	struct NewNode *t = Node;
    	Node = t->next;
    	free(t);
    }
}

void printStack(){
  	if (Node == NULL) printf("Stack is empty.");
    else {
        struct NewNode *t = Node;
        while(t->next != NULL){
		    printf("%p ",t->current);
		    t = t -> next;
        }
    }
}

void initStackArray(ArrayStack *stack) { stack->head = 0; }

void newElement(ArrayStack *stack){
	if (StackFull(stack) == 1) printf("Stack is full.");
	else{
		stack->array[stack->head] = stack->array[stack->head];
		stack->head++;
	}
}

void deleteElement(ArrayStack *stack){
	if (StackEmpty(stack) == 1) printf("Stack is empty.");
	else stack->head--;
}

void printElement(ArrayStack *stack){
	int flag = 0;
	int *element = &flag;
	while(StackEmpty(stack) == 0){
		element = stack->array[stack->head - 1];
		stack->head--;
		printf("%p ", element);
	}
}

int StackFull(ArrayStack *stack){ if (stack->head == 5) { return 1;} return 0; }

int StackEmpty(ArrayStack *stack){ if (stack->head == 0) {return 1;} return 0; }