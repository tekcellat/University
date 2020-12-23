#include <sqlite3.h>
#include <stdio.h>

/*
 * Script for create admin and usual user.
 */
int callback(void *, int, char **, char **);

sqlite3 * openUsersDB();
void createUsersTable(sqlite3 *db);

int main(void) {
    
	sqlite3 *db = openUsersDB();
	createUsersTable(db);    
    sqlite3_close(db);
    
    return 0;
}

sqlite3 * openUsersDB() {
	sqlite3 *db;
    char *err_msg = 0;
    
    int rc = sqlite3_open("users.db", &db);
    
    if (rc != SQLITE_OK) {
        
        fprintf(stderr, "Cannot open database: %s\n", 
                sqlite3_errmsg(db));
        sqlite3_close(db);
        
        return 0;
    }

    return db;
}

void createUsersTable(sqlite3 *db) {
	int rc;
    char *err_msg = 0;    
	 char *sql = "DROP TABLE IF EXISTS Users;" 
	 			 "CREATE TABLE Users(Name TEXT PRIMARY KEY, Password TEXT, Right INTEGER);"
                 "INSERT INTO Users VALUES('admin', 'admin', 0);"
                 "INSERT INTO Users VALUES('user', 'user', 1)";

    rc = sqlite3_exec(db, sql, 0, 0, &err_msg);

        if (rc != SQLITE_OK ) {
        
        fprintf(stderr, "SQL error: %s\n", err_msg);
        
        sqlite3_free(err_msg);        
        sqlite3_close(db);
        
        return;
    } 
}
