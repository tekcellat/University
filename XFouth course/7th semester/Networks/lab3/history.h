#ifndef HISTORY_H
#define HISTORY_H

#include "common.h"

typedef struct user_t
{
    SA_IN id;
    uint32_t page_num;
    char *pages[PAGE_MAX];
} user;

typedef struct history_t
{
    uint32_t user_num, capacity, curr_index;
    user *users;
} history;

extern history *create(uint32_t);
extern int compare(SA_IN, SA_IN);
extern void show_log(const history *);

#endif