.386p ; Чтобы разрешить транслятору обрабатывать
      ; расширенный набор команд 32-разрядного микропроцессора,
			; часть к-х отн. к привелигерованным

; Пока не поздно - Рудаков-Ф. Раздел 6, Да, полностью
;									 Зубков Глава 6, можно пробежаться глазами


; ОСТАВЬ НАДЕЖДУ ВСЯК СЮДА ВХОДЯЩИЙ


; КРИТИЧЕСКОЕ ЗАМЕЧАНИЕ - программа начинается с метки start в сегменте RM_seg; затем, проделывая нессколько нехитрых, блять, манипуляций,
; мы переходим в защищенный режим на PM_Entry сегмента PM_seg

; НИЧЕГО НЕ ТРОГАТЬ, НЕ ПЕРЕСТАВЛЯТЬ, НЕ ПЕРЕПИСЫВАТЬ, НЕ ЧИХАТЬ, НЕ ДЫШАТЬ

; Я предупреждала

descr struc     ; Структура для описания декскриптора сегмента в таблице глобальных дескрипторов GDT
	lim 		dw 0	; Граница (биты 0..15)  - размер сегмента в байтах
	base_l 	dw 0	; Младшие 16 битов адресной базы. - базовый адрес задаётся в виртуальном адресном пространстве
	base_m 	db 0	; Следующие 8 битов адресной базы.
	attr_1	db 0	; Флаги/атрибуты доступа, определяющие в каком кольце защиты
	attr_2	db 0	; можно использовать этот сегмент.
	base_h 	db 0	; Последние 8 битов адресной базы.
descr ends

int_descr struc ; структура для описания декскриптора прерывания
	offs_l 	dw 0 	; Младшие 16 битов адреса, куда происходит переход в случае возникновения прерывания.
	sel			dw 0	; Селектор сегмента с кодом прерывания/Переключатель сегмента ядра
	counter db 0  ; Счётчик, не используется в программе. Всегда ноль!
	attr		db 0  ; Атрибуты
	offs_h 	dw 0  ; Старшие 16 битов адреса, куда происходит переход.
int_descr ends

; Protected mode
PM_seg	SEGMENT PARA PUBLIC 'DATA' USE32		; указываем, что команды работают со всеми 32 битов регистров; например LOOP будет
												                    ;декрементить ECX целиком, а не только его младшую половинку CX
										                        ;при этом если нам ВДРУГ понадобится "младший" луп, то его можно включить через пляску с бубном для каждого такого лупа
	                ASSUME	CS:PM_seg

    ; Таблица дескрипторов сегметов GDT
  	GDT		label	byte

  	; нулевой дескриптор
  	gdt_null	descr <>

  	; 32-битный 4-гигабайтный сегмент с базой = 0
  	gdt_flatDS	descr <0FFFFh,0,0,92h,11001111b,0>	; 92h = 10010010b

  	; 16-битный 64-килобайтный сегмент кода с базой RM_seg
  	gdt_16bitCS	descr <RM_seg_size-1,0,0,98h,0,0>	; 98h = 10011010b

  	; 32-битный 4-гигабайтный сегмент кода с базой PM_seg
  	gdt_32bitCS	descr <PM_seg_size-1,0,0,98h,01000000b,0>

  	; 32-битный 4-гигабайтный сегмент данных с базой PM_seg
  	gdt_32bitDS	descr <PM_seg_size-1,0,0,92h,01000000b,0>

  	; 32-битный 4-гигабайтный сегмент данных с базой stack_seg
  	gdt_32bitSS	descr <stack_l-1,0,0, 92h, 01000000b,0>

  	gdt_size = $-GDT ; размер нашей таблицы GDT+1байт (на саму метку)

  	gdtr	df 0	; переменная размера 6 байт как Регистр глобальной таблицы дескрипторов GDTR

    ; имена для селекторов
    SEL_flatDS     equ   8
    SEL_16bitCS    equ   16
    SEL_32bitCS    equ   24
    SEL_32bitDS    equ   32
    SEL_32bitSS    equ   40

    ; Таблица дескрипторов прерываний IDT
    IDT	label	byte

    ; первые 32 элемента таблицы (в программе не используются)
    int_descr 32 dup (<0, SEL_32bitCS,0, 8Eh, 0>)

    ; дескриптор прерывания от таймера
    int08 int_descr <0, SEL_32bitCS,0, 8Eh, 0>

    ; дескриптор прерывания от клавиатуры
    int09 int_descr	<0, SEL_32bitCS,0, 8Eh, 0>

    idt_size = $-IDT ; размер нашей таблицы IDT+1байт (на саму метку)

    idtr	df 0 ; переменная размера 6 байт как Регистр таблицы дескрипторов прерываний IDTR

    idtr_real dw	3FFh,0,0 ; содержимое регистра IDTR в реальном режиме

    master	db 0					 ; маска прерываний ведущего контроллера
    slave		db 0					 ; ведомого

    escape		db 0				 ; флаг - пора выходить в реальный режим, если ==1
    time_08		dd 0				 ; счетчик прошедших тиков таймера

		msg1 db 'In Real Mode now. To move to Protected Mode press any key...$'
		msg2 db 'In Real Mode again!$'

		; Таблица символов ASCII для перевода из скан кода в код ASCII.
		; Номер скан кода = номеру соответствующего элемента в таблице:
		ASCII_table	db 0, 0, 49, 50, 51, 52, 53, 54, 55, 56, 57, 48, 45, 61, 0, 0
					db 81, 87, 69, 82, 84, 89, 85, 73, 79, 80, 91, 93, 0, 0, 65, 83
					db 68, 70, 71, 72, 74, 75, 76, 59, 39, 96, 0, 92, 90, 88, 67
					db 86, 66, 78, 77, 44, 46, 47
		out_position	dd 1E0h ; Позиция печати вводимого текста




print_str macro str
		mov ah,9
		mov dx, str
		int 21h
endm


		; макрос для создания символа циферки (или буковки) из чиселки (7 -> '7', 15 -> 'F')
create_number macro
		local number1
			cmp dl,10
			jl number1
			add dl,'A' - '0' - 10
		number1:
			add dl,'0'
endm



		; макрос печати на экран значения регистра ЕАХ через видеобуффер
my_print_eax macro
		local prcyc1 				; указываем, что метка локальная для макроса; на каждой подстановке она должна называться по разному
			push ecx 					; сохраняем используемые регистры
			push dx

			mov ecx,8					; количество символов, которые распечатаем
			add ebp,0B8010h 	; сейчас в EBP должно лежать положение первого символа на экране, с которого и будет распечатано число
												; 0B8000h - смещение видеобуффера относительно начала сегмента.
												; Ещё 10h - добавляем 8 символов, поскольку число печатается справа-налево
		prcyc1:
			mov dl,al					; кладём в DL текущее значение AL (самый младший байт ЕАХ)
			and dl,0Fh				; оставляем от него одно 16ричное число (последняя цифра)
			create_number 0		; превращаем это число в символ
			mov es:[ebp],dl		; запихиваем его в видеобуфер
			ror eax,4					; циклически двигаем биты в ЕАХ - таким образом, после всех перестановок,
												; ЕАХ окажется тем же что и в начале, нет необходимости на PUSH; POP
			sub ebp,2					; смещаемся на один символ влево (предыдущая цифра в ЕАХ)
			loop prcyc1				; повторяемся 8 раз

			sub ebp,0B8010h		; возвращаем в EBP то же значение, что было в нём до пляски с видеопамятью
			pop dx
			pop ecx
endm


	; точка входа в 32-битный защищенный режим
PM_entry:
		; ранее в реальном режиме мы загрузили в дескрипторы адреса сегментов данных, стека и кода;
		;теперь мы непосредственно их устанавливаем
		mov	ax,SEL_32bitDS
		mov	ds,ax
		mov	ax,SEL_flatDS
		mov	es,ax
		mov	ax,SEL_32bitSS
		mov	ebx,stack_l
		mov	ss,ax
		mov	esp,ebx

		; разрешить прерывания, запрещенные ранее ещё в реальном режиме
		sti ; установка флага прерывания IF = 1

		;считаем количество доступной памяти и печатаем его на экран
		call	compute_memory

		;крутимся в бесконечном цикле, периодически натыкаясь на прерывания клавиатуры и таймера
		;выход из цикла - по нажатию Enter (прописано в обработчике прерывания клавиатуры new_int09)
work:
		test	escape, 1
		jz	work

goback:
		; запрещаем прерывания, всё по той же причине
		; при этом немаскируемые уже запрещены, их не трогаем
		cli ; сброс флага прерывания IF = 0

		; а вы думали мы будем подробно описывать переход в реальность? йух, тут магия, а потом мы просто переходим по метке RM_return
		db	0EAh ; не трогать, вообще, в принципе, ни прикаких условиях, запрещаем, все заинтересованные в магии к Рудакову-Ф.
		; шутка. Это просто код команды far jump
		dd	offset RM_return
		dw	SEL_16bitCS


	;новый самопальный обработчик прерывания таймера, который будет в защищенном режиме крутить счетчик time_08
new_int08:
		; пролог тырпырдыр
		push eax
		push ebp
		push ecx
		push dx
		mov  eax,time_08

		; кладём в EBP смещение на 8 символов от начала экрана
		push ebp
		mov ebp, 0					; указываем смещение в видеопамяти относительно начала экрана (10 символов - 1 байт символа и 1 байт цвета )
		my_print_eax 0			; вызываем чудо-макрос видео-печати
		pop ebp							; восстанавливаем потраченное смещение EBP

		inc eax
		mov time_08,eax

		; эпилог, наверное
		pop dx
		pop ecx
		pop ebp

		;обязательная щепотка магии, без которой никуда; отправляем команду End of Interrupt ведущему контроллеру прерываний
		mov	al,20h
		out	20h,al
		pop eax

		iretd ;выходим из прерывания

		; Новый обработчик прерывания клавиатуры для защищенного режима:
new_int09:
			push eax
			push ebx
			push ebp
			push edx

			in	al,60h 		 ; Получаем скан-код нажатой клавиши из порта клавиатуры

			cmp	al,1Ch 	     ; Сравниваем с кодом энтера
			jne	not_leave 	 ; Если не энтер - ввыведем, то что ввели
			mov escape,1     ; Если энтер - ставим флаг, что нужно вернуться в реальный режим
			jmp leav
not_leave:
			cmp al,80h 	 ; Сравним какой скан-код пришел: нажатой клавиши или отжатой?
			ja leav 	 ; Если отжатой, то ничего не выводим
			xor ah,ah	 ; Если нажатой, то выведем на экран
			mov bp,ax
			mov dl,ASCII_table[ebp] ; Получим ASCII код нажатой клавиши по скан коду из таблицы
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

; Ты еще уверен, что хочешь это видеть?



; танец с бубном (функция подсчета доступной памяти)
compute_memory	proc

		push	ds            ; сохраняем прошлое значение DS
		mov	ax, SEL_flatDS	; кладем в него сегмент на 4 ГБ - все доступное виртуальное АП
		mov	ds, ax					; суем сию прелесть в DS
		mov	ebx, 100001h		; пропускаем первый мегабайт оного сегмента
		mov	dl,	10101010b	  ; попытка считать значение из несуществующего байта памяти вернёт все нули (или все единицы)
												; в каждый байт мы пишем какое-то значение, а потом смотрим, что прочитается

		mov	ecx, 0FFEFFFFEh	; в ECX кладём количество оставшейся памяти (до превышения лимита в 4ГБ) - чтобы не было переполнения

		; в цикле считаем память
check:
		mov	dh, ds:[ebx]		; сохраняем в DH текущее значение по некоторому байту памяти
												; EBX на первой итерации содержит смещение за 1й мегабайт памяти
												; мегабайт пропускаем потому, что в противном случае может произойти
												; попытка редактирования процедуры собственного кода, что есть крайне не торт
		mov	ds:[ebx], dl		; кладём некоторое значение (заданное выше DL) в этот байт
		cmp	ds:[ebx], dl		; проверяем - считается обратно то же DL, или какая-то хрень
		jnz	end_of_memory		; если считается хрень - то мы достигли дна, а на дне лежит конец памяти, вываливаемся из цикла
		mov	ds:[ebx], dh		; если дна не достигли - кладём обратно сохранённое значение, чтобы не попортить лишнего на всякий
		inc	ebx							; проверяем следующий байт.... ну вы поняли, ждать придётся столько, сколько гигабайтов ОЗУ в машине
												; к счастью, в досбоксе обычно всего 16 МБ памяти, так что не очень-то и долго ждать
												; желающие ждать больше (меньше?) могут поменять эти 16 МБ в конфиге досбокса
		loop	check
end_of_memory:
		pop	ds							; мемориджоб подошёл к логическому концу, память кончилась - восстанавливаем регистры
		xor	edx, edx
		mov	eax, ebx				; в EBX лежит количество посчитанной памяти в байтах; кладём его в EAX,
		mov	ebx, 100000h		; делим на 1 Мб, чтобы получить результат в мегабайтах
		div	ebx

		push ebp
		mov ebp,20					; указываем смещение в видеопамяти относительно начала экрана (10 символов - 1 байт символа и 1 байт цвета )
		my_print_eax 0			; вызываем чудо-макрос видео-печати
		pop ebp							; восстанавливаем потраченное смещение EBP

		ret
	compute_memory	endp


	PM_seg_size = $-GDT
PM_seg	ENDS

; Я ведь тебя предупреждала

stack_seg	SEGMENT  PARA STACK 'STACK'
	stack_start	db	100h dup(?)
	stack_l = $-stack_start							; длина стека для инициализации ESP
stack_seg 	ENDS




; Real Mode
RM_seg	SEGMENT PARA PUBLIC 'CODE' USE16		; USE16 - используем нижние части регистров, АХ ВХ СХ; верхние биты E* в реальном режиме недоступны
	ASSUME CS:RM_seg, DS:PM_seg, SS:stack_seg

start:

		mov   ax,PM_seg
		mov   ds,ax

		mov ah, 09h
		mov edx, offset msg1
		int 21h

		;ожидаем ввода клавиатуры
		push eax;сохраняем, чтоб не потерять AX
		mov ah,10h
		int 16h
		pop eax;и восстанавливаем

		; очистить экран
		mov	ax,3
		int	10h

		; настроить регистр ds на сегмент с защищенном режимом
		push PM_seg
		pop ds

		; вычислить базы для всех используемых дескрипторов сегментов
		xor	eax,eax
		mov	ax,RM_seg
		shl	eax,4		; сегменты объявлены как PARA, нужно сдвинуть на 4 бита для выравнивания по границе параграфа
		mov	word ptr gdt_16bitCS.base_l,ax
		shr	eax,16
		mov	byte ptr gdt_16bitCS.base_m,al
		mov	ax,PM_seg
		shl	eax,4
		push eax		; для вычисления адреса idt
		push eax		; для вычисления адреса gdt
		mov	word ptr GDT_32bitCS.base_l,ax
		mov	word ptr GDT_32bitSS.base_l,ax
		mov	word ptr GDT_32bitDS.base_l,ax
		shr	eax,16
		mov	byte ptr GDT_32bitCS.base_m,al
		mov	byte ptr GDT_32bitSS.base_m,al
		mov	byte ptr GDT_32bitDS.base_m,al

		; вычислим линейный адрес GDT
		pop eax
		add	eax,offset GDT 						; в eax будет полный линейный адрес GDT (адрес сегмента + смещение GDT относительно него)
		; аттеншен - все адреса в защищённом режиме ВИРТУАЛЬНЫЕ
		mov	dword ptr gdtr+2,eax			; кладём полный линейный адрес в младшие 4 байта переменной gdtr
		mov word ptr gdtr, gdt_size-1	; в старшие 2 байта заносим размер gdt, из-за определения gdt_size (через $) настоящий размер на 1 байт меньше
		; загрузим GDT
		lgdt	fword ptr gdtr

		; аналогично вычислим линейный адрес IDT
		pop	eax
		add	eax,offset IDT
		mov	dword ptr idtr+2,eax
		mov word ptr idtr, idt_size-1

		; Заполним смещение в дескрипторах прерываний
		mov	eax, offset new_int08 ; прерывание таймера
		mov	int08.offs_l, ax
		shr	eax, 16
		mov	int08.offs_h, ax
		mov	eax, offset new_int09 ; прерывание клавиатуры
		mov	int09.offs_l, ax
		shr	eax, 16
		mov	int09.offs_h, ax

		; сохраним маски прерываний контроллеров
		in	al, 21h							; ведущего, 21h - "магическая константа" - номер шины, in на неё даст нам набор масок (флагов)
		mov	master, al					; сохраняем в переменной master (понадобится для возвращения в RM)
		in	al, 0A1h						; ведомого - аналогично, in даёт набор масок для ведомого
		mov	slave, al

		; кучка магии (перепрограммируем ведущий контроллер)
		mov	al, 11h							; команда "инициализировать ведущий контроллер"
		out	20h, al							; 20h - условно говоря, "порт включения\выключения"
		mov	AL, 20h							; базовый вектор (начальное смещение для обработчика) теперь 32 (20h)
		out	21h, al							; указываем, что аппаратные прерывания будут обрабатываться начиная с 32го (20h)
		mov	al, 4								; отправляем в тот же порт ещё две магические константы,
														; дефакто - команды, благодаря которым всё акшуалли заработает
		out	21h, al
		mov	al, 1							  ; указываем, что нужно будет посылать команду завершения обработчика прерывания
		out	21h, al

		; Запретим все прерывания в ведущем контроллере, кроме IRQ0 (таймер) и IRQ1(клавиатура)
		mov	al, 0FCh
		out	21h, al

		;запретим ВООБЩЕ ВСЕ прерывания в ведомом контроллере
		;в противном случае возникнет исключение - может прийти прерывание, для которого у нас не написан обработчик
		mov	al, 0FFh
		out	0A1h, al

		; загрузим IDT
		lidt	fword ptr idtr

		; если мы собираемся работать с 32-битной памятью, стоит открыть A20
		; А20 - линия ("шина"), через которую осуществляется доступ ко всей памяти за пределами первого мегабайта
		in	al,92h						; поймали набор флагов
		or	al,2							; добавили в нём единичку во 2 бите
		out	92h,al						; отправили обратно

		; отключить маскируемые прерывания
		; если во время перехода в защищённый режим к нам ВНЕЗАПНО придёт хоть какое-нибудь прерывание - может произойти целый ворох
		; неведомой херни, в результате который процессор так или иначе упадёт в варп - одни обработчики прерываний УЖЕ не работают, другие - ЕЩЁ не работают
		cli
		; затем вдогонку и немаскируемые прерывания
		in	al,70h
		or	al,80h
		out	70h,al

		; перейти в непосредственно защищенный режим установкой соответствующего бита регистра CR0
		mov	eax,cr0
		or	al,1
		mov	cr0,eax

		; напрямую загрузить SEL_32bitCS в регистр CS мы не можем из-за защитных ограничений ассемблера; добавим немного магии
		db	66h
		db	0EAh
		dd	offset PM_entry
		dw	SEL_32bitCS
		; начиная с этой строчки, будет выполняться код по оффсету PM_entry
		; быдлоговоря, из-за ^ ограничений, вместо MOV CS, offset SEL_32bitCS; jmp PM_entry, нам приходится использовать вот такие костыли
		; теперь, дорогой юзер, мотай блокнот на пару сотен строк вверх

RM_return:
		; переход в реальный режим; подробности - у Рудакова-Ф.
		mov	eax,cr0
		and	al,0FEh 				; сбрасываем флаг защищенного режима
		mov	cr0,eax

		; сбросить очередь и загрузить CS реальным числом
		db	0EAh						; пляски с бубном - опять из-за ограничения доступа к CS
		dw	$+4							; вот это прям мое любимое место
		dw	RM_seg

		; восстановить регистры для работы в реальном режиме
		mov	ax,PM_seg				; загружаем в сегментные регистры "нормальные" (реальные) смещения
		mov	ds,ax
		mov	es,ax
		mov	ax,stack_seg
		mov	bx,stack_l
		mov	ss,ax
		mov	sp,bx

		;перепрограммируем ведущий контроллер обратно на вектор 8 - смещение, по которому вызываются стандартные обработчики прерываний в реалмоде
		mov	al, 11h					; инициализация
		out	20h, al
		mov	al, 8						; отправка смещения
		out	21h, al
		mov	al, 4						; волшебные команды, "код - работай!"
		out	21h, al
		mov	al, 1
		out	21h, al

		;восстанавливаем предусмотрительно сохраненные ранее маски контроллеров прерываний
		mov	al, master
		out	21h, al
		mov	al, slave
		out	0A1h, al

		; загружаем таблицу дескрипторов прерываний реального режима
		lidt	fword ptr idtr_real

		; разрешаем обратно немаскируемые прерывания
		in	al,70h
		and	al,07FH
		out	70h,al

    ; а затем маскируемые
		sti

		; очистить экран
		mov	ax,3
		int	10h

		; печать сообщения о выходе из защищенного
		mov ah, 09h
		mov edx, offset msg2
		int 21h


		; как в старые добрые завершаем программу через int 21h по команде 4Ch
		mov	ah,4Ch
		int	21h

RM_seg_size = $-start 	; завершаем сегмент, указываем метку начала для сегмента
RM_seg	ENDS
END start