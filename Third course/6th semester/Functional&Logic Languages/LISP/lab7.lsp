;1.	Написать итеративный вариант функции memberp, которая
;возвращает t или nil в зависимости от того, принадлежит ли первый
;аргумент второму, как элемент
(defun memberp (elem lst)
	(dolist	(index lst)
		(if	(equalp index elem)
			(return t)
		)
	)
)


;2.	Написать итеративный вариант функции assoc c именем it_assoc.
(defun it_assoc (item alist)
	(dolist	(x alist)
		(if	(equalp (car x) item)
			(return x)
		)
	)
)


;3.	Написать итеративный вариант функции length c именем it_length.
(defun it_length (lst)
	(do	(	(x lst (cdr x))
			(i 0 (+ i 1))
		)
		((null x) i)
	)
)


;4.	Написать итеративный вариант функции nth c именем it_nth. 
(defun it_nth (n lst)
	(do	(	(x lst (cdr x))
			(i 0 (+ i 1))
		)
		(	(or	(null x)
				(eq i n)
			)
			(car x)
		)
	)
)
;ИЛИ
(defun it_nth (n lst)
	(dotimes	(i n (car lst))
				(pop lst)
	)
)


;5.	Написать итеративный вариант функции reverse c именем
;it_reverse. 
(defun it_reverse (lst &aux (result nil))
	(dolist	(x lst)
			(setf result (cons x result))
	)
	result
)


;6.	Написать итеративные варианты функций, вычисляющих объединение,
;разность и симметрическую разность двух множеств.
(defun it_union (set1 set2 &aux (result (copy-seq set1)))
	(dolist	(y set2)
		(if	(not (member y result))
			(setf result (cons y result))
		)
	)
	result
)

(defun it_difference (set1 set2 &aux (result nil))
	(dolist	(x set1)
		(if	(not (member x set2))
			(setf result (cons x result))
		)
	)
	result
)

(defun it_symmetric_difference (set1 set2)
	(it_union	(it_difference set1 set2)
				(it_difference set2 set1)
	)
)


;7.	Используя в одном варианте dolist, а в другом do или do*,
;написать функцию, возвращающую наибольший элемент из списка чисел.
(defun find_largest (lst &aux (largest (car lst)))
	(dolist	(cur (cdr lst) largest)
		(if	(> cur largest)
			(setf largest cur)
		)
	)
)

(defun find_largest (lst)
	(do*	((largest (car lst))
			 (tail (cdr lst) (cdr tail))
			 (cur (car tail) (car tail))
			)
		((null tail) largest)
		(if	(> cur largest)
			(setf largest cur)
		)
	)
)


;8.	Используя в одном варианте dolist, а в другом do или do*, написать функцию, возвращающую первый нечисловой элемент заданного списка. Написать рекурсивный вариант этой же функции. 
(defun first_notnumber (lst)
	(dolist	(cur lst)
		(if	(not (numberp cur))
			(return cur)
		)
	)
)

(defun first_notnumber (lst)
	(do*	((tail lst (cdr tail))
			 (cur (car tail) (car tail))
			)
		((null tail) nil)
		(if	(not (numberp cur))
			(return cur)
		)
	)
)

(defun first_notnumber (lst) 
	(cond	((null lst) nil)
			((numberp (car lst))
				first_notnumber (cdr lst)
			)
			(t (car lst))
	)
) 


;9.	Написать итеративную и рекурсивную версии функции, которая
;сортирует по возрастанию полученный набор чисел. 
(defun bubble_rec (lst &aux (head (car lst)) (tail (cdr lst)))
	(cond	((null lst) nil)
			((= (length lst) 1) lst)
			((<= head (car tail))
				(check	(cons	head
								(bubble_rec tail)
						)
				)
			)
			(t (check	(cons	(car tail)
								(bubble_rec (cons	head
													(cdr tail)
											)
								)
						)
			))
	)
)
(defun check (lst)
	(if (<=	(car lst)
			(cadr lst)
		) 
		lst
		(bubble_rec lst)
	)
)

(defun bubble_it (lst &aux (len (length lst)))
	(dotimes	(i (- len 1))
		(dotimes	(j (- (- len i) 1))
			(if	(>	(nth j lst)
					(nth (+ j 1) lst)
				)
				(rotatef	(nth j lst)
							(nth (+ j 1) lst)
				)
			)
		)
	)
	lst
)