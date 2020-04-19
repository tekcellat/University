.386P ; Разрешение трансляции всех команд Pentium

; Структура для описания декскриптора сегмента в таблице глобальных дескрипторов GDT
descr struc     
	lim 	dw 0	; Граница (биты 0..15) 
	base_l 	dw 0	; База, биты 0..15
	base_m 	db 0	; База, биты 1..23
	attr_1	db 0	; Байт атрибутов
	attr_2	db 0	; Граница (биты 16..19) и атрибуты 2
	base_h 	db 0	; База, биты 24..31
descr ends

; структура для описания декскриптора прерывания
int_descr struc 
	offs_l dw 0 ; Младшие 16 бит смещения
	sel dw 0 ; Селектор сегмента с кодом обработчика прерывания
	counter db 0 ; Счётчик, не используется в программе
	attr db 0 ; Атрибуты
	offs_h dw 0 ; Старшие 16 бит смещения
int_descr ends

; Сегмент данных
data segment use16

;Таблица глобальных дескрипторов GDT
gdt_null	descr <0,0,0,0,0,0> ; нулевой дескриптор
gdt_data	descr <data_size - 1,0,0,92h,0,0> ; селектор 8, сегмент данных
gdt_code	descr <code_size - 1,0,0,98h,0,0> ; селектор 16, сегмент кода
gdt_stack	descr <255,0,0,92h,0,0> ; селектор 24, сегмент стека
gdt_screen	descr <3999,8000h,0Bh,92h,0,0> ; Селектор 32, видеопамять
gdt_count	descr <0FFFFh,0,0,92h,11001111b,0> ; Селектор 40, сегмент данных с базой 0
gdt_size= $-gdt_null ; размер GDT

pdescr df 0 ; псевдодескриптор для команды lgdt


; Таблица дескрипторов прерываний IDT
IDT label byte

; первые 32 элемента таблицы (в программе не используются)
int_descr 32 dup (<catch, 16,0, 8Eh, 0>)

; дескриптор прерывания от таймера
int08 int_descr <0, 16, 0, 8Eh, 0>

; дескриптор прерывания от клавиатуры
int09 int_descr	<0, 16, 0, 8Eh, 0>

idt_size = $-IDT

idtr df 0 ; псевдодескриптор для команды lidt

idtr_real dw 3FFh, 0, 0 ; содержимое регистра IDTR в реальном режиме

master db 0	 ; маска прерываний ведущего контроллера
slave db 0   ; маска прерываний ведомого контроллера

timer dd 0h  ; счетчик тиков
escape db 0  ; флаг перехода в реальный режим

		ASCII_table	db 0, 0, 49, 50, 51, 52, 53, 54, 55, 56, 57, 48, 45, 61, 0, 0
				    db 81, 87, 69, 82, 84, 89, 85, 73, 79, 80, 91, 93, 0, 0, 65, 83
					db 68, 70, 71, 72, 74, 75, 76, 59, 39, 96, 0, 92, 90, 88, 67
					db 86, 66, 78, 77, 44, 46, 47
		print_pos dd 100 ; Позиция печати вводимого текста


data_size= $-gdt_null ; размер сегмента данных

data ends

text segment use16	
	assume CS:text, DS:data

main proc
	mov	AX, 3
	int	10h

	xor	EAX, EAX
	mov	AX, data ; загрузим в DS сегментный адрес сегмента данных
	mov DS, AX

	; Вычислим 32-битовый линейный адрес сегмента данных и загрузим его в дескриптор данных в GDT
	shl	EAX, 4
	mov	EBP, EAX ; EAX = линейный базовый адрес
	mov	BX, offset gdt_data	; BX = смещение дескриптора
	mov	[BX].base_l, AX	; загрузим младшую часть базы
	shr	EAX, 16	; старшую половину EAX в AX
	mov	[BX].base_m, AL	; загрузим среднюю часть базы

	; Вычислим и загрузим в GDT линейный адрес сегмента кода
	xor	EAX, EAX
	mov	AX, CS
	shl	EAX, 4
	mov	BX, offset gdt_code
	mov	[BX].base_l, AX
	shr	EAX, 16
	mov	[BX].base_m, AL

	; Вычислим и загрузим в GDT линейный адрес сегмента стека
	xor	EAX, EAX
	mov	AX, SS
	shl	EAX, 4
	mov	BX, offset gdt_stack
	mov	[BX].base_l, AX
	shr	EAX, 16
	mov	[BX].base_m, AL

	; Подготовим псевдодескриптор pdescr и загрузим регистр GDTR
	mov	dword ptr pdescr+2, EBP
	mov	word ptr pdescr, gdt_size-1
	lgdt pdescr

	; Подготовим псевдодескриптор для команды lidt
	xor	EAX,EAX
	mov	AX, data
	shl	EAX,4
	add	EAX, offset IDT
	mov	dword ptr idtr + 2, EAX
	mov word ptr idtr, idt_size-1

	; Заполним смещение в дескрипторах прерываний
	mov	EAX, offset int08h ; прерывание системного таймера
	mov	int08.offs_l, AX
	shr	EAX, 16
	mov	int08.offs_h, AX
	mov	EAX, offset int09h ; прерывание клавиатуры
	mov	int09.offs_l, AX
	shr	EAX, 16
	mov	int09.offs_h, AX

	; сохраним маски прерываний ведущего и ведомого контроллеров
	in	AL, 21h ; ведущий
	mov	master, AL
	in	AL, 0A1h ; ведомый
	mov	slave, AL

	; перепрограммируем контроллеры
	mov	AL, 11h	; команда "инициализировать ведущий контроллер" / СКИ1
	out	20h, AL ; 20h - "порт включения\выключения"
	mov	AL, 20h
	out	21h, AL	; базовый вектор - 20h (прерывания обрабатываются, начиная с 32) / СКИ2

	mov	AL, 4 ; Ведомый контроллер подключен к IRQ2 / СКИ3
	out	21h, AL
	mov	AL, 1 ; необходимо посылать команду EOI завершения обработчика прерывания  / СКИ4
	out	21h, AL

	; Запретим все прерывания в ведущем контроллере, кроме IRQ0 и IRQ1
	mov	AL, 0FCh
	out	21h, AL

	;запретим все прерывания в ведомом контроллере
	mov	AL, 0FFh
	out	0A1h, AL
	
	cli

	; загрузим IDT
	lidt fword ptr idtr

	; Откроем линию А20 для обращения к расширенной памяти
	mov AL, 0D1h
	out 64h, AL
	mov AL, 0DFh
	out 60h, AL

	; Переводим в защищенный режим
	mov EAX, CR0 ; получим содержимое регистра CR0
	or AL, 1 ; установим бит защищенного режима
	mov	CR0, EAX ; запишем назад в CR0

	; Процессор работает в защищенном режиме
	db 0EAh	; код команды far jmp
	dw offset continue ; смещение
	dw 16 ; селектор сегмента кода

continue:
	; Делаем адреуемые данные
	mov	AX, 8
	mov DS, AX
	; Делаем адресуемый стек
	mov AX, 24
	mov SS, AX

	; Инициализируем ES
	mov AX, 32
	mov	ES, AX

	call memory_cnt
	sti

work:
	test escape, 1
	jz	work

	; Закроем линию А20
	mov AL, 0D1h
	out 64h, AL
	mov AL, 0DDh
	out 60h, AL

	; Возврат в реальный режим
	cli
	
	mov	gdt_data.lim, 0FFFFh ; граница сегмента данных
	mov	gdt_code.lim, 0FFFFh			
	mov	gdt_stack.lim, 0FFFFh			
	mov	gdt_screen.lim, 0FFFFh			

	push DS	; загрузим теневой регистр сегмента данных
	pop	DS

	push SS	; загрузим теневой регистр сегмента стека
	pop	SS

	push ES	; загрузим теневой регистр дополнительного сегмента данных
	pop	ES	

	; Выполним дальний переход для того, чтобы заново загрузить селектор в регистр CS и модифицировать 
	; его теневой регистр
	db 0EAh					
	dw offset go				
	dw 16

go:
	mov	EAX, CR0 ; получим содержимое CR0
	and	EAX, 0FFFFFFFEh	; сбросим бит защищенного режима
	mov CR0, EAX ; запишем обратно в CR0

	db 0EAh ; код команды far jmp
	dw offset return ; смещение
	dw text ; сегмент

; Процессор снова работает в реальном режиме
return:
	mov	AX, data ; сделать адресуемыми данные
	mov	DS, AX
	mov	AX, stk	; сделать адресуемыми стэк
	mov	SS, AX

	; перепрограммируем контроллеры
	mov	AL, 11h ; инициализация
	out	20h, AL
	mov	AL, 8 ; отправка смещения
	out	21h, AL
	mov	AL, 4
	out	21h, AL
	mov	AL, 1
	out	21h, AL

	; восстанавливаем сохраненные ранее маски контроллеров
	mov	AL, master
	out	21h, AL
	mov	AL, slave
	out	0A1h, AL

	; загружаем таблицу дескрипторов прерываний реального режима
	lidt fword ptr idtr_real

	; разрешаем обратно немаскируемые прерывания
	in	AL,70h
	and	AL,07FH
	out	70h,AL

	sti						

	mov	AH, 4Ch
	int	21h
main endp

catch proc
	db 66h
	iretd
catch endp

int08h proc
	push EAX
	push EDI

	mov EDI, 30
	xor EAX, EAX
	mov EAX, timer

	call print_number_dec

	inc timer

	; отправляем команду EOI ведущему контроллеру прерываний
	mov	AL, 20h
	out	20h, AL

	pop EDI	
	pop EAX

	db 66h
	iretd
int08h endp

int09h proc
	push EAX
	push EBX
	push EBP
	push EDX

	in AL, 60h ; получаем скан-код нажатой клавиши из порта клавиатуры

	cmp	AL, 1Ch ; Сравниваем с кодом клавиши enter
	jne	print_key
	mov escape, 1 ; Иначе ставим флаг возвращения в реальный режим
	jmp exit
	
print_key:
	cmp AL, 80h ; Какой код пришел: нажатой или отпущенной клавиши?
	ja exit ; Если отпущенной, то ничего не выводим
	xor AH, AH ; Если нажатой, то выведем на экран
	mov BP, AX
	mov DL, ASCII_table[EBP] ; Получим ASCII код нажатой клавиши по коду из таблицы
	mov EBX, print_pos ; Текущая позиция вывода символа
	mov ES:[EBX], DL

	add EBX, 2 ; Увеличим текущую позицию вывода текста и сохраним ее
	mov print_pos, EBX

exit:
	; Разрешаем обрабатывать клавиатуру
	in	AL, 61h
	or	AL, 80h
	out	61h, AL
	and AL, 07Fh
	out 61h, AL

	; Посылаем сигнал EOI
	mov	AL, 20h
	out	20h, AL

	pop EDX
	pop EBP
	pop EBX
	pop	EAX

	; Выходим из прерывания
	db 66h
	iretd				
int09h endp

memory_cnt proc
    push DS
    mov AX, 40
    mov DS, AX          ; помещаем в DS селектор сегмента с базой 0
    mov EBX, 100001h    ; пропуск первого мегабайта
    mov DL,  10011001b  ; сигнатура
    mov ECX, 0FFEFFFFEh ; максимальный размер адресуемой памяти
	
memory_cnt_loop:
    mov DH, DS:[EBX]    ; сохраняем содержимое памяти
    mov DS:[EBX], DL    ; записываем сигнатуру
    cmp DS:[EBX], DL    ; сравниваем содержимое памяти с исходной сигнатурой
    jnz memory_cnt_end
    mov DS:[EBX], DH    ; восстанавливаем содержимое памяти
    inc EBX
	db 67h
    loop memory_cnt_loop
	
memory_cnt_end:
    pop DS          
    xor EDX, EDX
    mov EAX, EBX
    push EDI
    mov EDI, 14
    call print_number_dec            
    pop EDI                         

    ret
memory_cnt endp

print_number_dec proc
	push EAX
	push EBX
	push EDX
	push ECX
	push EDI

	mov EBX, 10

print:
	mov EDX, 0
	div EBX
	add DL, '0'
	
	mov ES:[EDI], DL
	sub EDI, 2
	cmp EAX, 0
 	jne print

	pop EDI
	pop ECX
	pop EDX
	pop EBX
	pop EAX
	ret
print_number_dec endp

code_size=$-main ; размер сегмента кода
text ends

stk segment stack use16					
	db 256 dup ('^')
stk	ends
	end main
