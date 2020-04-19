using System;
using System.Data;
using System.Linq;
using System.Data.SqlClient;

namespace _RK3
{
    class Program
    {
        static readonly string connectionString = @"server = localhost; Initial Catalog = tempdb; Integrated Security = True";
        static SqlConnection connection = null;

        static void Main(string[] args)
        {
            connection = new SqlConnection(connectionString);
            connection.Open();

            int option;

            do
            {
                Console.WriteLine("Menu");
                Console.WriteLine("1. Task 1 - SQL Command");
                Console.WriteLine("2. Task 1 - LINQ");
                Console.WriteLine("3. Task 2 - SQL Command");
                Console.WriteLine("4. Task 2 - LINQ");
                Console.WriteLine("5. Task 3 - SQL Command");
                Console.WriteLine("6. Task 3 - LINQ");
                Console.WriteLine("7. Exit");
                Console.Write("Choose option: ");
                option = Int32.Parse(Console.ReadLine());

                switch (option)
                {
                    case 1:
                        {
                            Task1_SQLCommand();
                            break;
                        }
                    case 2:
                        {
                            Task1_LINQ();
                            break;
                        }
                    case 3:
                        {
                            Task2_SQLCommand();
                            break;
                        }
                    case 4:
                        {
                            Task2_LINQ();
                            break;
                        }
                    case 5:
                        {
                            Task3_SQLCommand();
                            break;
                        }
                    case 6:
                        {
                            Task3_LINQ();
                            break;
                        }
                    case 7:
                        {
                            break;
                        }
                    default:
                        {
                            Console.WriteLine("Invalid option");
                            break;
                        }
                }

                Console.WriteLine();
            }
            while (option != 7);

            connection.Close();
        }

        static void Task1_SQLCommand()
        {
            string query = @"select distinct department
                            from dbo.Emp
                            where id_emp in (
	                            select id_emp
	                            from(
		                            select id_emp, count(distinct date_) as nlate
		                            from dbo.InOutEmp
		                            where type_ = 1 and time_ > convert(time, '8:00') and date_ > DATEADD(day, -10, GETDATE())
		                            group by id_emp
	                            ) as temp
	                            where temp.nlate >= 10
                            )";

            SqlCommand cmd = new SqlCommand(query, connection);

            using (SqlDataReader reader = cmd.ExecuteReader())
            {                
                while (reader.Read())
                    Console.WriteLine($"{reader[0]}");
            }

            cmd.Dispose();
        }

        static void Task1_LINQ()
        {
            SqlCommand cmd = new SqlCommand("select * from dbo.InOutEmp", connection);
            var InOutEmp = new DataTable();
            InOutEmp.Load(cmd.ExecuteReader());
            cmd = new SqlCommand("select * from dbo.Emp", connection);
            var Emp = new DataTable();
            Emp.Load(cmd.ExecuteReader());

            var res = (
                from temp in InOutEmp.AsEnumerable()
                    .Where(
                        row => (int)row["type_"] == 1 &&
                        DateTime.Compare(DateTime.Parse(row["time_"].ToString()), DateTime.Parse("8:00")) == 1 &&
                        (DateTime.Now - DateTime.Parse(row["date_"].ToString())).Days < 10
                    )
                    .GroupBy(
                        id => id["id_emp"],  // Key
                        dates => dates["date_"],
                        (id, dates) => new
                        {
                            Id = id,
                            NumLate = dates.Distinct().Count()
                        }
                    )
                    .Where(row => row.NumLate >= 10)
                from temp1 in Emp.AsEnumerable()
                    .Where(row => (int)row["id_emp"] == (int)temp.Id)
                select temp1
                )
                .GroupBy(row => row["department"]);                

            foreach (var row in res)            
                Console.WriteLine($"{row.Key}");            
        }

        static void Task2_SQLCommand()
        {
            string query = @"   select top 1 id_emp, max(time_) as out_time
                                from dbo.InOutEmp
                                where   type_ = 2 and time_ between convert(time, '9:00') and 
                                        convert(time, '21:00') and 
                                        cast(date_ as date) = cast(GETDATE() as date)
                                group by id_emp
                            ";

            SqlCommand cmd = new SqlCommand(query, connection);

            using (SqlDataReader reader = cmd.ExecuteReader())
            {
                while (reader.Read())
                    Console.WriteLine($"{reader[0]} {reader[1]}");
            }

            cmd.Dispose();
        }

        static void Task2_LINQ()
        {
            SqlCommand cmd = new SqlCommand("select * from dbo.InOutEmp", connection);
            var InOutEmp = new DataTable();
            InOutEmp.Load(cmd.ExecuteReader());

            var res = InOutEmp.AsEnumerable()
                .Where(
                    row => (int)row["type_"] == 2 &&
                    DateTime.Compare(DateTime.Parse(row["time_"].ToString()), DateTime.Parse("9:00")) == 1 &&
                    DateTime.Compare(DateTime.Parse(row["time_"].ToString()), DateTime.Parse("21:00")) == -1 &&
                    (DateTime.Now - DateTime.Parse(row["date_"].ToString())).Days == 0
                )
                .GroupBy(
                    id => id["id_emp"],
                    time => time["time_"],
                    (id, time) => new
                    {
                        Id = id,
                        Time = time.Max()
                    }
                )
                .OrderBy(time => time.Time)
                .First();

            Console.WriteLine($"{res.Id} {res.Time}");
        }

        static void Task3_SQLCommand()
        {
            string query = @"
                            select q1.department from
                            (
	                            select department, count(*) as c1
	                            from dbo.Emp
	                            where id_emp in 
	                            (
		                            select id_emp
		                            from(
			                            select id_emp, min(t1) t2
			                            from (
				                            select id_emp, date_, min(time_) as t1
				                            from dbo.InOutEmp
				                            where type_ = 1
				                            group by id_emp, date_

			                            ) as temp
			                            group by id_emp
		                            )as temp
		                            where temp.t2 < convert(time, '8:00')
	                            )	
	                            group by department
                            ) q1 
                            join
                            (
	                            select department, count(*) as c2
	                            from dbo.Emp 
	                            group by department
                            ) q2
                            on q1.department = q2.department and q1.c1 = q2.c2                            
                            ";
            SqlCommand cmd = new SqlCommand(query, connection);

            using (SqlDataReader reader = cmd.ExecuteReader())
            {
                while (reader.Read())
                    Console.WriteLine($"{reader[0]}");
            }

            cmd.Dispose();
        }

        static void Task3_LINQ()
        {
            SqlCommand cmd = new SqlCommand("select * from dbo.InOutEmp", connection);
            var InOutEmp = new DataTable();
            InOutEmp.Load(cmd.ExecuteReader());
            cmd = new SqlCommand("select * from dbo.Emp", connection);
            var Emp = new DataTable();
            Emp.Load(cmd.ExecuteReader());

            var res = (
                from temp in InOutEmp.AsEnumerable()
                    .Where(row => (int)row["type_"] == 1)
                    .GroupBy(
                        id => id["id_emp"],
                        time => time["time_"],
                        (id, time) => new
                        {
                            Id = id,
                            Time = time.Min()
                        }
                    )
                    .Where(
                        row => DateTime.Compare(DateTime.Parse(row.Time.ToString()), DateTime.Parse("8:00")) == -1
                    )
                from temp1 in Emp.AsEnumerable()
                    .Where(row => (int)row["id_emp"] == (int)temp.Id)
                select temp1               
                );

            var res1 = (
                from temp in res
                from temp1 in Emp.AsEnumerable()
                    .Where(
                        row => row["id_emp"].ToString() == temp["id_emp"].ToString()
                    )
                select temp1
            )
            .GroupBy(
                dep => dep["department"],
                num => num["department"],
                (dep, num) => new
                {
                    Department = dep,
                    Num = num.Count()
                }
            );

            var res2 = Emp.AsEnumerable()
            .GroupBy(
                dep => dep["department"],
                num => num["department"],
                (dep, num) => new
                {
                    Department = dep,
                    Num = num.Count()
                }
            );

            var final_res =
                (
                    from temp in res1
                    from temp1 in res2
                    .Where(row => row.Department == temp.Department && row.Num == temp.Num)
                    select temp
                );

            foreach (var row in final_res)
            {
                Console.WriteLine($"{row.Department}");
            }
        }

    }
}
