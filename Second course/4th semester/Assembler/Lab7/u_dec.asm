PUBLIC	M_u_dec

CodeSeg	SEGMENT	PUBLIC
	ASSUME	CS:CodeSeg
	
M_u_dec	PROC	NEAR

	Begin:        
        	PUSH		BP		
		MOV		BP,SP
		PUSH		BX
		MOV		AX,[BP+4]
		MOV		BX,10
		PUSH		AX
	
	Loop1:
		MOV		DX,0
		DIV		BX
		MOV		CX, AX
		MOV		AH,2	
		MOV		DL,'a'
		INT		21h
		MOV		AX, CX		
		CMP		AX,0
		JNE		Loop1
		MOV		AH,2
		MOV 		DL,8	
		INT 		21h
		POP		AX

	Loop2:
		MOV		DX,0
		DIV		BX
		MOV		CX,AX	
		MOV		AH,2
		ADD		DL,'0'
		INT		21h
		MOV		DL,8
		INT		21h
		INT		21h
		MOV		AX, CX
		CMP		AX,0
		JNE		Loop2

    Exit:   
		POP		BX
		POP		BP
		RET		2

M_u_dec ENDP
CodeSeg	ENDS
END