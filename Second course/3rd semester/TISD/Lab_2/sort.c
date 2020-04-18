#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "sort.h"
#include "struct.h"

// Сортирует, замеряет время сортировки таблицы bubble и quicksost сортировкой
int sort_table(struct information* array, int n, int *const time_bubble, int *const time_qsort){
	int *array_2 = malloc(n * sizeof(array[0]));
	if (array_2 == NULL) return MEMORY_ALLOCATION_ERROR;
	
	memcpy(array_2, array, n * sizeof(array[0]));
	
	*time_bubble = tick();
	mysort(array, n, sizeof(array[0]), compare_string);
	*time_bubble = tick() - *time_bubble;
	
	*time_qsort = tick();
	qsort(array_2, n, sizeof(array[0]), compare_string);
	*time_qsort = tick() - *time_qsort;
	
	free(array_2);
	return SUCCESS;
}

// Сортирует, замеряет время сортировки массива ключей bubble и quicksost 
int sort_key_array(struct information* array, int n, int **p, int *const time_bubble, int *const time_qsort){
	int *p_2 = malloc(n * sizeof(p[0]));
	
	if (!*time_bubble) *p = realloc(*p, n * sizeof((*p)[0]));
	
	for (int i = 0; i < n; i++) (*p)[i] = i;
	
	memcpy(p_2, *p, n * sizeof((*p)[0]));
	
	*time_bubble = tick();
	mysort(*p, n, sizeof((*p)[0]), compare_key);
	*time_bubble = tick() - *time_bubble;
	
	*time_qsort = tick();
	qsort(*p, n, sizeof((*p)[0]), compare_key);
	*time_qsort = tick() - *time_qsort;
	
	free(p_2);
	return SUCCESS;
}

/**
 * \fn void mysort(void *pbegin, size_t num, size_t size, 
       int (*compare)(const void *, const void *))
 * \brief Сортирует элементы массива модифицированным bubble 
 * \param [in] pbegin Указатель на первый элемент массива
 * \param [in] num Количество элементов массива
 * \param [in] size Размер одного элемента массива
 * \param [in] compare Указатель на функцию-компоратор compare() 
 * \return Код выполнения
 */
void mysort(void *base, size_t num, size_t size, int (*compare)(const void *, const void *)){
    char *pbegin = base;
    char *pend = pbegin + (num - 1) * size; // Правый флаг
    char *ptemp = pbegin;
    
    while (pbegin != pend){
        // Перебор элементов слева направо до флага
        for (char *pi = pbegin; pi < pend; pi += size)
            // Перестановка элементов, если левый больше правого
            (compare(pi, pi + size) > 0) ? 
                swap(pi, pi + size, size), ptemp = pi : 0;
        
        // Перестановка правого флага
        pend = ptemp;
        
        // Перебор элементов справа налево до флага
        for (char *pi = pend - size; pi >= pbegin; pi -= size)
            // Перестановка элементов, если левый больше правого
            (compare(pi, pi + size) > 0) ? 
                swap(pi, pi + size, size), ptemp = pi + size : 0;

        // Перестановка левого флага
        pbegin = ptemp;     
    }
}

/**
 * \fn void swap(void *i, void *j, size_t size)
 * \brief Побайтовая перестановка элементов 
 * \param [in] i Указатель на первый элемент
 * \param [in] j Указатель на второй элемент 
 */
void swap(void *i, void *j, int size){
    int *temp = malloc(size);
    
    memmove(temp, i, size);
	memmove(i, j, size);
    memmove(j, temp, size);
	
	free(temp);
}

unsigned long long tick(void){
    unsigned long long d;
    __asm__ __volatile__ ("rdtsc" : "=A" (d) );
	
    return d;
}

// Компаратор строк
int compare_string(const void *a, const void *b){ return strcmp(((struct information*)a)->country, ((struct information*)b)->country); }

// Компаратор строк по индексу записи
int compare_key(const void *a, const void *b) { extern struct information *array; return strcmp(array[*((int*)a)].country, array[*((int*)b)].country); }