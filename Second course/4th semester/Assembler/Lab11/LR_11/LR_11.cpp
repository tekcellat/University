#include "stdafx.h"

extern "C" int Dli(char *s);
extern "C" char *CopyStr(char *s1, char *s2, int L);
extern "C" int DelProbel(char *s);

int _tmain(int argc, _TCHAR* argv[]){
	char string[] = "    1234567890  ";
	printf("%s\n", string);

	int new_length = DelProbel(string);
	printf("%s\n", string);

	int len = Dli(string);
	printf("length = %d\n", len);

	CopyStr(string + 3, string + 5, 4);


	return 0;
}

