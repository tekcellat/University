EXTRN	M_MenuPrint:NEAR
EXTRN	M_NumInput:NEAR
EXTRN	M_s_bin:NEAR
EXTRN	M_u_bin:NEAR
EXTRN	M_s_dec:NEAR
EXTRN	M_u_dec:NEAR
EXTRN	M_s_hex:NEAR
EXTRN	M_u_hex:NEAR

PUBLIC NewLine

StackSeg	SEGMENT STACK
	DW	128h	DUP (?)
StackSeg	ENDS

DataSeg	SEGMENT PUBLIC
	FuncM	DW	M_MenuPrint,M_NumInput, M_u_bin,M_s_bin, M_u_dec,M_s_dec, M_u_hex,M_s_hex
	X		DW	1
	Ent		DB	'> ','$'
DataSeg	ENDS

CodeSeg	SEGMENT PUBLIC
	ASSUME CS:CodeSeg,DS:DataSeg,SS:StackSeg

NewLine	PROC NEAR
	PUSH	AX
	PUSH	DX
	MOV		AH,2
	MOV		DL,10
	INT		21h
	MOV		DL,13
	INT		21h
	POP		DX
	POP		AX
	RET
NewLine	ENDP

;--------------------------------------------------


MAIN:
	MOV AX,DataSeg
	MOV DS,AX
	
	Print:	
		CALL	FuncM
	
	MenuLoop:
		MOV		AH,9
		MOV		DX,OFFSET Ent
		INT		21h

		MOV		AH,8
		INT		21h
		MOV		AH,2
		MOV		DL,AL
		INT		21h

		CALL	NewLine
		MOV		BL,AL
		SUB		BL,'0'
		
		CMP		BL,8
		JE		EndProg
		
		ADD		BL,BL
		MOV		BH,0
		
		CMP		BL,2
		JBE		SkipPush
		PUSH	X			;ïóø Õ åñëè âûçûâàåòñÿ ôóíêöèÿ ïå÷àòè ÷èñëà
	SkipPush:
		CALL	FuncM[BX]	; Вызываем функцию
		
		CMP		BL,2
		JBE		SkipPop
		ADD		SP,2		;ïîï Õ
	SkipPop:
		CMP		BL,2
		JNE		MenuLoop
		MOV		X,AX
		
	JMP		MenuLoop
	
	EndProg:
		MOV		AH,4Ch
		MOV		AL,0
		INT		21h
CodeSeg ENDS
	END MAIN
		


	
