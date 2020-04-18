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
	
main.o : main.c *.h
	$(CC) -o $@ $^
	
%.o : %.c %.h
	$(CC) $(CFLAGS) -c $<
	
clean :
	$(RM) *.o *.exe
