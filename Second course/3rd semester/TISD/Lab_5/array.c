#include <stdlib.h>
#include "array.h"
#include "request.h"

void create_array(struct array_order *array_order, int len){
    array_order->pleft = malloc(len * sizeof(struct request));
	array_order->pright = array_order->pleft + len - 1;
	array_order->pin = array_order->pleft;
	array_order->pout = array_order->pleft;
	array_order->len = 0;
}

void free_array(struct array_order array_order){ free(array_order.pleft);}

int array_push(struct array_order *array_order, struct request request){
	if (array_order->pin == array_order->pout && array_order->len > 0) return UNSUCCESS;
	
	(array_order->len)++;
	*(array_order->pin) = request;
	(array_order->pin)++;
	if (array_order->pin > array_order->pright) array_order->pin = array_order->pleft;
	
	return SUCCESS;
}

struct request array_pop(struct array_order *array_order){
	struct request *temp;
	
	(array_order->len)--;
	temp = array_order->pout;
	(array_order->pout)++;
	if (array_order->pout > array_order->pright) array_order->pout = array_order->pleft;
	
	return *temp;
}