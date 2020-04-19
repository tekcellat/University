.386p

; Структура для описания декскриптора сегмента:
descr struc
lim 	dw 0	; Граница (биты 0..15)
base_l 	dw 0	; База, биты 0..15
base_m 	db 0	; База, биты 16..23
attr_1	db 0	; Байт атрибутов 1
attr_2	db 0	; Граница(биты 16..19) и атрибуты 2
base_h 	db 0	; База, биты 24..31
descr ends

; Структура для описания декскриптора прерываний:
int_descr struc
offs_l	dw 0 	; Смещение в сегменте (нижняя часть)
sel		dw 0	; Селектор сегмента с кодом прерывания
reserv 	db 0	; Резерв (не используется в программе)
attr	db 0	; Атрибуты
offs_h 	dw 0	; Смещение в сегменте (верхняя часть)
int_descr ends

; Сегмент данных:
data	SEGMENT PARA PUBLIC 'DATA' USE16

; Таблица глобальных дескрипторов GDT:
gdt_null	descr <0,0,0,0,0,0>                             ; Селектор 0 (нулевой дескриптор)
gdt_memory	descr <0FFFFh,0,0,92h,11001111b,0>              ; Селектор 8, 32-битный, 4Гб сегмент
gdt_data	descr <data_size-1,0,0,92h,01000000b,0>         ; Селектор 16, 32-битный сегмент данных
gdt_code16	descr <real_mode_size-1,0,0,98h,0,0>            ; Селектор 24, 16-битный сегмент кода, 98h = 10011010b
gdt_code32	descr <protect_mode_size-1,0,0,98h,01000000b,0> ; Селектор 32, 32-битный сегмент кода
gdt_stack	descr <stack_size-1,0,0,92h,01000000b,0>        ; Селектор 40, 32-битный сегмент стека

; Размер таблицы GDT:
gdt_size = $-gdt_null

; Переменная размером 6 байт для GDT:
gdtr    df	0

; Имена для селекторов:
SEL_memory	equ	8
SEL_data    equ 16
SEL_code16  equ 24
SEL_code32  equ 32
SEL_stack   equ 40

; Таблица дескрипторов прерываний IDT:
IDT	label	byte                          ; Метка для подсчета размера IDT
exceptions int_descr 32 dup (<0,SEL_code32,0,8Fh,0>) ; Первые 32 элемента таблицы (исключения)
my_int08 int_descr <0,SEL_code32,0,8Eh,0> ; Дескриптор прерывания от таймера
my_int09 int_descr <0,SEL_code32,0,8Eh,0> ; Дескриптор прерывания от клавиатуры

; Размер таблицы IDT:
idt_size = $-IDT

; Переменная размером 6 байт для IDT:
idtr	df 0

; Содержимое регистра IDTR в реальном режиме:
idtr_real	dw	3FFh,0,0

master_mask	db 0 ; Маска прерываний ведущего контроллера
slave_mask	db 0 ; Маска прерываний ведомого контроллера

exit_p	db 0 ; Флаг выхода в реальный режим, если = 1
time	dd 0 ; Счётчик прошедших тиков таймера

; Строки для вывода при переходе в реальный режим:
msg_protect db 'P',7,'r',7,'o',7,'t',7,'e',7,'c',7,'t',7,' ',7,'m',7,'o',7,'d',7,'e',7,' ',7,'o',7,'n'
msg_protect_size = $-msg_protect
msg_real db 0Ah,0Ah,0Ah,0Ah,'Real mode on$'

; Таблица символов ASCII для перевода из скан кода в код ASCII.
; Номер скан кода = номеру соответствующего элемента в таблице:
ASCII_table	db 0, 0, 49, 50, 51, 52, 53, 54, 55, 56, 57, 48, 45, 61, 0, 0
			db 81, 87, 69, 82, 84, 89, 85, 73, 79, 80, 91, 93, 0, 0, 65, 83
			db 68, 70, 71, 72, 74, 75, 76, 59, 39, 96, 0, 92, 90, 88, 67
			db 86, 66, 78, 77, 44, 46, 47
out_position	dd 1E0h ; Позиция печати вводимого текста

; Размер сегмента данных:
data_size = $-gdt_null

data	ENDS

; Сегмет стека:
stack	SEGMENT PARA STACK 'STACK'
	stack_start	db 256 dup(?)
	stack_size = $-stack_start ; Длина стека
stack 	ENDS

; Сегмент кода в защищённом режиме (32 бит):
protect_mode	SEGMENT PARA PUBLIC 'CODE' USE32
	ASSUME	CS:protect_mode, DS:data

;Точка входа в 32-битный защищенный режим
protect_main:
    	mov	ax,SEL_data
    	mov	ds,ax
    	mov	ax,SEL_memory
    	mov	es,ax
    	mov	ax,SEL_stack
    	mov	ebx,stack_size
    	mov	ss,ax
    	mov	esp,ebx

    	; Разрешим маскируемые прерывания, запрещённые ранее в реальном режиме:
    	sti

    	; Выведем строку о том, что мы прешли в защищённый режим:
    	mov esi,offset msg_protect
    	mov edi,0B8000h
    	mov ecx,msg_protect_size
    	rep movsb ; Записываем в ячейку по адресу ES:EDI байт из ячейки с адресом DS:ESI (т.е. в видеобуфер из строки)

    	; Посчитаем количество доступной памяти и напечатаем его на экран:
    	mov	ebx, 100001h	; Пропуск первого мегабайта сегмента
    	mov	dl,	10101010b	; Байт сигнатура (просто какое-то значение)
    	mov	ecx, 0FFFFFFDEh	; Сколько до конца памяти

; Считаем в цикле память:
count:
    	mov	dh, es:[ebx]    ; Сохраняем в DH текущее значение по некоторому байту памяти

    	mov	es:[ebx], dl	; Кладём некоторое значение (заданное выше DL) в этот байт
    	cmp	es:[ebx], dl	; Проверяем - считается обратно то же DL, или нет
    	jnz	end_of_memory	; Если нет - то достигли конец памяти, выход из цикла
    	mov	es:[ebx], dh	; Если считалось все правильно,
    						; то возвращаем сохранённое значение из DH, чтобы не испортить лишнего
    	inc	ebx				; Берём на проверку следующий байт
    	loop count
end_of_memory:
    	mov	eax, ebx		; В EBX теперь лежит количество посчитанной памяти в байтах, кладём его в EAX
    	mov	ebx, 100000h	; Делим на 1 Мб, чтобы получить результат в мегабайтах
    	xor	edx, edx
    	div	ebx

		; Выведем количество памяти на экран
    	mov ebp,0B8000h
    	mov ebx,0AEh
    	mov ecx,8

print_mem:
    	mov dl,al
    	and dl,0Fh
    	cmp dl,10
    	jl is_number_mem
    	add dl, 'A' - '0' - 10
is_number_mem:
    	add dl,'0'
    	mov es:[ebp+ebx],dl
    	sub ebx,2
    	ror eax,4
    	loop print_mem

; Входим в бесконечный цикл
; Выход из цикла по нажатию энтера (прописано в обработчике прерывания клавиатуры new_int09):
main_cycle:
    	cmp exit_p, 0
    	jz 	main_cycle

return:
    	; Запрещаем маскируемые прерывания:
    	cli

    	db	0EAh
    	dd	offset real_mode_return
    	dw	SEL_code16

; Новый обработчик прерывания таймера для защищенного режима
; (увеличивает счетчик таймера и выводит мигающий смайлик):
new_int08:
    	push eax
    	push ebp
    	push ecx
    	push ebx
    	push edx

    	mov eax,time

    	;Вывод на экран
    	mov ebp,0B8000h
    	mov ebx,14Eh
    	mov ecx,8

print:
    	mov dl,al
    	and dl,0Fh
    	cmp dl,10
    	jl is_number
    	add dl, 'A' - '0' - 10
is_number:
    	add dl,'0'
    	mov es:[ebp+ebx],dl
    	sub ebx,2
    	ror eax,4
    	loop print

    	; Небольшая задержка для мигания смайлика (каждый тик):
    	test eax,2
    	jnz skip
    	mov dl,1
    	mov es:[ebp+152h],dl
    	jmp inc_
skip:
    	mov dl,0
        mov es:[ebp+152h],dl

    	; Увеличиваем счетчик и записываем его:
inc_:
    	inc eax
    	mov time,eax

    	; Посылаем сигнал EOI (End of Interrupt) контроллеру прерываний, уведомив его о завершении обработки:
    	mov	al,20h
    	out	20h,al

    	pop edx
    	pop ebx
    	pop ecx
    	pop ebp
    	pop eax

    	; Выходим из прерывания:
    	iretd

; Новый обработчик прерывания клавиатуры для защищенного режима:
new_int09:
    	push eax
    	push ebx
    	push ebp
    	push edx

    	in	al,60h 		 ; Получаем скан-код нажатой клавиши из порта клавиатуры

    	cmp	al,1Ch 	     ; Сравниваем с кодом энтера
    	jne	not_leave 	 ; Если не энтер - ввыведем, то что ввели
    	mov exit_p,1     ; Если энтер - ставим флаг, что нужно вернуться в реальный режим
    	jmp leav
not_leave:
    		cmp al,80h 	 ; Сравним какой скан-код пришел: ажатой клавиши или отжатой?
    		ja leav 	 ; Если отжатой, то ничего не выводим
    		xor ah,ah	 ; Если нажатой, то выведем на экран
    		mov bp,ax
            mov dl,ASCII_table[bp] ; Получим ASCII код нажатой клавиши по скан коду из таблицы
    		mov ebp,0B8000h
    		mov ebx,out_position   ; Текущая позиция вывода символа
            mov es:[ebp+ebx],dl

    		add ebx,2			   ; Увеличим текущую позицию вывода текста и сохраним ее
    		mov out_position,ebx

leav:
    	; Разрешаем обрабатывать клавиатуру дальше:
    	in	al,61h
    	or	al,80h
    	out	61h,al

    	; Посылаем сигнал EOI:
    	mov	al,20h
    	out	20h,al

    	pop edx
    	pop ebp
    	pop ebx
    	pop	eax

    	; Выходим из прерывания:
    	iretd

		; Заглушка для исключения:
		stub:

protect_mode_size = $-protect_main ; Получаем длину сегмента кода для защищенного режима
protect_mode	ENDS

; Сегмент кода в реальном режиме (16 бит)
real_mode	SEGMENT PARA PUBLIC 'CODE' USE16
    ASSUME CS:real_mode, DS:data, SS:stack
main:
    	; Очистим экран, чтобы нормально было видно количество памяти и изменение таймера:
    	mov	ax,3
    	int	10h

    	xor eax,eax ; Чистим EAX
    	mov ax,data ; Грузим в DS сегментный адрес сегмента данных
    	mov ds,ax

    	; Вычислим 32-битовые линейные адреса для всех используемых дескрипторов сегментов и загрузим их в
    	; дескриптор соответствующих сегментов в таблице глобальных дескрипторов GDT.
    	; Начнём с сегмента данных, т.к. он уже лежит в AX:
    	shl	eax,4
    	mov ebp,eax
    	mov bx,offset gdt_data ; BX - смещение дескриптора
    	mov [bx].base_l,ax     ; Загрузим младшую часть базы
    	shr	eax,16             ; Старшую половину EAX в AX
    	mov	[bx].base_m,al     ; Загрузим среднюю часть базы

    	; Теперь сегмент кода реального режима:
    	xor	eax,eax ; Чистим EAX
    	mov	ax,cs   ; Сегментный адрес сегмента кода
    	shl	eax,4   ; Далее аналогично загрузке сегмента данных
    	mov	bx,offset gdt_code16
    	mov	[bx].base_l,ax
    	shr	eax,16
    	mov	[bx].base_m,al

    	; Теперь сегмент кода защищенного режима:
    	xor	eax,eax           ; Чистим EAX
    	mov	ax,protect_mode   ; Сегментный адрес сегмента кода
    	shl	eax,4             ; Далее аналогично загрузке сегмента данных
    	mov	bx,offset gdt_code32
    	mov	[bx].base_l,ax
    	shr	eax,16
    	mov	[bx].base_m,al

    	; Считаем и грузим сегент стека:
    	xor	eax,eax ; Чистим EAX
    	mov	ax, ss  ; Сегментный адрес сегмента стека
    	shl	eax,4   ; Далее аналогично
    	mov	bx,offset gdt_stack
    	mov	[bx].base_l,ax
    	shr	eax,16
    	mov	[bx].base_m,al

    	; Вычислим линейный адрес GDT и загрузим регистр GDTR:
    	mov	dword ptr gdtr+2,ebp ; Помещаем линейный адрес(база GDT) в младшие 4 байта переменной gdtr
    	mov word ptr gdtr,gdt_size-1
    	lgdt gdtr

    	; Аналогично вычислим линейный адрес IDT:
    	mov eax,ebp
    	add	eax,offset IDT ; В EAX линейный адрес IDT (адрес сегмента данных + смещение IDT относительно него)
    	mov	dword ptr idtr+2,eax
    	mov word ptr idtr,idt_size-1

    	; Заполним смещения в дескрипторах прерываний:
    	mov	eax,offset new_int08 ; Новое прерывание таймера
    	mov	my_int08.offs_l,ax
    	shr	eax,16
    	mov	my_int08.offs_h,ax
    	mov	eax,offset new_int09 ; Новое прерывание клавиатуры
    	mov	my_int09.offs_l,ax
    	shr	eax,16
    	mov	my_int09.offs_h,ax

		mov cx, 32
		exceptions_loop:
			xor ebp, ebp
			mov eax, offset stub
			mov exceptions[ebp].offs_l, ax
			shr eax, 16
			mov exceptions[ebp].offs_h, ax
			add ebp, 8
		loop exceptions_loop

    	; Загрузим IDT
    	lidt idtr

    	; Cохраним маски прерываний контроллеров:
    	in	al,21h         ; Ведущего (получаем маски)
    	mov	master_mask,al ; Сохраняем в переменной master_mask (нужно для возвращения в реальный режим)
    	in	al,0A1h        ; Ведомого
    	mov	slave_mask,al  ; Аналогично сохраняем в переменной slave_mask

    	mov	al, 11h ; Команда инициализации (ведущего контроллера)
    	out	20h,al	; Ведущий контроллер (20h - "порт включения\выключения")
    	mov	al,20h	; Базовый вектор ведущего контроллера (начальное смещение для обработчика) теперь 32 (20h)
    	out	21h,al	; Указываем, что аппаратные прерывания будут обрабатываться начиная с 32го (20h)
    	mov	al,4    ; Управляющее слово
    	out	21h,al
    	mov	al,1
    	out	21h,al

    	; Запретим все прерывания в ведущем контроллере, кроме IRQ0 (таймер) и IRQ1 (клавиатура):
    	mov	al,0FCh
    	out	21h,al

    	; Запретим все прерывания в ведомом контроллере:
    	mov	al,0FFh
    	out	0A1h,al

    	; Так как мы работаем с 32-битной памятью надо открыть линию A20:
    	in	al,92h
    	or	al,2	; Установим единичку во 2-м бите
    	out	92h,al

    	; Отключаем маскируемые прерывания:
    	cli
    	; Отключаем немаскируемые прерывания (NMI):
    	in	al,70h
    	or	al,80h
    	out	70h,al

    	; Переходим в защищённый режим установкой соответствующего бита (PE) регистра CR0:
    	mov	eax,cr0
    	or	al,1
    	mov	cr0,eax

    	; Загружаем в CS:IP селектор:смещение точки protect_main:
    	db	66h  ; Префикс изменения размера операнда
    	db	0EAh ; Код команды far jmp
    	dd	offset protect_main
    	dw	SEL_code32

real_mode_return:
    	; Возврат в реальный режим:
    	mov	eax,cr0
    	and	al,0FEh 	  ; Cбрасываем флаг защищенного режима (бит PE)
    	mov	cr0,eax

    	; Сбросим очередь и загрузим CS:
    	db	0EAh          ; Из-за ограничения доступа к CS
    	dw	$+4
    	dw	real_mode

    	; Восстановим регистры для работы в реальном режиме:
    	mov	ax,data       ; Загрузка в сегментные регистры реальные смещения
    	mov	ds,ax
    	mov	ax,stack
    	mov	bx,stack_size
    	mov	ss,ax
    	mov	sp,bx

    	;Перепрограммируем ведущий контроллер обратно на вектор 8 - смещение,
    	;по которому вызываются стандартные обработчики прерываний в реальном режиме:
    	mov	al, 11h
    	out	20h,al
    	mov	al,8      ; Установка смещения
    	out	21h,al
    	mov	al,4      ; Управляющее слово
    	out	21h,al
    	mov	al,1
    	out	21h,al

    	; Восстанавливаем сохраненные ранее маски контроллеров прерываний:
    	mov	al,master_mask ; Для ведущего контроллера
    	out	21h,al
    	mov	al,slave_mask  ; Для ведомого контроллера
    	out	0A1h,al

    	; Загружаем таблицу дескрипторов прерываний реального режима:
    	lidt fword ptr idtr_real

    	; Разрешаем немаскируемые прерывания:
    	in	al,70h
    	and	al,07FH
    	out	70h,al

        ; Разрешаем маскируемые прерывания:
    	sti

    	; Выведем на экран строку о том, что мы вернулись в реальный режим:
    	mov ah,09h
    	mov dx,offset msg_real
    	int 21h

    	; Завершаем работу программы:
    	mov	ah,4Ch
    	int	21h

real_mode_size = $-main ; Получаем длину сегмента кода для реального режима
real_mode	ENDS
END	main
