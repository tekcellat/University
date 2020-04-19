.386P

descr struc
limit dw 0
base_l dw 0
base_m db 0
attr_1 db 0
attr_2 db 0
base_h db 0
descr ends

data segment use16

gdt_null descr <0,0,0,0,0,0>

gdt_data descr <data_size-1,0,0,92h, 0, 0>

gdt_code descr <code_size-1,0,0,98h,0,0>

gdt_stack descr <255,0,0,92h, 0,0>
gdt_screen descr <4095,8000h,0Bh,92h,0,0>

gdt_size=$-gdt_null

pdescr	dq 0
sym 	db 1
attr 	db 1Eh
msg		db 27,'[31;42m    back to real mode ',27, '[0m$'
data_size=$-gdt_null
data 	ends

text segment 'code' use16
	assume CS:text, DS:data
main proc
	xor eax, eax
	mov AX, data
	mov DS, AX
	
	shl eax, 4
	mov ebp, eax
	mov bx, offset gdt_data
	mov [bx].base_l, ax
	shr eax, 16
	mov [bx].base_m, al
	
	xor eax, eax
	mov ax, cs
	shl eax, 4
	mov bx, offset gdt_code
	mov [bx].base_l, ax
	shr eax, 16
	mov [bx].base_m, al
	
	xor eax, eax
	mov ax, ss
	shl eax, 4
	mov bx, offset gdt_stack
	mov [bx].base_l, ax
	shr eax, 16
	mov [bx].base_m, al
	
	mov dword ptr pdescr+2, ebp
	mov word ptr pdescr, gdt_size-1
	lgdt pdescr
	
	mov ax,40h
	mov es,ax
	mov word ptr es:[69h],cs
	mov al,0fh
	out 70h,al
	mov al,0fh
	out 71h,al
	cli
	
	mov eax, CR0
	or eax,1
	mov CR0, eax
	; Теперь процессор работает в защищенном режиме
	db 0eah
	dw offset continue
	dw 16
	
continue:
	mov ax, 8
	mov ds, ax
	
	mov ax, 24
	mov ss, ax
	
	mov ax, 32
	mov es, ax
	mov DI, 1920
	mov cx, 80
	mov ax, word ptr sym

screen:
	stosw
	inc al
	loop screen
	
	mov al, 0feh
	out 64,al
	hlt

return:
	mov AX, data
	mov DS, AX
	mov AX, stk
	mov SS, AX
	mov sp, 256
	
	sti
	
	mov AH, 09h
	mov DX, offset msg
	int 21h
	mov AX, 4C00h
	int 21h
main endp
code_size=$-main
text ends
stk segment stack 'stack'
	db 256 dup('^')
stk ends
	end main