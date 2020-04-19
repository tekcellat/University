.386
.model FLAT ,C
PUBLIC p1
.CODE
p1:
	push EBP
	MOV EBP,ESP
	MOV EAX,[EBP + 8];N
	MOV EBX,[EBP + 12];NF

	MOV ECX,[EBP + 8]
	CMP ECX,1
	JE M1
	DEC ECX
	PUSH EBX,NF
	
	PUSH ECX
	CALL p1
	ADD ESP,8
	MOV ECX ,[EBP + 8]
	MUL ECX
	JMP M2
	
	M1:MOV EAX,1
	M2:POP ESP
 



	ret
end