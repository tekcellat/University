CC := gcc
CFLAGS := -std=c99 -Wall -Werror -ggdb
OBJ := main.o array.o list.o request.o

main.exe : $(OBJ)
	$(CC) -o $@ $^
	
%.o : %.c *.h
	$(CC) $(CFLAGS) -c $<
	
clean :
	$(RM) *.o *.exe