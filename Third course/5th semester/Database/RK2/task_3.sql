

CREATE OR REPLACE PROCEDURE all_tables(databasename text, tablename text) AS
$$
    declare r record;
    begin
        for r in select * from information_schema.tables WHERE table_catalog = databasename AND table_name = tablename
        loop
            raise info '%', r;
        end loop;
    end;
$$ language plpgsql;

call all_tables('rk2', 'cooperator');