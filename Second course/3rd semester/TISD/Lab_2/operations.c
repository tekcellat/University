#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "file_handling.h"
#include "operations.h"
#include "struct.h"

// Считывает данные и добавляет запись в массив структур
int add_record(struct information** inform, int* const n){
	struct information new;
	
    if ((printf("Country: "), (new.country = read_word(stdin)) == NULL) ||
		(printf("Population: "), scanf("%d", &(new.population)) != 1) ||
	    (printf("Capital: "), (new.capital = read_word(stdin)) == NULL) ||
		(printf("Continent: "), (new.continent = read_word(stdin)) == NULL)
		|| (printf("Tourism type(excursions/beach/sport): "), 
		(new.tourism_type = read_word(stdin)) == NULL))
        return INPUT_ERROR;
		
		if (strcmp(new.tourism_type, "excursions") == 0){
			if ((printf("Number of objects: "), 
			    scanf("%d", &(new.n_objects)) != 1) ||
		        (printf("Excursion type(nature/history/art): "), 
				(new.excursion_type = read_word(stdin)) == NULL))
                return INPUT_ERROR;
			
			if (strcmp(new.excursion_type, "nature") != 0 &&
                strcmp(new.excursion_type, "history") != 0 &&
                strcmp(new.excursion_type, "art") != 0)
                return INPUT_ERROR;
        }				

		else if (strcmp(new.tourism_type, "beach") == 0){
			if (((printf("Season: "), 
			    new.season = read_word(stdin)) == NULL) ||
		        (printf("Water temperature: "), 
				scanf("%d", &(new.t_water)) != 1) ||
				(printf("Air temperature: "), scanf("%d", &(new.t_air)) != 1)
				|| (printf("Time to fly: "), scanf("%d", &(new.time)) != 1))
                return INPUT_ERROR;			
		}

        else if (strcmp(new.tourism_type, "sport") == 0){
			if ((printf("Sport type(skiing/surfing/climbing): "), 
			    (new.sport_type = read_word(stdin)) == NULL) || 
                (strcmp(new.sport_type, "skiing") != 0 &&	
                strcmp(new.sport_type, "surfing") != 0 &&
                strcmp(new.sport_type, "climbing") != 0) ||
		        (printf("Min. price: "), scanf("%d", &(new.min_price)) != 1))
                return INPUT_ERROR;	
        }		
        
        else
            return INPUT_ERROR;			
	
    *inform = realloc(*inform, (*n + 1) * sizeof((*inform)[0]));
    if (*inform == NULL) return MEMORY_ALLOCATION_ERROR;	
	
	(*inform)[*n] = new;
	*n = *n + 1;
	
	return SUCCESS;
}

// Выводит страны по континенту и виду туризма
int find_country(struct information* array, const int n, char *continent, char *tourism_type){
	int flag = 0;
	
	for (int i = 0; i < n; i++)
		if (strcmp(array[i].continent, continent) == 0 &&
	        strcmp(array[i].tourism_type, tourism_type) == 0){
			if (flag == 0){
				flag = 1;
                printf("-----------------------------------------------\n"
	            "Format:\nOther for excursions: number of objects, excursion type\n"
		        "Other for beach: season, water temperature, air temperature, time "
		        "to fly\nOther for sport: sport type, minimum price\n\n"
		        "\nCountry      Population Capital    Continent  Tourism type| Other"
		        "\n- - - - - - - - - - - - - - - - - - - - - - - -\n");				
			}
			
			printf("%-12s %-10d %-12s %-10s %-10s ", array[i].country,
		        array[i].population, array[i].capital, array[i].continent,
			    array[i].tourism_type);
		
		    if (strcmp(array[i].tourism_type, "excursions") == 0)
                printf("%-9d %-7s\n", array[i].n_objects,
		            array[i].excursion_type);

            else if (strcmp(array[i].tourism_type, "beach") == 0)
                printf("%-9s %-7d %-3d %-2d\n", array[i].season,
		            array[i].t_water, array[i].t_air, array[i].time);	

            else if (strcmp(array[i].tourism_type, "sport") == 0)
                printf("%-9s %-7d\n", array[i].sport_type, array[i].min_price);
	    }
	
	if (flag == 0)
		return NOTHING_FOUND;
	return SUCCESS;
}

// Удаляет запись из массива по названию страны
int delete_record(struct information** inform, const char* const deleted_country, int* const n){
	int flag = 0; //  Был ли удален элемент
	int last_checked = 0; // Индекс за последним проверенным элементом
	
	while (last_checked != *n)	
        for (int i = last_checked; i < *n; i++){
		    if (strcmp((*inform)[i].country, deleted_country) == 0){
		        memmove(*inform + i, *inform + i + 1,
				    (*n - i - 1) * sizeof((*inform)[0]));
                *inform = realloc(*inform, (*n - 1) * sizeof((*inform)[0]));	
			    if (*inform == NULL) return MEMORY_ALLOCATION_ERROR;
				
			    *n = *n - 1;
				flag = 1;
				
				break;
            }
			
			last_checked = i + 1;
        }

    if (!flag) return NOTHING_DELETED;
    
    return SUCCESS;	
}

// Выводит таблицу на экран
void write(FILE *f, const struct information* const array, const int n){
    for (int i = 0; i < n; i++){
		fprintf(f, "%-12s %-10d %-12s %-10s %-10s ", array[i].country,
		    array[i].population, array[i].capital, array[i].continent,
			array[i].tourism_type);
		
		if (strcmp(array[i].tourism_type, "excursions") == 0)
            fprintf(f, "%-9d %-7s\n", array[i].n_objects,
		        array[i].excursion_type);

        else if (strcmp(array[i].tourism_type, "beach") == 0)
            fprintf(f, "%-9s %-7d %-3d %-2d\n", array[i].season,
		        array[i].t_water, array[i].t_air, array[i].time);	

        else if (strcmp(array[i].tourism_type, "sport") == 0)
            fprintf(f, "%-9s %-7d\n", array[i].sport_type, array[i].min_price);	
    }		
}

// Выводит таблицу и её заголовок
void print(const struct information* const array, const int n){
	printf("-----------------------------------------------\n"
	    "Format:\nOther for excursions: number of objects, excursion type\n"
		"Other for beach: season, water temperature, air temperature, time "
		"to fly\nOther for sport: sport type, minimum price\n\n"
		"\nCountry      Population Capital    Continent  Tourism type| Other"
		"\n- - - - - - - - - - - - - - - - - - - - - - - -\n");
	
	write(stdout, array, n);
	printf("-----------------------------------------------\n\n");
}