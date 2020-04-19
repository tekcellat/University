PUBLIC M_MenuPrint

DataSeg	SEGMENT PUBLIC
	Menu	DB	10,13,'	MENU',10,13,'$'
	Menu0	DB	'0.Print menu',10,13,'$'
	Menu1	DB	'1.Input number',10,13,'$'
	Menu2	DB	'2.Num as unsigned bin',10,13,'$'
	Menu3	DB	'3.Num as signed bin',10,13,'$'
	Menu4	DB	'4.Num as unsigned dec',10,13,'$'
	Menu5	DB	'5.Num as signed dec',10,13,'$'
	Menu6	DB	'6.Num as unsigned hex',10,13,'$'
	Menu7	DB	'7.Num as signed hex',10,13,'$'
	Menu8	DB	'8.Exit',10,13,'$'
DataSeg ENDS

CodeSeg	SEGMENT PUBLIC
	ASSUME CS:CodeSeg, DS:DataSeg
	
;вывод меню на экран
M_MenuPrint	PROC NEAR
	PUSH	AX
	PUSH	DX
	
	MOV		AH,9
	MOV	DX,OFFSET Menu
	INT		21h

	MOV	DX,OFFSET Menu0
	INT		21h

	MOV	DX,OFFSET Menu1
	INT		21h

	MOV	DX,OFFSET Menu2
	INT		21h

	MOV	DX,OFFSET Menu3
	INT		21h

	MOV	DX,OFFSET Menu4
	INT		21h

	MOV	DX,OFFSET Menu5
	INT		21h

	MOV	DX,OFFSET Menu6
	INT		21h

	MOV	DX,OFFSET Menu7
	INT		21h

	MOV	DX,OFFSET Menu8
	INT		21h
	
	POP		DX
	POP		AX
	RET
M_MenuPrint ENDP

CodeSeg ENDS
END 