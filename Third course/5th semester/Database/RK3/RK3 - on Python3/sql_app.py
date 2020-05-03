import psycopg2
import datetime
import copy

con = psycopg2.connect(
        database='rk3',
        username='postgres',
        password='notforyou)))',
        host='localhost'
    )

#####################################################################################
# Find department, where employee is late more than 3 times in a week.
def task_one():
    cur = con.cursor()
    cur.execute("select * from employee")
    employees = cur.fetchall()
    cur.execute("select * from timetable")
    timetable = cur.fetchall()
    t = []

    for line1 in employees:
        for line2 in timetable:
            if line1[0] == line2[0]:
                t.append((line1[0], line1[1], line1[2], line1[3], line2[1], line2[2],
                          line2[3], line2[4]))
    dep = {}
    staff = {}
    for i in range(len(t)):
        dep[t[i][3]] = 0
        staff[t[i][0]] = 0

    for i in range(len(t)):
        if t[i][6] > datetime.time(9, 0) and t[i][-1] == 1:
            staff[t[i][0]] += 1
        if staff[t[i][0]] > 3:
            dep[t[i][3]] += 1
    print('Departments, where employee is late more than 3 times in a week')
    for i in list(dep.keys()):
        if dep[i] > 0:
            print(i)

#####################################################################################
# Find average age of employes, which don't work 8 hours a day.

def calculate_age(birth_date): # function, that counts age of employee by the birth date given 
    today = datetime.date.today()
    try:
        birthday = birth_date.replace(year=today.year)
    except ValueError:
        birthday = birth_date.replace(year=today.year,
                                month=birth_date.month + 1, day=1)

    if birthday > today:
        return today.year - birth_date.year - 1
    else:
        return today.year - birth_date.year

def task_two():
    cur = con.cursor()
    cur.execute('SELECT * FROM timetable')
    timetable = cur.fetchall()
    cur.execute('SELECT * FROM employee')
    employees = cur.fetchall()

    empls = dict()
    for employee in employees:
        empls[employee[0]] = False

    for i in range(len(timetable) - 1):
        for j in range(len(timetable) - i - 1):
            if timetable[j][0] > timetable[j + 1][0]:
                timetable[j], timetable[j + 1] = timetable[j + 1], timetable[j]

    for i in range(len(timetable) - 1):
        for j in range(len(timetable) - i - 1):
            if timetable[j][1] > timetable[j + 1][1] and timetable[j][0] == timetable[j + 1][0]:
                timetable[j], timetable[j + 1] = timetable[j + 1], timetable[j]

    for i in range(len(timetable) - 1):
        for j in range(len(timetable) - i - 1):
            if timetable[j][3] > timetable[j + 1][3] and timetable[j][0] == timetable[j + 1][0] and \
                    timetable[j][1] == timetable[j + 1][1]:
                timetable[j], timetable[j + 1] = timetable[j + 1], timetable[j]
    cur_hours = 0
    for i in range(len(timetable)):
        if i < len(timetable) - 1:
            if timetable[i][0] == timetable[i + 1][0] and timetable[i][1] == timetable[i + 1][1] and timetable[i][4] == 1:
                cur_hours += timetable[i+1][3].hour * 60 + timetable[i+1][3].minute - timetable[i][3].hour * 60 - \
                             timetable[i][3].minute
            elif ((timetable[i][0] == timetable[i + 1][0] and timetable[i][1] != timetable[i + 1][1]) or
                  timetable[i][0] != timetable[i + 1][0]) and timetable[i][4] == 1:
                cur_hours += 24*60 - timetable[i][3].hour * 60 - timetable[i][3].minute
                if cur_hours < 480:
                    empls[timetable[i][0]] = True
                cur_hours = 0
            elif timetable[i][0] != timetable[i + 1][0] or (timetable[i][1] != timetable[i + 1][1] and timetable[i][4] == 2):
                if cur_hours < 480:
                    empls[timetable[i][0]] = True
                cur_hours = 0
        elif timetable[i][4] == 1:
            cur_hours += 24 * 60 - timetable[i][3].hour * 60 - timetable[i][3].minute
            if cur_hours < 480:
                empls[timetable[i][0]] = True
            cur_hours = 0
    sum_age = 0
    cnt = 0
    for empl, key in empls.items():
        if key:
            sum_age += calculate_age(employees[empl - 1][2])
            cnt += 1
    if cnt > 0:
        print('Avg age: ', sum_age / cnt)
    else:
        print('None')

#####################################################################################
# Display all departments and the number of employees who have been late at least once
# in the entire accounting history.
def task_three():
    cur = con.cursor()
    cur.execute('SELECT * FROM timetable')
    timetable = cur.fetchall()
    cur.execute('SELECT * FROM employee')
    employees = cur.fetchall()
    deps = dict()
    empls = dict()
    empls_late = dict()
    for employee in employees:
        deps[employee[3]] = 0
        empls[employee[0]] = datetime.time(23, 59)
        empls_late[employee[0]] = 0
    dates = dict()
    for sch in timetable:
        dates[sch[1]] = copy.copy(empls)

    for sch in timetable:
        if sch[3] < dates[sch[1]][sch[0]]:
            dates[sch[1]][sch[0]] = sch[3]
    for dt, els in dates.items():
        for em, time in els.items():
            if time > datetime.time(9, 0):
                empls_late[em] += 1
    for emp, cnt in empls_late.items():
        if cnt > 0:
            deps[employees[emp - 1][3]] += 1
    print('Departments and count of latecomers')
    for title, cnt in deps.items():
        print(title,'-',cnt)


def task_three_sql():
    cur = con.cursor()
    cur.execute('''
    select count(tmp2.em), department
    from (
    	select e.employee_id as em, e.department as e_d
    	from (
    		select employee_id, come_date, min(come_time) as first_entry
    		from timetable
    		where var = 1
    		group by employee_id, come_date
    	) as tmp inner join employee e on e.employee_id = tmp.employee_id
        where first_entry > '9:00'
        group by e.employee_id
    ) as tmp2 right join employee e on tmp2.e_d = e.department
    group by e.department
    ''')
    print('Departments and count of latecomers')
    for row in cur:
        print(row[1], '-', row[0])


if __name__ == '__main__':
    task_one()
    task_two()
    task_three()
    task_three_sql()

con.close()
