PUBLIC	M_s_dec

EXTRN M_u_dec:NEAR

CodeSeg	SEGMENT	PUBLIC
	ASSUME	CS:CodeSeg
	
M_s_dec	PROC	NEAR

	begin:
		PUSH		BP	
		MOV		BP,SP		

	get_param:
		MOV		AX,[BP+4]
		CMP		AX, 0
		JGE		Call_print10

	make_neg:
    		PUSH 		AX
    		MOV		AH, 2h
		MOV		DL, '-'
    		INT		21h
    		POP		AX
		NEG 		AX

	Call_print10:
		PUSH		AX
		CALL 		M_u_dec

      Exit:
        	POP		BP
        	RET		2

M_s_dec ENDP
CodeSeg	ENDS
END