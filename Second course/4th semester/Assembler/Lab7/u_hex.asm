PUBLIC	M_u_hex

Data    SEGMENT PUBLIC
    List    DB  "qwertyuiopasdfghj"
Data    ENDS

CodeSeg	SEGMENT	PUBLIC
	ASSUME	CS:CodeSeg
	
M_u_hex	PROC	NEAR

	Begin:        
        	PUSH		BP	
		MOV		BP,SP
		PUSH		BX

		MOV		CX, 4
		MOV		BX,[BP+4]
		MOV 		AX, 0 
	Loop1:
		MOV 		AL, BH
		SHR		AL, CL
		CMP		AL, 0
		JE 		Zero
		MOV		DI, BX
		LEA		BX, List
		XLAT
		MOV		BX, DI
		MOV		DL, AL
		MOV		AH,2
		INT		21h
	
	Zero:
		SHL		BX, CL
		CMP		BX, 0 
		JNE		Loop1

   	Exit:  
		POP		BX
		POP		BP
		RET		2

M_u_hex ENDP
CodeSeg	ENDS
END