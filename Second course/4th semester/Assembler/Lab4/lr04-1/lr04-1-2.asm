PUBLIC output_X
EXTRN X: byte

DS2 SEGMENT AT 0b800h
	CA LABEL byte
	;задание текущей позиции в сегменте
	ORG 80 * 2 * 2 + 2 * 2
	SYMB LABEL word
DS2 ENDS

CSEG SEGMENT PARA PUBLIC 'CODE'
	assume CS:CSEG, ES:DS2
output_X proc near
	;установка сегмента данных DS2
	mov ax, DS2
	mov es, ax
	mov ah, 10
	mov al, X
	mov symb, ax
	ret
output_X endp
CSEG ENDS
END
