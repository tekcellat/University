PUBLIC	M_s_hex

EXTRN M_u_hex:NEAR

CodeSeg	SEGMENT	PUBLIC
	ASSUME	CS:CodeSeg
	
M_s_hex	PROC	NEAR

	begin:
		PUSH		BP	
		MOV		BP,SP


	get_param:
		MOV		AX,[BP+4]
		CMP		AX, 0
		JGE		Call_print16

	make_neg:
    		PUSH 		AX
    		MOV		AH, 2h
		MOV		DL, '-'
    		INT		21h
    		POP		AX
		NEG 		AX

	Call_print16:
		PUSH		AX
		CALL 		M_u_hex

        
    	Exit:
        	POP		BP
        	RET		2

M_s_hex ENDP
CodeSeg	ENDS
END