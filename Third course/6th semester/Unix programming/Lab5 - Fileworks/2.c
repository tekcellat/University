#include <fcntl.h>
int main(){
    char c;
    // have kernel open for two connection to our file
    int fd1 = open("alphabet.txt",O_RDONLY);
    int fd2 = open("alphabet.txt",O_RDONLY);
    int break_flag = 1;
    // read a char & write it alternatingly from connections fs1 & fd2
    while(break_flag){
        if (read(fd1,&c,1)!= 1)
            break_flag = 0;
        write(1,&c,1);

        if (read(fd2,&c,1)!= 1)
            break_flag = 0;
        write(1,&c,1);
    }
    return 0;
}
