PUBLIC	M_u_bin

CodeSeg	SEGMENT	PUBLIC
	ASSUME	CS:CodeSeg

EXTRN NewLine:NEAR

;-------------------

M_u_bin	PROC	NEAR

	begin:
		PUSH		BP
		MOV		BP,SP
		PUSH		SI

	get_param:
		MOV		AX, [BP+4]
		CMP		AL, 0
		JE      	Print_Zero
		MOV		SI, 16

	Loop1:
		MOV		DL, 0
		SHL		AX, 1
		JNC		Loop1_next
		JMP		M0
	
	Loop1_next:
		DEC 		SI
		JNZ 		Loop1

	Loop2:
		MOV 		DL, 0
		SHL		AX, 1
		JNC		Loop2_print
    	M0:
		INC 		DL

    	Loop2_print:
    		ADD		DL, '0'
    		MOV 		CX, AX 
    		MOV		AH, 2
    		INT		21h
    		MOV		AX, CX
    		DEC		SI
    		JNZ		Loop2
    		JMP		Exit

     Print_Zero:
    		MOV		DL, '0'
		MOV		AH, 2
    		INT		21h

     Exit:
     		CALL NewLine
        	POP     	SI
        	POP		BP
        	RET		2

M_u_bin ENDP
CodeSeg	ENDS
END
