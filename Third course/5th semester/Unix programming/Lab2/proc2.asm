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

pdescr dq 0
sym db 1
attr1 db 4Fh
attr2 db 2Fh
s      db ?
mes_protected_mode		db ' in protected mode '
mes_real_mode			db ' in real mode '
mes_real_mode_back			db ' back to real mode '
data_size=$-gdt_null
data ends

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
	rol eax, 16
	mov [bx].base_m, al
	
	xor eax, eax
	mov ax, cs
	shl eax, 4
	mov bx, offset gdt_code
	mov [bx].base_l, ax
	rol eax, 16
	mov [bx].base_m, al
	
	xor eax, eax
	mov ax, ss
	shl eax, 4
	mov bx, offset gdt_stack
	mov [bx].base_l, ax
	rol eax, 16
	mov [bx].base_m, al
	
	mov dword ptr pdescr+2, ebp
	mov word ptr pdescr, gdt_size-1
	lgdt pdescr
	
	
	mov AX, 0B800h
	mov ES, AX
	mov si, offset mes_real_mode
	mov di, 160 * 5 + 2 * 30
	mov cx, 20
	cld
	mov ah, attr2

screen1:
	lodsb
	stosw
	loop screen1
	
	mov al, 0D1h
	out 64h, al
	mov al, 0dfh
	out 60h, al
	
	cli
	mov al, 80h
	out 70h, al
	
	mov eax, cr0
	or eax, 1
	
	mov cr0, eax
	db 0EAh
	dw offset continue
	dw 16
	
continue:
	mov ax, 8
	mov ds, ax
	
	mov ax, 24
	mov ss, ax
	
	mov ax, 32
	mov es, ax
	mov si, offset mes_protected_mode
	mov di, 160 * 6 + 2 * 30
	mov cx, 20
	cld
	mov ah, attr1

screen2:
	lodsb
	stosw
	loop screen2
	
mem:
	mov	ebx, 100001h
	mov EAX, 10101010b	  
	mov ECX, 0FFEFFFFEh
	mov EDI, 1

check_mem:
	mov ECX, GS:[EBX]
	mov GS:[EBX], EAX ; запись сигнатуры
	mov EDX, GS:[EBX]
	cmp EDX, EAX ; сравнение сигнатуры
	jne end_mem
	mov GS:[EBX], ECX
	inc EBX
	inc EDI
	jmp check_mem
			
	
end_mem:
	xor EDX, EDX
	mov EAX, EDI
	mov BX, 370
	mov ECX, 10
	
divide:	
	div ECX
	add DX, '0'
	mov s, DL
	mov DX, word ptr s
	mov ES:[BX], DX
	sub BX, 2
	mov EDX, 0
	cmp EAX, 0
	jnz divide
	
	mov al, 0d1h
	out 64h, al
	mov al, 0ddh
	out 60h, al	

	mov gdt_data.limit, 0FFFFh
	mov gdt_code.limit, 0FFFFh
	mov gdt_stack.limit,0FFFFh
	mov gdt_screen.limit,0FFFFh
	
	mov ax, 8
	mov ds, ax
	mov ax, 24
	mov ss, ax
	mov ax, 32
	mov es, ax
	
	db 0EAh
	dw offset go
	dw 16

	
go:
	mov eax, CR0
	and eax, 0FFFFFFFEh
	mov CR0, eax
	db 0EAh
	dw offset return
	dw text
return:
	mov AX, data
	mov DS, AX
	mov AX, stk
	mov SS, AX
	
	sti
	mov AL, 0
	out 70h, AL
	
	mov AX, 0B800h
	mov ES, AX
	mov si, offset mes_real_mode_back
	mov di, 160 * 7 + 2 * 30
	mov cx, 20
	cld
	mov ah, attr2

screen3:
	lodsb
	stosw
	loop screen3
	mov AX, 4C00h
	int 21h


	
main endp
code_size=$-main
text ends
stk segment stack 'stack'
	db 256 dup('^')
stk ends
	end main