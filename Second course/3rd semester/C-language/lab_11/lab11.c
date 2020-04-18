#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <string.h>
#include "func.h"

int main(){
	char buffer [100];
	my_snprintf(buffer, 100, "Group released %hd albums with more than %d songs%c", 0xffff0000, 200, '.');

	printf("\n\nResult string: \n");
	puts(buffer);
	snprintf(buffer, 100, "Group released %hd albums with more than %d songs%c", 0xffff0000, 200, '.');
	puts(buffer);
	printf("\n\n");
}