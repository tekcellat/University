#include <stdio.h>
#include <stdlib.h>
#include <malloc.h>
#include "func.h"


int main_function(FILE *f){
	Node* head = NULL;
	int quantity = 0;
	fscanf(f, "%d", &quantity);
	fromFileToList(&head, f, quantity);
	Node* new_head = NULL;
	copy(head, &new_head);
	writeToFile(new_head);
	sort(&new_head, compare);
	printf("\nList: ");
	printAll(head);
	printf("Sorted list: ");
	printAll(new_head);
	printf("Pop back element: %d \n", (*(int *)pop_back(&head)));
	printf("\nPop front element: %d \n\n", (*(int *)pop_front(&head)));
	printf("List after pop_back and pop_front: ");
	printAll(head);
	while(head->next){
		Node *tmp = head->next;
		free(head->data);
		free(head);
		head = tmp->next;
	}
	free(head);

	return 0;
}

void writeToFile(Node *head){
	FILE *fo;
	fo = fopen("out.txt","w");
	if (fo){
		while(head){
			int c = *((int *)head->data);
			fprintf(fo, "%d", c);
			head = head->next;
		}
		fclose(fo);
	}
	else printf("Error. No file!");
}

void fromFileToList(Node **head, FILE *f, int quantity){
	for(int i = 0; i < quantity; i++){
		int number = 0;
		fscanf(f, "%d", &number);
		add(head, number);
	}
}

void add(Node **head, int data){
	Node *tmp = (Node*)malloc(sizeof(Node));
	int *newData = (int *)malloc(sizeof(int));
	if (tmp && newData){
		*newData = data;
		tmp->data = newData;
		tmp->next = *head;
		*head = tmp;
	}
	else{
		if (newData) free(newData);
		else if (tmp) free(tmp);
		printf("Error. No memory!");
	}
}

void* pop_back(Node **head){
	if (!(*head)) return NULL;

	void *back;
	if (!((*head)->next)){
		back = (*head)->data;
		free(*head);
		*head = NULL;
	}
	else{
		Node *current = *head;
		Node *former;

		while (current->next){
			former = current;
			current = current->next;
		}

		back = current->data;
		free(former->next);
		former->next = NULL;
	}
	return back;
}

void* pop_front(Node **head){
	Node *node;
	void *front = NULL;

	if(head){
		node = *head;
		front = node->data;
		*head = (*head)->next;

		free(node);
		node = NULL;
	}
	return front;
}


void copy(Node *head, Node **new_head){
	while(head){
		Node *tmp = (Node*)malloc(sizeof(Node));
		if (tmp){
			tmp->data = head->data;
			tmp->next = *new_head;
			*new_head = tmp;
			head = head->next;
		}
		else printf("Error memory. ");
	}
	*new_head = reverse(*new_head);
}

Node *reverse(Node *head){
	Node *new_head = NULL;

	while (head){
		Node *tmp = head->next;
		head->next = new_head;
		new_head = head;
		head = tmp;
	}

	return new_head;
}

void printAll(Node *head)
{
	while (head){ printf("%d ", *((int *)head->data)); head = head->next; }
	printf("\n\n");
}

int compare(const void* element1, const void* element2){
	if (element1 == NULL || element2 == NULL){
		if (element1 != element2) return 1;
		return 0;
	}
	if (*(int *)element1 > *(int *)element2) return 1;
	if (*(int *)element1 < *(int *)element2) return -1;
	return 0;
}

void sort(Node** head, int (*comparator)(const void *, const void *)){
	Node* cursor = (*head)->next;
	Node* prev = *head;
	while (cursor){
		Node* kill = cursor;
		cursor = cursor->next;
		prev->next = kill->next;
		sorted_insert(head, kill, comparator);

		Node* tmp = *head;
		while(tmp->next != cursor) tmp = tmp->next;
		prev = tmp;
	}
}

void sorted_insert(Node **head, Node *element, int (*comparator)(const void *, const void *)){
	Node* cursor = *head;
	while (cursor){
		if (comparator(element->data, cursor->data) <= 0){ insert(head, element, cursor); return;}
		cursor = cursor->next;
	}
	insert(head, element, cursor);
}

void insert(Node **head, Node *element, Node *before){
	Node* after = *head;
	if (after != before){
		while(after->next != before){
			if (!(after->next)) return;
			after = after->next;
		}

		after->next = element;

		if (before != element) element->next = before;
	}
	else{ element->next = *head; *head = element; }
}
