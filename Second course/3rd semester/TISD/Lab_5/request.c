#include <stdlib.h>
#include "request.h"

struct request create_request(int proc_b, int proc_e){
	struct request request;
	request.iteration = 0;
	request.proc_time = (float)(rand() % (1000 * (proc_e - proc_b) + 1)) / 1000 + proc_b;
		
	return request;
}

void update_request(struct request *request, int proc_b, int proc_e){
	request->proc_time = (float)(rand() % (1000 * (proc_e - proc_b) + 1))  /1000 + proc_b;	
}

float get_time(int interv_b, int interv_e){
	return (float)(rand() % (100 * (interv_e - interv_b) + 1)) / 100 + interv_b;
}

unsigned long long tick(void){
    unsigned long long d;
    __asm__ __volatile__ ("rdtsc" : "=A" (d) );
	
    return d;
}