#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "file_handling.h"
#include "operations.h"
#include "struct.h"

// Возвращает считанную до первого пробела или \n строку
char* read_word(FILE *f){
	char *str = malloc(MAX_LEN_STR * sizeof(char));
	char temp;
	int n = 0;
	
	while (fscanf(f, "%c", &temp) == 1){
		if (temp == ' ' || temp == '\n'){ if (n != 0) break;}
		else *(str + n++) = temp;
	}
	
	if (n == 0) return NULL;
	
	*(str + n) = '\0';
	str = realloc(str, (n+1) * sizeof(char));
	
	return str;
}

// Считывает таблицу в массив структур
int read_information(const char *const argv, struct information **p, int *const n){
	FILE *f;
	char temp;
	struct information *array;

	f = fopen(argv, "r");
    if (f == NULL) return ERROR_OPENING_FILE;

    while (fscanf(f, "%c", &temp) == 1) if (temp == '\n') (*n)++;

    if (feof(f) == 0){ fclose(f); return INPUT_ERROR; }
    if (*n == 0){ fclose(f); return EMPTY_ARRAY;}
    
	rewind(f);

    array = malloc(*n * sizeof(struct information));
	*p = array;
    if (array == NULL){ fclose(f); return MEMORY_ALLOCATION_ERROR; }
    
	// Заполнение массива структур
    for (int i = 0; i < *n; i++){
	    if ((array[i].country = read_word(f)) == NULL ||
		    fscanf(f, "%d", &(array[i].population)) != 1 ||
			(array[i].capital = read_word(f)) == NULL ||
			(array[i].continent = read_word(f)) == NULL ||
			(array[i].tourism_type = read_word(f)) == NULL){
            fclose(f);
			free(array);
			return INPUT_ERROR;
		}
		
		if (strcmp(array[i].tourism_type, "excursions") == 0){
			if (fscanf(f, "%d", &(array[i].n_objects)) != 1 ||
		        (array[i].excursion_type = read_word(f)) == NULL){
                fclose(f);
				free(array);
				return INPUT_ERROR;
            }				
		}

		else if (strcmp(array[i].tourism_type, "beach") == 0){
			if ((array[i].season = read_word(f)) == NULL ||
		        fscanf(f, "%d", &(array[i].t_water)) != 1 ||
				fscanf(f, "%d", &(array[i].t_air)) != 1 ||
				fscanf(f, "%d", &(array[i].time)) != 1){
                fclose(f);
				free(array);
				return INPUT_ERROR;
            }				
		}

        else if (strcmp(array[i].tourism_type, "sport") == 0){
			if ((array[i].sport_type = read_word(f)) == NULL ||
		        fscanf(f, "%d", &(array[i].min_price)) != 1){
				fclose(f);
				free(array);
                return INPUT_ERROR;	
			}
        }		
        
        else{
			fclose(f);
			free(array);
            return INPUT_ERROR;
		}

        if (strcmp(array[i].tourism_type, "excursions") == 0 &&
            strcmp(array[i].excursion_type, "nature") != 0 &&
            strcmp(array[i].excursion_type, "history") != 0 &&
            strcmp(array[i].excursion_type, "art") != 0){
			fclose(f);
			free(array);
            return INPUT_ERROR;
		}
			
        else if (strcmp(array[i].tourism_type, "sport") == 0 &&
            strcmp(array[i].sport_type, "skiing") != 0 &&	
            strcmp(array[i].sport_type, "surfing") != 0 &&
            strcmp(array[i].sport_type, "climbing") != 0){
			fclose(f);
			free(array);
            return INPUT_ERROR;
        }			
	}
	
	while (fscanf(f, "%c", &temp) == 1)
	    if (!(temp == '\n' || temp == ' ' || temp == 'I')){
			fclose(f);
			free(array);
		    return INPUT_ERROR;
		}
	
	if (feof(f) == 0){
		fclose(f);
		free(array);
        return INPUT_ERROR;
	}
	
	fclose(f);
	return SUCCESS;
}

// Записывает таблицу в файл
int write_file(const char *const argv, const struct information *const array, const int n){
	FILE *f;

	f = fopen(argv, "w");
    if (f == NULL) return ERROR_OPENING_FILE;

    write(f, array, n);
	
	fclose(f);
	return SUCCESS;
}