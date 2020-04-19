// 12lab.cpp: определяет точку входа для консольного приложения.
#include "stdafx.h"


extern "C" {
	void START(void);
}

int _tmain(int argc, _TCHAR* argv[])
{
	START();
	return 0;
}