#ifndef _ARRAY_H
#define _ARRAY_H

#include "request.h"

#define SUCCESS 0
#define UNSUCCESS -1

#pragma pack(push, 1)
struct array_order{
	struct request *pleft;
	struct request *pright;
	struct request *pin;
	struct request *pout;
	int len;
};
#pragma pack(pop)

void create_array(struct array_order *array_order, int len);
void free_array(struct array_order array_order);
int array_push(struct array_order *array_opder, struct request request);
struct request array_pop(struct array_order *array_opder);

#endif