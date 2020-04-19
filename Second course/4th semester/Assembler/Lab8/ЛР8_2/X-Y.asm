;—оставить подпрограмму с именем A_B типа
;   Procedure (var A: LONGWORD; const B:LONGWORD; L:LONGWORD)
;выполн€ющую вычитание битовых строк A:=A \ B длины L.

.386
.model FLAT,PASCAL
PUBLIC A_B

.CODE
A_B PROC
  PUSH EBP
  MOV EBP,ESP
  
A EQU DWORD PTR[EBP+16]
B EQU DWORD PTR[EBP+12]
LXY EQU DWORD PTR[EBP+8]
  
  MOV EDX, B
  MOV EBX, [EDX]
  MOV EDX, A
  MOV EAX, [EDX]
  MOV ECX, LXY  ;
  
  NOT EBX
  AND EAX, EBX
  MOV [EDX], EAX
  
  POP EBP

  RET 12
A_B ENDP
END