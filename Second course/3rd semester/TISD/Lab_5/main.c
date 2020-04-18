#include <stdio.h>
#include "array.h"
#include "list.h"
#include <stdlib.h>
#include "request.h"
#include "array.h"


int main(void){
	int time_1, time_2, type, max_len = 0;
	int proc_time_b, proc_time_e, interv_b, interv_e;
	float input_time, proc_time = -1, my_time = 0;
	int sys_in = 0, sys_out = 0, n_cycles;
	struct request proc_request;
	float waiting_time = 0;
	int machine_worked = 0, num_not_processed = 0, sum_queue_len = 0;

	
	setbuf(stdout, NULL);
	srand(time(NULL));
	/*printf("\nPrint appearing interval for requests\n","Only integers(exp: 4 6): ");
	while (scanf("%d %d", &interv_b, &interv_e) != 2 || interv_b < 0)printf("Wrong input, try again: ");*/
	
	printf("Select type:\n1. Array\n2. List\n-->");
	while (scanf("%d", &type) != 1 || type < 1 || type > 2) printf("Wrong input, try again:\n-->");
	
	if (type == 1){
	printf("\nPrint max length of array: "); while (scanf("%d", &max_len) != 1 || max_len < 1) printf("Wrong input, try again: ");}

	printf("\nPrint appearing interval for requests\n","Only integers(exp: 4 6): ");
	while (scanf("%d %d", &interv_b, &interv_e) != 2 || interv_b >= interv_e || interv_b < 0)printf("Wrong input, try again: ");
	
	//----------------------------------------------------
	
	printf("\nPrint machine processing interval for requests\n"
	"Only integers(exp: 4 6): ");
	while (scanf("%d %d", &proc_time_b, &proc_time_e) != 2 || proc_time_b >= proc_time_e || proc_time_b < 0) printf("Wrong input, try again: ");

	printf("\nPrint number of cycles for one request: ");
	while (scanf("%d", &n_cycles) != 1 || n_cycles < 1) printf("Wrong input, try again: ");
		
	printf("\n- - - - - - - - - - - - - - - - - - - - - - - - - -\n\n");
	
    if (type == 1){	
    	struct array_order array_order;
	    create_array(&array_order, max_len);

		input_time = get_time(interv_b, interv_e);
		
		time_1 = tick();
		
		while (sys_out < 1000){
			if (proc_time < 0 || input_time < proc_time) {
				if (proc_time < 0) waiting_time += input_time;
				
				my_time += input_time;
				proc_time -= input_time;
				input_time = get_time(interv_b, interv_e);

				/*if (array_push(&array_order, create_request(proc_time_b, proc_time_e)) != SUCCESS){ time_2 = tick();*/

				if (array_push(&array_order, create_request(proc_time_b, proc_time_e)) != SUCCESS){
					time_2 = tick();
				    printf("WARNING!!!\nThe queue is full\nNew element was not added to queue\n\n");
					time_1 += (tick() - time_2);
					num_not_processed++;
					//my_time ++; proc_time;
				} else sys_in++;
				
				if (proc_time < 0 && array_order.len){
					proc_request = array_pop(&array_order);
					proc_time = proc_request.proc_time;
				}
			}
			else{
				/*input_time += proc_time;
				my_time += proc_time;
				proc_time = 0;
				//(proc_request.iteration);
				machine_worked++;*/


				input_time -= proc_time;
				my_time += proc_time;
				proc_time = 0;
				
				(proc_request.iteration)++;
				machine_worked++;
				if (proc_request.iteration < n_cycles){
					update_request(&proc_request, proc_time_b, proc_time_e);
					if (array_push(&array_order, proc_request) != SUCCESS){
						time_2 = tick();
				        printf("WARNING!!!\nThe queue is full\nNew element was not added to queue\n\n");
						time_1 += (tick() - time_2);
					    sys_in--;
						num_not_processed++;
						//my_time += proc_time;
					}
				}
				else{
					sum_queue_len += array_order.len;
					sys_out++;
					if (sys_out % 100 == 0){
						time_2 = tick();
						printf("%d. Current queue is %d\n     Average queue is %f\n\n", sys_out, array_order.len, (float)sum_queue_len / sys_out);
						time_1 += (tick() - time_2);} }
				
				if (array_order.len == 0) proc_time = -1;
				else{
					proc_request = array_pop(&array_order);
					proc_time = proc_request.proc_time;
				}
			}
		}
		
		time_2 = tick() - time_1;
		time_1 = sizeof(struct request) * max_len + sizeof(struct array_order);

		//prints
		//.................

		printf("- - - - - - - - - - - - - - - - - - - - - - - - - -\n");
		printf("System has worked for %f (%f%%)\n", my_time, my_time (machine_worked * (proc_time_e + proc_time_b) / 2 + waiting_time) * 100);			
		printf("Number of input requests: %d (%f%%)\n", sys_in, (float)sys_in (my_time / (interv_e + interv_b) * 2) * 100);
		printf("Number of output requests: %d\n", sys_out);
		printf("Machine worked %d times\n", machine_worked);
		printf("Machine has waited for %f\n", waiting_time);
		printf("Average queue was %f\n", (float)sum_queue_len / sys_out);
		printf("Number of not processed requests is %d\n\n", num_not_processed);

		printf("Required time: %d ticks\nRequired memory: %d bytes\n\n", time_2, time_1);
		

		free_array(array_order);
    }
	else{
    	struct list_order list_order;
	    create_list(&list_order);

		input_time = get_time(interv_b, interv_e);
		
		time_1 = tick();
		
		while (sys_out < 1000){
			if (proc_time < 0 || input_time < proc_time){
				if (proc_time < 0) waiting_time += input_time;
				
				my_time += input_time;
				proc_time -= input_time;
				input_time = get_time(interv_b, interv_e);
				
				list_push(&list_order, create_request(proc_time_b, proc_time_e));
				sys_in++;
				
				if (list_order.len > max_len) max_len = list_order.len;
				
				if (proc_time < 0 && list_order.len){
					proc_request = list_pop(&list_order);
					proc_time = proc_request.proc_time;
				}
			}
			else{
				input_time -= proc_time;
				my_time += proc_time;
				proc_time = 0;
				
				(proc_request.iteration)++;
				machine_worked++;
				if (proc_request.iteration < n_cycles){
					update_request(&proc_request, proc_time_b, proc_time_e);
					list_push(&list_order, proc_request);
					
					if (list_order.len > max_len) max_len = list_order.len;
				}
				/*else
				{
					sum_queue_len += list_order.len;
					sys_out++;
					if (sys_out % 100 == 0){
						time_2 = tick();
						printf("%d. Current queue is %d\n     Average queue is %f\n\n", sys_out, list_order.len, (float)sum_queue_len / sys_out);
						time_1 += (tick() - time_2);
					}
				}*/
				
				if (list_order.len == 0) proc_time = -1;
				else{
					proc_request = list_pop(&list_order);
					proc_time = proc_request.proc_time;
				}
			}
		}
		
		time_2 = tick() - time_1;
		time_1 = sizeof(struct list_member) * max_len + sizeof(struct list_order);		

		printf("- - - - - - - - - - - - - - - - - - - - - - - - - -\n");
		printf("System has worked for %f (%f%%)\n", my_time, my_time (machine_worked * (proc_time_e + proc_time_b) / 2 + waiting_time) * 100);			
		printf("Number of input requests: %d (%f%%)\n", sys_in, (float)sys_in (my_time / (interv_e + interv_b) * 2) * 100);
		printf("Number of output requests: %d\n", sys_out);
		printf("Machine worked %d times\n", machine_worked);
		printf("Machine has waited for %f\n", waiting_time);
		printf("Average queue was %f\n", (float)sum_queue_len / sys_out);
		
		printf("Required time: %d ticks\nRequired memory: %d bytes\n\n", time_2, time_1);		

		free_list(list_order);
		
		printf("- - - - - - - - - - - - - - - - - - - - - - - - - -\nDo you want to check fragmentation?\n1. Yes\n2. No\n-->");
		if (scanf("%d", &type) != 1 || type > 2 || type < 1) printf("Wrong input, try again\n-->");
		
		if (type == 2) return SUCCESS;

		//if (type == 3) { free_list(list_order); return SUCCESS;}

		create_list(&list_order);
		
		while (1)
		{
		    printf("\n1. Push\n2. Pop\n3. Exit\n-->");
		    if (scanf("%d", &type) != 1 || type > 3 || type < 1) printf("Wrong input, try again\n-->");
			
			if (type == 3) { free_list(list_order); return SUCCESS;}
			
			if (type == 1){
				list_push(&list_order, proc_request);
				printf("\nElement was added to %p\n", list_order.last);
			}
			else if (type == 2 && list_order.len > 0){
				printf("\nElement was removed from %p\n", list_order.first);
				list_pop(&list_order);
			}
			else printf("\nEmpty list\n");
		}
    }

    return SUCCESS;	
}