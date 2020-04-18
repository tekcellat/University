CC := gcc
CFLAGS := -std=c99 -Wall -Werror
OBJ := count.o read_array.o

ifeq ($(mode), debug)
	CFLAGS += g3
endif

ifeq ($(mode), release)
	CGLAGS += -DNDEBUG -g0
endif

main.exe : $(OBJ) main.o
	$(CC) -o $@ $^
	
test.exe : $(OBJ) test.o
	$(CC) -o $@ $^
	
test.o : test.c *.h
	$(CC) $(CFLAGS) -c $<
	
main.o : main.c *.h
	$(CC) $(CFLAGS) -c $<
	
%.o : %.c %.h
	$(CC) $(CFLAGS) -c $<
	
clean :
	$(RM) *.o *.exe
