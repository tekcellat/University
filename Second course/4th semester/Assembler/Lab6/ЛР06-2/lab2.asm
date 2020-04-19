.286
STK SEGMENT PARA STACK 'STACK'
	db 100 dup(0)
STK ENDS

DSEG SEGMENT PARA PUBLIC 'DATA'
	X dw 5
	F dw ?
DSEG ENDS

CSEG SEGMENT PARA PUBLIC 'CODE'
	assume CS:CSEG, DS:DSEG, SS:STK
	
factor proc near
	PUSH BP
	MOV  BP, SP

	MOV  DX, [BP+4] ; get N		
	DEC DX
	JNE M1
	MOV AX, 1
	
	POP BP
	RET
M1:
	PUSH [BP + 6]
	PUSH DX
	CALL factor
	ADD SP, 4
	
	MOV DX, [BP + 4]
	MUL DX
	MOV BX, [BP + 6]
	MOV [BX], AX
	POP BP

	RET
factor endp	
	
main:
	MOV AX, DSEG
	MOV DS, AX

	MOV BX, OFFSET F

	PUSH BX
	PUSH X
	
	CALL FACTOR

	ADD SP, 2
	POP BX
	
	
	MOV DX, AX

	MOV AH,02
	INT 21h
	
	MOV AX, 4ch
	INT 21h

CSEG ENDS

END main
