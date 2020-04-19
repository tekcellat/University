#include "stdafx.h"


int _tmain(int argc, _TCHAR* argv[])
{
	unsigned char m[8][8] = {
		{'1', '1', '1', '1', '1'}, {'2', '2', '2', '2', '2'}, {'3', '3', '3', '3', '3'},
		{'4', '4', '4', '4', '4'}, {'5', '5', '5', '5', '5'}};
	for (int i = 0; i < 8; i++) {
		for (int j = 0; j < 8; j++) printf("%c ", m[i][j]); printf("\n");
	}

	_asm {
		mov esi,0
		mov edi,0
		mov ecx, 8
		dec ecx
		
		diagonal_loop:
			mov ebx, ecx
			add esi, 8
			sub esi, ecx
			mov edi, esi
			add edi, 8
			dec edi
		

			change_loop:
				xchg al, byte ptr m[esi]
				xchg al, byte ptr m[edi]
				xchg al, byte ptr m[esi]
				inc esi
				add edi, 8
				loop change_loop

			mov ecx, ebx
		
			loop diagonal_loop
	}

	for (int i = 0; i < 8; i++) {
		for (int j = 0; j < 8; j++) printf("%c ", m[i][j]); printf("\n");
	}
	{
		unsigned char m[8][8] = {
		{'1', '1', '1', '1', '1'},{'2', '2', '2', '2', '2'},{'3', '3', '3', '3', '3'},
		{'4', '4', '4', '4', '4'},{'5', '5', '5', '5', '5'}};

			for (int i = 0; i < 8; i++) {
				for (int j = i+1; j < 8; j++) {
					
					unsigned char tmp = m[i][j];
					m[i][j] = m[j][i];
					m[j][i] = tmp;
					
				}
				printf("\n");
			}

		for (int i = 0; i < 8; i++) { for (int j = 0; j < 8; j++) printf("%c ", m[i][j]); printf("\n");}
	}
	getchar();
	return 0;
}

