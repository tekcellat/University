;—оставить подпрограмму с именем X_U_Y типа
;   Procedure (var X: LONGWORD; const Y:LONGWORD; L:LONGWORD)
;выполн€ющую объединение битовых строк X:=X U Y длины L.

.386
.model FLAT,PASCAL
PUBLIC X_U_Y

.CODE
X_U_Y PROC
X EQU DWORD PTR[EBP+16]           ;перва€ строка
Y EQU DWORD PTR[EBP+12]           ;втора€ строка
L EQU DWORD PTR[EBP+8]            ;длина строк

  PUSH EBP                        ;пишем старый адрес EBP
  MOV EBP,ESP                     ;пишем в EBP текущее значение ESP

  PUSH ESI                        ;сохран€ем регистры
  PUSH EDI

  MOV ECX,L                       ;CX = L
  SHR ECX,5                       ;сдвигаем на 5 разр€дов вправо (делим нацело на 32)
;если ECX больше или равен 32, то он станет 1, иначе 0
  INC ECX                         ;»нкрементируем ECX, чтобы цикл снизу выполнилс€ 2 раза
  MOV EDI,X
  MOV ESI,Y

M1:
  MOV EAX,[ESI]
  OR [EDI],EAX                    ;объедин€ем
  ADD EDI,4                       ;сдвигаем указатели строк на 4
  ADD ESI,4
  LOOP M1                         

  POP EDI
  POP ESI
  POP EBP
  RET 12
X_U_Y ENDP
END