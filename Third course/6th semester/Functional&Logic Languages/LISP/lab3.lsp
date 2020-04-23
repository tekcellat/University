;1. Написать функцию, которая принимает целое число и возвращает первое четное число, не меньшее аргумента.
(defun fun (x) 
	(cond	((oddp x) (+ x 1))
			(t x)
	)
)
(fun 7)
(fun 10)

;2. Написать функцию, которая принимает число и возвращает число того же знака, но с модулем на 1 больше модуля аргумента.
(defun fun (x)
	(cond	((minusp x) (- x 1))
			(t	(+ x 1))
	)
)
(fun 5)
(fun -3)

;3. Написать функцию, которая принимает два числа и возвращает список из этих чисел, расположенный по возрастанию.
(defun fun (x y)
	(cond	((< x y) (list x y))
			(t (list y x))
	)
)
(fun 3 4)
(fun 6 5)
(fun 7 7)

;4. Написать функцию, которая принимает три числа и возвращает T, если первое число расположенно между вторым и третьим.
(defun fun (x y z)
	(and (>= x y) (<= x z))
)
(fun 1 2 3)
(fun 3 2 1)
(fun 2 1 3)

;5. Каков результат вычисления следующих выражений:
	(and 'fee 'fie 'foe)			(or nil 'fie 'foe)
;		foe								fie
	(or 'fee 'fie 'foe)				(and nil 'fie 'foe)
;		fee								nil
	(and (equal 'abc 'abc) 'yes)	(or (equal 'abc 'abc) 'yes)
;		YES								T

;6. Написать предикат, который принимает два числа-аргумента и возвращает Т, если первое число не меньше второго.
(defun fun (x y)
	(>= x y)
)
(fun 1 2)
(fun 2 2)
(fun 3 2)

;7. Какой из следующих двух вариантов предиката ошибочен и почему:
(defun pred1 (x)
	(and (numberp x) (plusp x))
)
(defun pred2 (x)
	(and (plusp x)(numberp x))
) ; VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV

;8. Решить задачу 4, используя для ее решения конструкции IF, COND, AND/OR.
(defun fun (x y z)
	(if (>= x y)
		(if (<= x z)
			t
		)
		nil
	)
)

(defun fun (x y z)
	(cond	((>= x y)
				(cond	((<= x z) t))
			)
			(t nil)
	)
)
(fun 1 2 3)
(fun 3 2 1)
(fun 2 1 3)

;9. Переписать функцию how-alike, приведенную в лекции и использующую COND, используя конструкции IF, AND/OR.
(defun how_alike(x y)
	(if	(or (= x y) (equal x y))
		'the_same
		(if	(and (oddp x) (oddp y))
			'both_odd
			(if	(and (evenp x) (evenp y))
				'both_even
				'difference
			)
		)
	)
)
(how_alike 4 4)