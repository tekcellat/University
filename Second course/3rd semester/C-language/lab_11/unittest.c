#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <string.h>
#include "func.h"

void test(char *buffer, char *testBuffer, int number){
	if (strcmp(buffer, testBuffer) == 0) printf("\nTest %d done.\n", number);
	else printf("\nTest %d error.\n", number);
}

int main(){
	// Test case1 
	char buffer1 [100];
	my_snprintf(buffer1, 100, "Radiohead released %hd albums with more than %d songs%c", 9, 200, '.');
	char testBuffer1[100];
	snprintf(testBuffer1, 100, "Radiohead released %hd albums with more than %d songs%c", 9, 200, '.');
	//

	// Test case2 
	char buffer2 [100];
	my_snprintf(buffer2, 100, "Radiohead released %c albums with more than %d songs%c", '9', 200, '.');
	char testBuffer2[100];
	snprintf(testBuffer2, 100, "Radiohead released %c albums with more than %d songs%c", '9', 200, '.');
	//

	// Test case3 
	char buffer3 [100];
	my_snprintf(buffer3, 100, "Radiohead released %c albums.", '9');
	char testBuffer3[100];
	snprintf(testBuffer3, 100, "Radiohead released %c albums.", '9');
	//

	// Test case4 
	char buffer4 [100];
	my_snprintf(buffer4, 100, "Radiohead released 9 albums.");
	char testBuffer4[100];
	snprintf(testBuffer4, 100, "Radiohead released 9 albums.");
	//

	// Test case4 
	char buffer5 [100];
	my_snprintf(buffer5, 100, "Radiohead released %hd albums with more than %d songs%c", 0xffff0000, 200, '.');
	char testBuffer5[100];
	snprintf(testBuffer5, 100, "Radiohead released %hd albums with more than %d songs%c", 0xffff0000, 200, '.');
	//

	// Compare results
	test(buffer1, testBuffer1, 1);
	test(buffer2, testBuffer2, 2);
	test(buffer3, testBuffer3, 3);
	test(buffer4, testBuffer4, 4);
	test(buffer5, testBuffer5, 5);

	printf("\n");
}