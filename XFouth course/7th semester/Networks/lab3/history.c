#include "history.h"

history *create(uint32_t capacity)
{
    history *log = (history *)malloc(sizeof(history));
    log->capacity = capacity;
    log->user_num = 0;
    log->curr_index = 0;
    log->users = (user *)malloc(capacity * sizeof(user));
    return log;
}

int compare(SA_IN a, SA_IN b)
{
    if ((a.sin_addr.s_addr == b.sin_addr.s_addr) &&
        (a.sin_port == b.sin_port))
        return 0;
    else
        return 1;
}

void show_log(const history *log)
{
    printf("\nNumber of visited user: %d\n", log->user_num);

    for (int i = 0; i < log->user_num; i++)
    {
        printf("User [%d] visited %u pages\n", i,
               log->users[i].page_num);
        for (int j = 0; j < log->users[i].page_num; j++)
            printf("\t%s\n", log->users[i].pages[j]);
        printf("\n");
    }
}
