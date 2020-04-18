#include <stdlib.h>
#include "list.h"
#include "request.h"

void create_list(struct list_order *list_order){
    list_order->first = NULL;
	list_order->last = NULL;
	list_order->len = 0;
}

void free_list(struct list_order list_order){ for (int i = 0; i < list_order.len; i++) list_pop(&list_order);}

void list_push(struct list_order *list_order, struct request request){
	struct list_member *list_member = malloc(sizeof(struct list_member));
	
	list_member->request = request;
	(list_order->len)++;
	
	if (list_order->len != 1) (list_order->last)->next = list_member;
	else list_order->first = list_member;
	
	list_order->last = list_member;
}

struct request list_pop(struct list_order *list_order){
	struct request temp = (list_order->first)->request;
	struct list_member *ptemp = list_order->first;
	
	if (list_order->len == 1){ list_order->first = NULL; list_order->last = NULL;}
	else list_order->first = (list_order->first)->next;
	
	(list_order->len)--;
	free(ptemp);
	
	return temp;
}