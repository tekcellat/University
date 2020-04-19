DSEG	SEGMENT PARA PUBLIC 'DATA'
	N	DW 5
DSEG	ENDS

SSEG	SEGMENT PARA STACK 'STACK'
		DB	200h DUP(?)
SSEG	ENDS

CSEG	SEGMENT PARA 'CODE'
	ASSUME CS:CSEG, DS:DSEG, SS:SSEG
	Fact proc NEAR
		MOV	BP, SP        ;сохраняем текущее положение указателя sp
		MOV	CX, [BP+2]    ;в cx  первый и последний параметр
		DEC	CX	      ;уменьшаем на единицу
		JNZ	M1	      ;если не ноль, то прыг
		MOV	AX, 1	      ;в АХ аккулируем значение
		RET								
M1:
		PUSH 	CX	      ;запоминаем CX
		CALL	Fact	      ;вызываем fact  / push адрес возврата
		ADD     SP, 2
		MOV	BP, SP	      ;обратные вызовы рекурсии
		MOV	CX, [BP+2]    ;берем косвенно значение из стека
		MUL	CX	      ;перемножаем
		RET		
	Fact ENDP


Start:
	MOV	AX, DSEG
	MOV	DS, AX

	PUSH 	N
	CALL	Fact
	ADD     SP, 2

	MOV	AH, 4Ch
	INT	21h
CSEG	ENDS
		END Start
		END Start