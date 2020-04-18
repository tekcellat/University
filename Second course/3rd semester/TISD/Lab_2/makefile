CC := gcc
CFLAGS := -std=c99 -Wall -Werror -ggdb

main.exe : main.o file_handling.o operations.o sort.o
	$(CC) -o $@ $^
	
main.o : main.c struct.h file_handling.h operations.h sort.h
	$(CC) $(CFLAGS) -c $<
	
file_handling.o : file_handling.c file_handling.h struct.h operations.h
	$(CC) $(CFLAGS) -c $<
	
%.o : %.c %.h struct.h
	$(CC) $(CFLAGS) -c $<
	
clean :
	$(RM) *.o *.exe
