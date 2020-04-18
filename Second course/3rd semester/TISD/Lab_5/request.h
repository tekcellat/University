#ifndef _REQUEST_H
#define _REQUEST_H

#pragma pack(push, 1)
struct request{
	float proc_time;
	int iteration;
};
#pragma pack(pop)

struct request create_request(int proc_b, int proc_e);
void update_request(struct request *request, int proc_b, int proc_e);
float get_time(int interv_b, int interv_e);
unsigned long long tick(void);

#endif