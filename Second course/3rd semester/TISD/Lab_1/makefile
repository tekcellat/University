CC := gcc
CFLAGS := -std=c99 -Wall -Werror

main.exe : main.o read_number.o multiply.o print_number.o
	$(CC) -o $@ $^

main.o : main.c
	$(CC) $(CFLAGS) -c main.c
    
read_number.o : read_number.c read_number.h
	$(CC) $(CFLAGS) -c $<

multiply.o : multiply.c multiply.h
	$(CC) $(CFLAGS) -c $<
    
print_number.o : print_number.c print_number.h
	$(CC) $(CFLAGS) -c $<

clean :
	$(RM) *.o *.exe