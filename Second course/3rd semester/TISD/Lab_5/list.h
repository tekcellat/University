#ifndef _LIST_H
#define _LIST_H


#include "request.h"

#pragma pack(push, 1)
struct list_member{
	struct request request;
	struct list_member *next;
};

struct list_order{
	struct list_member *first;
	struct list_member *last;
	int len;
};
#pragma pack(pop)

void create_list(struct list_order *list_order);
void free_list(struct list_order list_order);
void list_push(struct list_order *list_order, struct request request);
struct request list_pop(struct list_order *list_order);


#endif