-- Инструкцию SELECT, использующую простое выражение CASE
-- Выводит всех медсестёр и остальных сотрудников
SELECT cooperator_name, cooperator_salary,
        CASE (cooperator_post)
            WHEN 'Nurse' THEN 'Nurse Info'
            ELSE 'Ex cooperator'
        END
FROM cooperator;

-- Инструкцию, использующую оконную функцию
-- Отображает среднюю зарплату по каждому отделу
SELECT DISTINCT department_name,
       avg(cooperator_salary) OVER (PARTITION BY department.department_id) AS AVG_SALARY
FROM department JOIN cooperator on cooperator.cooperator_department = department.department_id;

-- Список работников, которые продали продукции на сумму более 100
-- денежных единиц, и их продаже в сумме
SELECT WM.cooperator_id, sum(drug.drug_cost) AS total_sales
FROM cooperator as CO inner join cooperator_drug as WM on CO.id = WM.cooperator_id
inner join drug as D on WM.medicament_id = D.id
GROUP BY WM.cooperator_id
HAVING sum(D.drug_cost) > 100
ORDER BY total_sales DESC;
