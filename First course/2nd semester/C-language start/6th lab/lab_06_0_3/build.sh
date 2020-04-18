gcc -std=c99 -Wall -Werror -c main.c
gcc -std=c99 -Wall -Werror -c count.c
gcc -std=c99 -Wall -Werror -c read_array.c
gcc -o main.exe main.c read_array.c count.c