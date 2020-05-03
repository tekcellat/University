create table timetable
(
    id integer references employees (id),
    date date,
    day_of_week text,
    time time,
    type integer
 );
DROP TABLE timetable;

create table employees
(
    id integer,
    fio text,
    birthday date,
    department text,
    PRIMARY KEY (id)
 );

show datestyle;

set datestyle to 'iso, mdy';

insert into timetable values(1, '12-14-2018', 'Saturday', '9:01', 1), -- changed time here to see the difference
                                                                      -- count_late was giving 1, now 2
                            (1, '12-14-2018', 'Saturday', '9:20', 2),
                            (1, '12-14-2018', 'Saturday', '9:25', 1),
                            (2, '12-14-2018', 'Saturday', '9:05', 1);

drop table timetable;

insert into employees values (1,'Ivanov Ivan Ivanovich','09-25-1990','IT'),
                             (2,'Petrov Petr Petrovich','11-12-1987','Bookkeeping');

CREATE OR REPLACE FUNCTION count_late(date_of_late_arrival date)
RETURNS bigint
AS $$
SELECT COUNT (*)
FROM (
    SELECT id, min(time) as first_entry
    FROM timetable
    WHERE type = 1 AND date = date_of_late_arrival
    GROUP BY id
) tmp
WHERE first_entry > '9:00'
$$ LANGUAGE 'sql';

DROP FUNCTION count_late(date_of_late_arrival date);
SELECT * FROM count_late('2018-12-14');