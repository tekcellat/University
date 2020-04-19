// Lab_10.cpp:
//

#include "stdafx.h"
#include "iostream" 

extern "C" int DlinaStroki(char *S);
extern "C" char *CopyStr(char *s1, char *s2, int L);

int _tmain(int argc, _TCHAR* argv[])
{
	char str1[] = "test_string_len_18";
	char str2[30] = {0};

	printf("%i\n", DlinaStroki(str1));
	printf("%s\n", CopyStr(str1, str2, 11));
	CopyStr(str2, str2+6, 11);
	printf("%s\n", str2);

	return 0;
}

