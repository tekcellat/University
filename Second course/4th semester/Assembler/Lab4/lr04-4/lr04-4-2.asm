EXTRN X: byte
PUBLIC exit

SD2 SEGMENT para 'DATA'
	Y db 'Y'
SD2 ENDS

SC2 SEGMENT para public 'CODE'
	assume CS:SC2, DS:SD2
exit:
	mov bx, ds
	mov ax, SD2
	mov ds, ax
	
	mov ah, Y
	mov ds, bx
	mov al, X
	xchg ah, al
	mov X, al
	mov bx, SD2
	mov ds, bx
	mov Y, ah

	mov dl, Y
	mov ah, 2
	int 21h
	
	mov ax, 4c00h
	int 21h
SC2 ENDS
END


