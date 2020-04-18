#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include "func.h"

int number_size(int n){
	int i = 0;
	if (n < 0) n = -n;
	while (n > 0) {
		n = n/10;
		i++;
	}
	return i;
}

int whileMacros(int numberSize, int num, char *buffer, int k){
	while (numberSize > 0){
		int i = numberSize - 1;
		int pw = 1;
		while (i > 0){
			pw = pw * 10;
			i--;
		}
		int o = (((num / pw)%10));
		buffer[k] = o + '0';
		numberSize--;
		k++;
	}
	return k;
}

void my_snprintf(char *buffer, size_t count, const char *format){
	int quantity = 0;
	for (int i = 0; format[i] != '\0'; i++)
		if (format[i] == '%') quantity++;

	va_list vl;
	va_start(vl, format);

	int k = 0;
	for (int j = 0; j < count; j++)	{
		if (format[j] == '%'){
			j++;
			if (format[j] == 'h' && format[j+1] == 'd'){
				j++;
				int d = va_arg(vl, int);
				short int num = (short int)d;
				int numberSize = number_size(num);
				if (numberSize == 0){
					buffer[k] = num + '0';
					k++;
				}
				else { k = whileMacros(numberSize, num, buffer, k); }
			}
			else if (format[j] == 'd'){
				int num = va_arg(vl, int);
				int numberSize = number_size(num);
				k = whileMacros(numberSize, num, buffer, k);
			}
			else if (format[j] == 'c'){
				char name = va_arg(vl, int);
				buffer[k] = name;
				k++;
			}
		}
		else{
			buffer[k] = format[j];
			k++;
		}
		
	}
	va_end(vl);
}