PUBLIC	M_s_bin

EXTRN M_u_bin:NEAR

CodeSeg	SEGMENT	PUBLIC
	ASSUME	CS:CodeSeg
	
M_s_bin	PROC	NEAR

	begin:
		PUSH	BP	
		MOV		BP,SP

	get_param:
		MOV		AX,[BP+4]
		CMP		AX, 0
		JGE		Call_print2

	make_neg:
    		PUSH		AX
    		MOV		AH, 2h
		MOV		DL, '-'
    		INT		21h
    		POP		AX
		NEG 		AX

	Call_print2:
		PUSH		AX
		CALL 		M_u_bin       
    	Exit:
        	POP		BP
        	RET		2

M_s_bin ENDP
CodeSeg	ENDS
END