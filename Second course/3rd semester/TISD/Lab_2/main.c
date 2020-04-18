#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include "file_handling.h"
#include "operations.h"
#include "sort.h"
#include "struct.h"

#define WRONG_COMMAND_LINE -1

struct information *array = NULL;

int main(const int argc, const char **argv){
    //struct information *array = NULL;
	int n = 0;
	int status;
	int menu;
	int t_time_bubble = 0, t_time_qsort = 0;
    int	k_time_bubble = 0, k_time_qsort = 0;
	int *key_array = NULL;
	char continent[25], tourism_type[25];
	
	// Проверка параметров командной строки
    if (argc != 2){
        printf("Wrong parameters\nExpected: main.exe <input_file>\n");
		return WRONG_COMMAND_LINE;
	}
	
	// Считывание данных из файла
	status = read_information(argv[1], &array, &n);
	if (status == ERROR_OPENING_FILE){
		printf("Error opening input file: %s\n", strerror(errno));
		return ERROR_OPENING_FILE;
	}
	else if (status == INPUT_ERROR){
		printf("Input error\n");
		return INPUT_ERROR;
	}
	else if (status == EMPTY_ARRAY){
		printf("Empty array\n");
		return EMPTY_ARRAY;
	}
	else if (status == MEMORY_ALLOCATION_ERROR){
		printf("Memory allocation error\n");
		return MEMORY_ALLOCATION_ERROR;
	}
	
	// Цикл меню
	while(1){
		printf("                    MENU:\n                    0. Find country"
		"\n                    1. Print table\n                   "
		" 2. Add record\n                    3. Delete record\n               "
		"     4. Sort table(bubble and qsort)\n                    5. Sort and"
		" print key-array"
		"(bubble and qsort)\n                    6. Print sorted table by key-"
		"array\n                    7. Compare efficiency\n                   "
		" 8. Save to file\n                    9. Quit\n                    --"
        "> ");
		
		// Проверка ввода
		if (scanf("%d", &menu) != 1 || menu < 0 || menu > 9){
			free(array);
			free(key_array);
			printf("Input error\n");
			return INPUT_ERROR;
		}
		
		// Выводит страны по континенту и виду туризма
		else if (menu == 0){
		    printf("\n-----------------------------------------------\n"
		    "Continent: ");
            if (scanf("%s", continent) == 1){
				printf("Tourism type(excursions/beach/sport): ");
				if (scanf("%s", tourism_type) == 1 && (strcmp(tourism_type,
     				"excursions") == 0 || strcmp(tourism_type, "beach") ==
					0 || strcmp(tourism_type, "sport") == 0)){
					if (find_country(array, n, continent, tourism_type))
						printf("Nothing found");
				}
				else
					printf("Input error");
			}
			else
                printf("Input error");	

            printf("\n-----------------------------------------------\n\n");			
		}
		
		// Вывод таблицы
		else if (menu == 1){
		    printf("\n");
			print(array, n);
		}
		
		// Добавление записи
		else if (menu == 2){
			printf("\n-----------------------------------------------\n");
			
			status = add_record(&array, &n);
			if (status == MEMORY_ALLOCATION_ERROR){
				printf("\nMemory allocation error\n");
				free(key_array);
				return status;
			}
			else if (status == INPUT_ERROR)
				printf("\nInput error\n--------------------------------------"
			    "---------\n");
			
			else
			    printf("-----------------------------------------------\n"
			    "Record was added\n---------------------------------------"
			    "--------\n\n");
			
			t_time_bubble = 0;
			t_time_qsort = 0;
			k_time_bubble = 0;
			k_time_qsort = 0;
		}
		
		// Удаление записи
		else if (menu == 3){
			printf("Deleted country: ");
			status = delete_record(&array, read_word(stdin), &n);
			printf("-----------------------------------------------\n");
			if (status == MEMORY_ALLOCATION_ERROR){
				printf("Memory allocation error\n");
				free(key_array);
				return status;
			}
			else if (status == NOTHING_DELETED)
				printf("Nothing deleted\n");
			else
				printf("Done\n");
			
			printf("-----------------------------------------------\n\n");
			
			t_time_bubble = 0;
			t_time_qsort = 0;
			k_time_bubble = 0;
			k_time_qsort = 0;
		}
		
		// Сортировка таблицы пузырьком и быстрой сортировкой 
		else if (menu == 4){
			if (sort_table(array, n, &t_time_bubble, &t_time_qsort)
				== MEMORY_ALLOCATION_ERROR)
			    printf("Memory allocation error\n");
			
			printf("-----------------------------------------------\n"
			"Bubble sort: %d tacts\nQsort: %d tacts\n-----------------------"
			"------------------------\n\n", t_time_bubble, t_time_qsort);
		}
		
		// Сортировка массива ключей
		else if (menu == 5){
			sort_key_array(array, n, &key_array, &k_time_bubble, &k_time_qsort); 
			
			printf("-----------------------------------------------\n"
			"Bubble sort: %d tacts\nQsort: %d tacts\n- - - - - - - - - - - -"
			" - - - - - - - - - - - -\n", k_time_bubble, k_time_qsort);
			
			for (int i = 0; i < n; i++)
				printf("%2d) %-2d %s\n", i + 1, key_array[i],
			        array[key_array[i]].country);
			printf("-----------------------------------------------\n\n");
		}
		
		// Вывод отсортированной таблицы по таблице ключей
		else if (menu == 6){
			if (!k_time_bubble)
				sort_key_array(array, n, &key_array, &k_time_bubble,
			        &k_time_qsort);
			
	        printf("\n-----------------------------------------------\n"
	        "Format:\nOther for excursions: number of objects, excursion type\n"
		    "Other for beach: season, water temperature, air temperature, time "
		    "to fly\nOther for sport: sport type, minimum price\n\n"
		    "\nCountry      Population Capital    Continent  Tourism type| Other"
		    "\n- - - - - - - - - - - - - - - - - - - - - - - -\n");
			
			for (int i, j = 0; j < n; j++){
				i = key_array[j];
				
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
			
			printf("-----------------------------------------------\n\n");
		}
		
		// Анализ эффективности
		else if (menu == 7){
			if (!k_time_bubble)
				sort_key_array(array, n, &key_array, &k_time_bubble,
			        &k_time_qsort);
			
			if (!t_time_bubble) sort_table(array, n, &t_time_bubble, &t_time_qsort);				
			
            printf("\n-----------------------------------------------\n"
			"Efficiency\n\nTime:\n              Table   Key-array\n"
			"Bubble sort:  100%%    %f%%\nQuick sort:   100%%    %f%%",
			(float)k_time_bubble / t_time_bubble * 100, (float)k_time_qsort
			/ t_time_qsort * 100);
			
			printf("\n- - - - - - - - - - - - - - - - - - - - - - - -\n"
			"Memory:\n              Table   Key-array\n"
			"              100%%    %f%%",
			(float)sizeof(key_array[0]) / sizeof(array[0]) * 100 + 100);
			
			printf("\n-----------------------------------------------\n\n");			
		}
		
		// Сохранение таблицы в файл
		else if (menu == 8){
			write_file(argv[1], array, n);
			printf("\n-----------------------------------------------\n"
			"Saved\n-----------------------------------------------\n\n");
		}
		
		// Выход
		else if (menu == 9) break;
	}
	
	free(array);
	return SUCCESS;
} 