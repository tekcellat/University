use tempdb;
go

if object_id('dbo.Emp', 'U') is not null
	drop table dbo.Emp;
go

create table Emp
(
	id_emp int primary key identity(1,1),
	name varchar(50) not null,
	birthday date not null,
	department varchar(50)
);
go

if object_id('dbo.InOutEmp', 'U') is not null
	drop table dbo.InOutEmp;
go

create table InOutEmp
(
	id_emp int not null,
	date_ date not null,
	weekday_ varchar(20) check (weekday_ in ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')),
	time_ time not null,
	type_ int check (type_ in (1,2)),
	primary key(id_emp, date_, time_),
	foreign key(id_emp) references Emp(id_emp)
);
go

insert into dbo.Emp(name, birthday, department)
values  ('Ivanov Ivan Ivanovich', convert(date, '09-25-1990'), 'IT'),
		('Petrov Petr Petrovich', convert(date, '11-12-1987'), 'Marketing'),
		('Nguyen Ngoc Hai', convert(date, '11-23-1997'), 'IT'),
		('Nguyen Duc Hien', convert(date, '03-12-1998'), 'Something')
go

insert into dbo.InOutEmp(id_emp, date_, weekday_, time_, type_)
values	(1, convert(date, '12-14-2018'), datename(weekday, '12-14-2018'), convert(time, '9:00'), 1),
		(1, convert(date, '12-14-2018'), datename(weekday, '12-14-2018'), convert(time, '9:20'), 2),
		(1, convert(date, '12-14-2018'), datename(weekday, '12-14-2018'), convert(time, '9:25'), 1),
		(2, convert(date, '12-14-2018'), datename(weekday, '12-14-2018'), convert(time, '9:05'), 1),
		(3, convert(date, '12-14-2018'), datename(weekday, '12-14-2018'), convert(time, '7:59'), 1),
		(3, convert(date, '12-14-2018'), datename(weekday, '12-14-2018'), convert(time, '8:01'), 2),
		(4, convert(date, '12-15-2018'), datename(weekday, '12-15-2018'), convert(time, '12:01'), 1),
		(4, convert(date, '12-15-2018'), datename(weekday, '12-15-2018'), convert(time, '6:12'), 1),
		(2, convert(date, '12-15-2018'), datename(weekday, '12-15-2018'), convert(time, '7:30'), 1),
		(2, convert(date, '12-15-2018'), datename(weekday, '12-15-2018'), convert(time, '9:05'), 2),
		(1, convert(date, '12-21-2019'), datename(weekday, '12-21-2019'), convert(time, '9:00'), 1),
		(3, convert(date, '12-22-2019'), datename(weekday, '12-22-2019'), convert(time, '9:00'), 1),
		(3, convert(date, '12-21-2019'), datename(weekday, '12-21-2019'), convert(time, '9:00'), 1),
		(3, convert(date, '12-20-2019'), datename(weekday, '12-20-2019'), convert(time, '9:00'), 1),
		(3, convert(date, '12-19-2019'), datename(weekday, '12-19-2019'), convert(time, '9:00'), 1)
go

-- Methode 1: Create function
create function AvgAge (@department varchar(50))
returns float
begin
	declare @ret float;
	select @ret = AVG(datepart(year, getdate()) - datepart(year, temp.birthday))
	from
	(
		select I.time_, E.birthday, I.date_
		from dbo.InOutEmp I join dbo.Emp E on I.id_emp = E.id_emp
		where E.department = @department
	) as temp
	where cast(date_ as date) = cast(getdate() as date) and temp.time_ > convert(time, '8:00');

	return @ret;
end
go

select dbo.AvgAge('IT') as 'Avg age of late staff'
go

-- Method 2: Create Aggregate by CLR
create assembly SQLServerUDF 
from 'D:\Education\BMSTU\5th Semester\Database\_LAB\RK3\_RK3\Create aggregate\Task1_Aggregate\Task1_Aggregate\bin\Debug\Task1_Aggregate.dll' 
with permission_set = safe
go

create aggregate AvgAge (@input int) 
returns int
	external name SQLServerUDF.AvgAge;
go

select dbo.AvgAge(datepart(year, getdate()) - datepart(year, temp.birthday)) as 'Avg age of late staff'
from
(
	select I.time_, E.birthday, I.date_
	from dbo.InOutEmp I join dbo.Emp E on I.id_emp = E.id_emp
	where E.department = 'IT'
) as temp
where cast(date_ as date) = cast('12/21/2019' as date) and temp.time_ > convert(time, '8:00')
