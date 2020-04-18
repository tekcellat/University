#include <stdio.h>
#include <stdlib.h>
#include <malloc.h>
#include "func.h"

int main(int argc, char * argv[]){
	if (argc < 2){printf("ERROR"); return 1; }
	else{
		FILE *f;
		f = fopen(argv[1],"r");
		if (f){ main_function(f); fclose(f); }
		else printf("Error. No file!");
	}
}