.386p 

descr struc     	; декскриптор сегмента
	limit 	dw 0	
	base_l 	dw 0	
	base_m 	db 0	
	attr_1	db 0	
	attr_2	db 0	
	base_h 	db 0	
descr ends

int_descr struc 	; декскриптор прерывания
	offs_l 	dw 0 	
	sel	dw 0	
	rsrv 	db 0  
	iattr	db 0  
	offs_h 	dw 0  
int_descr ends

protected_seg	SEGMENT PARA PUBLIC 'CODE' USE32											                      
	ASSUME	CS:protected_seg

  	gdt	label	byte			; глобальная таблица дескрипторов
  	gdt_null	descr <0,0,0,0,0,0>	; нулевой дескриптор	
  	gdt_ds		descr <0FFFFh,0,0,92h,11001111b,0>	; для защищенного режима, 92h = 10010010b
  	gdt_cs16	descr <real_seg_size-1,0,0,98h,0,0>	; для кода реального режима, 98h = 10011010b
  	gdt_cs32	descr <protected_seg_size-1,0,0,98h,01000000b,0> ; для защищенного режима
  	gdt_ds32	descr <protected_seg_size-1,0,0,92h,01000000b,0>
  	gdt_ss32	descr <stack_size-1,0,0, 92h, 01000000b,0>
  	gdt_size = $-gdt
	gdtr	df 0	

    	idt	label	byte			; таблица дескрипторов прерываний
    	int_descr 32 dup (<0, 24, 0, 8Eh, 0>)
    	int08h int_descr <0, 24, 0, 8Eh, 0>
    	int09h int_descr <0, 24, 0, 8Eh, 0>
    	idt_size = $-idt
    	idtr	df 0 

    	idtr_r dw	3FFh,0,0 		; регистр таблицы дескрипторов прерываний

    	master	db 0				; маски прерываний ведущего и ведомого контроллеров					 
    	slave	db 0
	s      	db ?					 

    	exit_flag	db 0				
    	time_08h	dd 0				 

	mes_protected	db 'PROTECTED MODE  '
	mes_real	db 'REAL MODE$'
	string 		db '**** ****-**** ****-**** ****'

	ASCII_table	db 0, 0, 49, 50, 51, 52, 53, 54, 55, 56, 57, 48, 45, 61, 32, 0			; ESC, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, -, =,  
			db 113, 119, 101, 114, 116, 121, 117, 105, 111, 112, 91, 93, 0, 0, 97, 115	; q, w, e, r, t, y, u, i, o, p, [, ], a, s
			db 100, 102, 103, 104, 106, 107, 108, 59, 39, 96, 0, 92, 122, 120, 99		; d, f, g, h, j, k, l, ;, ', \, z, x, c
			db 118, 98, 110, 109, 44, 46, 47, 0, 0, 0, 32					; v, b, n, m, ,, ., /, space
	pos		dd 2h 

protected_mode:			
	mov	ax, 32
	mov	ds, ax
	mov	ax, 8
	mov	es, ax
	mov	ax, 40
	mov	ss, ax
	mov	ebx, stack_size
	mov	esp, ebx

	sti 	
					
	mov 	ebp, 160 * 18 + 2 * 37		; печатаем PROTECTED MODE
	mov 	ecx, 0					
	add 	ebp, 0B8000h

print_protected:
	mov 	al, mes_protected[ecx]
	mov 	es:[ebp], al
	add 	ebp, 2
	inc 	ecx
	cmp 	ecx, 23
	jne 	print_protected

	push	ds      			; объем доступной физ. памяти     
	mov	ax, 8
	mov	ds, ax
				
	mov	ebx, 100001h		
	mov	dl, 00010111b										
	mov	ecx, 0FFEFFFFEh	

try_write:
	mov	dh, ds:[ebx]												
	mov	ds:[ebx], dl		
	cmp	ds:[ebx], dl		
	jnz	memory_end
	
	mov	ds:[ebx], dh		
	inc	ebx								
	loop	try_write

memory_end:
	pop	ds

	xor	edx, edx			; печать результата
	mov	eax, ebx				 	
	mov 	ebx, 160 * 18 + 2 * 68
	add 	ebx, 0B8000h
	mov 	ECX, 10
	
print_digit:	
	div 	ECX
	add 	DX, '0'
	mov 	s, DL
	mov 	DX, word ptr s
	mov 	ES:[EBX], Dl
	sub 	EBX, 2
	mov 	EDX, 0
	cmp 	EAX, 0
	jnz 	print_digit
				
wait_for_exit:
	test	exit_flag, 1			; ждем команду пользователя на выход
	jz	wait_for_exit

home:
	cli 
	db	0EAh 				; Дальний переход для того, чтобы заново загрузить селектор в регистр CS  
	dd	offset real_end
	dw	16

new_int08h:					; обработчик прерывания от системного таймера
	push 	eax
	push 	ebp

	mov 	ebp, 160 * 19 + 2 * 61
	add 	ebp, 0B8000h
	test 	time_08h, 01h
	jnz 	skip_1

	mov 	al, 2Ah			
	jmp	skip_2	

skip_1:
	mov 	al, 20h			
										
skip_2:	
	mov 	es:[ebp], al
	mov 	es:[ebp + 2], al
	mov 	es:[ebp + 4], al

	inc 	time_08h

	mov	al, 20h			; EoI ведущему контроллеру прерываний
	out	20h, al

	pop 	ebp
	pop 	eax

	iretd 
	
new_int09h:				; обработчик прерывания клавиатуры	
	push 	eax
	push 	ebx
	push 	ebp
	push 	edx

	in	al, 60h

	xor 	ah, ah
	xor 	ebp, ebp	
	mov 	bp, ax
	mov 	dh, 5h

	cmp 	al, 0Eh
	je	delete_key

	cmp	al, 1Ch
	jne	print_key

	mov 	exit_flag, 1
	jmp 	continue

print_key:
	cmp 	al, 80h 	
	jnbe 	continue 	

	mov 	dl, ASCII_table[ebp] 
	mov 	ebp, 0B8000h + 160 * 24
	add 	ebp, pos   
	mov 	es:[ebp], dl
	add 	pos, 2
	jmp continue

delete_key:
	mov 	dl, ASCII_table[ebp] 
	mov 	ebp, 0B8000h + 160 * 24
	sub 	pos, 2
	add 	ebp, pos   
	mov 	es:[ebp], dl	

continue:
	in	al, 61h
	or	al, 80h
	out	61h, al

	mov	al, 20h			; EoI ведущему контроллеру прерываний
	out	20h, al

	pop 	edx
	pop 	ebp
	pop 	ebx
	pop	eax

	iretd

	protected_seg_size = $-GDT
protected_seg	ENDS

stack_seg	SEGMENT  PARA STACK 'STACK'
	stack_start	db	100h dup(?)
	stack_size = $-stack_start							
stack_seg 	ENDS

real_seg	SEGMENT PARA PUBLIC 'CODE' USE16		
	ASSUME CS:real_seg, DS:protected_seg, SS:stack_seg

begin:
	mov	ax, protected_seg
	mov	ds, ax

	mov ah, 09h
	mov edx, offset mes_real
	int 21h

	mov 	ax, protected_seg
	mov 	ds, ax

	xor	eax, eax				; вычислим линейный адрес сегмента и загрузим его дескриптор в ГТД
	mov	ax, real_seg
	shl	eax, 4		
	mov	word ptr gdt_cs16.base_l, ax
	shr	eax, 16
	mov	byte ptr gdt_cs16.base_m, al

	mov	ax, protected_seg
	shl	eax, 4
	push 	eax	
	
	mov	word ptr GDT_cs32.base_l, ax		
	mov	word ptr GDT_ss32.base_l, ax
	mov	word ptr GDT_ds32.base_l, ax
	shr	eax, 16
	mov	byte ptr GDT_cs32.base_m, al
	mov	byte ptr GDT_ss32.base_m, al
	mov	byte ptr GDT_ds32.base_m, al

	pop 	eax
	push 	eax

	add	eax, offset GDT 						
	mov	dword ptr gdtr + 2, eax		; полный линейный адрес в младшие 4 байта gdtr			
	mov 	word ptr gdtr, gdt_size - 1	; размер gdt в старшие 2 байта
	lgdt	fword ptr gdtr			; загрузка gdt

	pop	eax
	add	eax, offset IDT
	mov	dword ptr idtr + 2, eax
	mov 	word ptr idtr, idt_size - 1

	mov	eax, offset new_int08h		
	mov	int08h.offs_l, ax
	shr	eax, 16
	mov	int08h.offs_h, ax

	mov	eax, offset new_int09h 
	mov	int09h.offs_l, ax
	shr	eax, 16
	mov	int09h.offs_h, ax

	in	al, 21h			; сохранение масок прерываний контроллеров						
	mov	master, al					
	in	al, 0A1h						
	mov	slave, al

	mov	al, 11h	 		; перепрограммирование ведущего контроллера				
	out	20h, al							
	mov	al, 20h							
	out	21h, al						
	mov	al, 4																			
	out	21h, al
	mov	al, 1							  
	out	21h, al

	mov	al, 0FCh		; запрет прерываний ведущего контр., кроме таймера и клав.
	out	21h, al

	mov	al, 0FFh		; запрет всех в ведомом
	out	0A1h, al

	lidt	fword ptr idtr		; загрузка idtr
						
	mov	al, 0D1h		; открыть линию А20
	out	64, al
	mov	al, 0DFh
	out	60h, al

	cli

	in	al, 70h			; запрет немаскируемых прерываний
	or	al, 80h
	out	70h, al

	mov	eax, cr0		
	or	al, 1
	mov	cr0, eax

	db	66h			; дальний переход
	db	0EAh
	dd	offset protected_mode
	dw	24

real_end:
	mov	eax, cr0		; сброс флага
	and	al, 0FEh 				
	mov	cr0, eax
		
	db	0EAh			; Дальний переход для того, чтобы заново загрузить селектор в регистр CS				
	dw	offset return							
	dw	real_seg

return:
	mov	ax, protected_seg					
	mov	ds, ax
	mov	es, ax
	mov	ax, stack_seg
	mov	ss, ax
	mov	bx, stack_size
	mov	sp, bx

	mov	al, 11h			; перепрограммируем ведущий контроллер				
	out	20h, al
	mov	al, 8						
	out	21h, al
	mov	al, 4						
	out	21h, al
	mov	al, 1
	out	21h, al

	mov	al, master		; восстановление масок контроллеров прерываний
	out	21h, al
	mov	al, slave
	out	0A1h, al

	lidt	fword ptr idtr_r	; восстанавливаем idt

	sti
	mov AL, 0
	out 70h, AL

	mov ah, 09h
	mov edx, offset mes_real
	int 21h

	mov	ah, 4Ch
	int	21h

real_seg_size = $-begin 
real_seg	ENDS
END begin