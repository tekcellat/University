.386p 

descr struc     
	lim 	dw 0	
	base_l 	dw 0	
	base_m 	db 0	
	attr_1	db 0	
	attr_2	db 0	
	base_h 	db 0	
descr ends

int_descr struc 
	offs_l 	dw 0 	
	sel		dw 0	
	counter db 0  
	attr	db 0  
	offs_h 	dw 0  
int_descr ends

PM_seg	SEGMENT PARA PUBLIC 'CODE' USE32		
	                ASSUME	CS:PM_seg
  	GDT		label	byte
  	
  	gdt_null	descr <>
  	gdt_flatDS	descr <0FFFFh,0,0,92h,11001111b,0>	
  	gdt_16bitCS	descr <RM_seg_size-1,0,0,98h,0,0>	
  	gdt_32bitCS	descr <PM_seg_size-1,0,0,98h,01000000b,0>
  	gdt_32bitDS	descr <PM_seg_size-1,0,0,92h,01000000b,0>
  	gdt_32bitSS	descr <stack_l-1,0,0, 92h, 01000000b,0>
  	gdt_size = $-GDT 
  	gdtr	df 0	

    SEL_flatDS     equ   8
    SEL_16bitCS    equ   16
    SEL_32bitCS    equ   24
    SEL_32bitDS    equ   32
    SEL_32bitSS    equ   40

    
    IDT	label	byte

    int_descr 32 dup (<dummy>)
    int08 int_descr <0, SEL_32bitCS,0, 8Eh, 0>  
    int09 int_descr	<0, SEL_32bitCS,0, 8Eh, 0>
    idt_size = $-IDT
	
    idtr		df 0 
    idtr_real	dw	3FFh,0,0 

    master		db 0					 
    slave		db 0					 

    escape		db 0				 
    time_08		dd 0				 

		msg1 db 'In Real Mode now. To move to Protected Mode press any key...$'
		msg2 db 'In Real Mode again!$'
		
		ASCII_table	db 0, 0, 49, 50, 51, 52, 53, 54, 55, 56, 57, 48, 45, 61, 0, 0
					db 81, 87, 69, 82, 84, 89, 85, 73, 79, 80, 91, 93, 0, 0, 65, 83
					db 68, 70, 71, 72, 74, 75, 76, 59, 39, 96, 0, 92, 90, 88, 67
					db 86, 66, 78, 77, 44, 46, 47
		out_position	dd 1E0h 

print_str macro str
		mov ah,9
		mov dx, str
		int 21h
endm
		
create_number macro
		local number1
			cmp dl,10
			jl number1
			add dl,'A' - '0' - 10
		number1:
			add dl,'0'
endm
		
my_print_eax macro
		local prcyc1 				
			push ecx 					
			push dx

			mov ecx,8					
			add ebp,0B8010h 	
												
												
		prcyc1:
			mov dl,al					
			and dl,0Fh				
			create_number 0		
			mov es:[ebp],dl		
			ror eax,4					
												
			sub ebp,2					
			loop prcyc1				

			sub ebp,0B8010h		
			pop dx
			pop ecx
endm
	
PM_entry:
		mov	ax,SEL_32bitDS
		mov	ds,ax
		mov	ax,SEL_flatDS
		mov	es,ax
		mov	ax,SEL_32bitSS
		mov	ebx,stack_l
		mov	ss,ax
		mov	esp,ebx

		sti 
		
		call	compute_memory
		
work:
		test	escape, 1
		jz	work

goback:
		cli 
		
		mov gdt_32bitDS.lim, 0FFFFh
		mov gdt_32bitCS.lim, 0FFFFh
		mov gdt_32bitSS.lim, 0FFFFh
		
		push DS
		pop DS
		push SS
		pop SS
		push ES
		pop ES
		
		db	0EAh 
		dd	offset RM_return
		dw	SEL_16bitCS
	
new_int08:
		push eax
		push ebp
		push ecx
		push dx
		mov  eax,time_08
		
		push ebp
		mov ebp, 0					
		my_print_eax 0			
		pop ebp							

		inc eax
		mov time_08,eax
		
		pop dx
		pop ecx
		pop ebp

		
		mov	al,20h
		out	20h,al
		pop eax

		iretd 

		
new_int09:
		push eax
		push ebx
		push ebp
		push edx

		in	al,60h 		 

		cmp	al,1Ch 	     
		jne	not_leave 	 
		mov escape,1     
		jmp leav
not_leave:
		cmp al,80h 	 
		ja leav 	 
		xor ah,ah	 
		mov bp,ax
		mov dl,ASCII_table[ebp] 
		mov ebp,0B8000h
		mov ebx,out_position   
		mov es:[ebp+ebx],dl

		add ebx,2			   
		mov out_position,ebx

leav:
		in	al,61h
		or	al,80h
		out	61h,al

		mov	al,20h
		out	20h,al

		pop edx
		pop ebp
		pop ebx
		pop	eax

		iretd
			

compute_memory	proc
		push	ds            
		mov	ax, SEL_flatDS	
		mov	ds, ax					
		mov	ebx, 100001h		
		mov	dl,	10101010b	  

		mov	ecx, 0FFEFFFFEh			
check:
		mov	dh, ds:[ebx]		
		mov	ds:[ebx], dl		
		cmp	ds:[ebx], dl		
		jnz	end_of_memory		
		mov	ds:[ebx], dh		
		inc	ebx							
		loop	check
		
end_of_memory:
		pop	ds							
		xor	edx, edx
		mov	eax, ebx				
		mov	ebx, 100000h		
		div	ebx

		push ebp
		mov ebp,20					
		my_print_eax 0			
		pop ebp							

		ret
	compute_memory	endp

dummy proc
	jmp work
dummy endp

	PM_seg_size = $-GDT
PM_seg	ENDS

stack_seg	SEGMENT  PARA STACK 'STACK'
	stack_start	db	100h dup(?)
	stack_l = $-stack_start							
stack_seg 	ENDS

RM_seg	SEGMENT PARA PUBLIC 'CODE' USE16		
	ASSUME CS:RM_seg, DS:PM_seg, SS:stack_seg

start:
		mov   ax,PM_seg
		mov   ds,ax

		mov ah, 09h
		mov edx, offset msg1
		int 21h

		push eax
		mov ah,10h
		int 16h
		pop eax
		
		mov	ax,3
		int	10h
		
		push PM_seg
		pop ds
		
		xor	eax,eax
		mov	ax,RM_seg
		shl	eax,4		
		mov	word ptr gdt_16bitCS.base_l,ax
		shr	eax,16
		mov	byte ptr gdt_16bitCS.base_m,al
		mov	ax,PM_seg
		shl	eax,4
		push eax		
		push eax		
		mov	word ptr GDT_32bitCS.base_l,ax
		mov	word ptr GDT_32bitSS.base_l,ax
		mov	word ptr GDT_32bitDS.base_l,ax
		shr	eax,16
		mov	byte ptr GDT_32bitCS.base_m,al
		mov	byte ptr GDT_32bitSS.base_m,al
		mov	byte ptr GDT_32bitDS.base_m,al

		pop eax
		add	eax,offset GDT 						
		
		mov	dword ptr gdtr+2,eax			
		mov word ptr gdtr, gdt_size-1	
		
		lgdt	fword ptr gdtr

		pop	eax
		add	eax,offset IDT
		mov	dword ptr idtr+2,eax
		mov word ptr idtr, idt_size-1

		mov	eax, offset new_int08 
		mov	int08.offs_l, ax
		shr	eax, 16
		mov	int08.offs_h, ax
		mov	eax, offset new_int09 
		mov	int09.offs_l, ax
		shr	eax, 16
		mov	int09.offs_h, ax

		
		in	al, 21h							
		mov	master, al					
		in	al, 0A1h						
		mov	slave, al

		mov	al, 11h							
		out	20h, al							
		mov	AL, 20h							
		out	21h, al							
		mov	al, 4								
														
		out	21h, al
		mov	al, 1							  
		out	21h, al
		
		mov	al, 0FCh
		out	21h, al
		
		mov	al, 0FFh
		out	0A1h, al

		lidt	fword ptr idtr
		
		in	al,92h						
		or	al,2							
		out	92h,al						
		
		cli
		
		in	al,70h
		or	al,80h
		out	70h,al

		mov	eax,cr0
		or	al,1
		mov	cr0,eax

		db	66h
		db	0EAh
		dd	offset PM_entry
		dw	SEL_32bitCS

RM_return:
		
		mov	eax,cr0
		and	al,0FEh 				
		mov	cr0,eax

		db	0EAh						
		dw	$+4							
		dw	RM_seg
		
		mov	ax,PM_seg				
		mov	ds,ax
		mov	es,ax
		mov	ax,stack_seg
		mov	bx,stack_l
		mov	ss,ax
		mov	sp,bx
	
		mov	al, 11h					
		out	20h, al
		mov	al, 8						
		out	21h, al
		mov	al, 4						
		out	21h, al
		mov	al, 1
		out	21h, al
		
		mov	al, master
		out	21h, al
		mov	al, slave
		out	0A1h, al

		lidt	fword ptr idtr_real

		in	al,70h
		and	al,07FH
		out	70h,al

		sti
		
		mov	ax,3
		int	10h
		
		mov ah, 09h
		mov edx, offset msg2
		int 21h
		
		mov	ah,4Ch
		int	21h

RM_seg_size = $-start 	
RM_seg	ENDS
END start


