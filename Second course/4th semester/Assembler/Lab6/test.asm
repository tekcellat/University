data SEGMENT

p_n DB cr, lf, 'Enter n: ',0

p_res DB cr, lf, 'The factorial is: ',0

tmpstr DW 40 DUP (?)

data ENDS







code SEGMENT

	ASSUME cs:code, ds:data

start:	mov ax, data

	mov ds, ax

		;input n1

	output p_n 

	inputs tmpstr, 10

	atoi tmpstr

		;initialize

	mov bx, ax

	mov ax, 01h

		;factorial iterations

n_ip:	imul bx

	dec bx

	jnz n_ip

		;output factorial

	output p_res

	itoa tmpstr, ax

	output tmpstr



quit:	mov al, 00h

	mov ah, 4ch

	int 21h

code ENDS

END start