#include <syslog.h>
#include <fcntl.h>
#include <sys/resource.h>

#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include <arpa/inet.h>
#include <string.h>
#include <stdarg.h>
#include <errno.h>


const char demonname[64] = "sheytan";
#define LOCKFILE "/var/run/sheytan.pid"

int sock;				//файловый дескриптор сокета, в который пишем репорты
struct sockaddr_in addr;	//адрес, связанный с этим сокетом

//печать информации путем посылания через сокет
void func_pr(const char* format, ...){
	char message[512];
	va_list ap;
	va_start( ap, format );
	vsnprintf( message, 512, format, ap );
	va_end( ap );
	//открываем сокет
	sock = socket( AF_INET, SOCK_DGRAM, IPPROTO_UDP );
	
	//посылаем через сокет, сообщение, длиной, без флагов,
	//по адресу, определенного размера
	sendto( sock, message, strlen(message), 0, (struct sockaddr*) &addr, sizeof(addr) );
	
	close( sock ); //закрываем сокет


}

/*возвращает в основную функцию:
сигнал завершиться предку (1),
ошибку демонизации(-1),
успешную демонизацию (0)*/

int demonize(const char *process_name){
	int i;
		
	func_pr( "fork" );
	/*выводим демона в отдельный процесс чтобы командная оболочка думала, что команда была выполнена 
	 пока не лидер группы позволяет вызвать setsid*/
	int pid = fork();
	if ( pid < 0 ){
		func_pr( "ERROR: fork" );
		return -1;
	}
	if ( pid != 0 ) return 1; //parent

	
	//запускаем его в новой сессии - становится лидером сессии,
	//лидером группы и лишается управляющего терминала
	setsid();
	
	//игнорируем сигнал потери терминала
	struct sigaction sa; //будем выполнять действие над сигналом:
	sa.sa_handler = SIG_IGN; //игнорировать сигнал
	sigemptyset( &sa.sa_mask ); //сбрасываем маску
	sa.sa_flags = 0;
	
	func_pr( "sigaction" );
	if ( sigaction(SIGHUP, &sa, NULL) < 0 ){
		func_pr( "ERROR: can't ignore SIGHUP" );
		return -1;
	}
	
	func_pr( "changing dir" );
	//меняем директорию на / чтобы при необходимости можно было
	//отмонтировать файловую систему, из которой запустился демон
	if ( chdir("/") < 0 ){
		func_pr( "ERROR: can't change directory" );
		return -1;
	}

	func_pr( "umask and getrlimit\n" );
	umask(0); //обнуляем старую маску доступа к файлам, чтобы она *
	//маска наследуется и может маскировать биты прав доступа (запись, чтение)
	//не привела к неопределенному поведению
	
	//получаем максимальное количество дескрипторов
	struct rlimit rl;
	if ( getrlimit(RLIMIT_NOFILE, &rl) < 0 ) {
		func_pr( "ERROR: couldn't get max number of fd" );
		return -1;
	}
	if ( rl.rlim_max == RLIM_INFINITY ) rl.rlim_max = 1024;
	
	//проходим по всем дескрипторам и закрываем их - демон не должен
	//взаимодействовать с дескрипторами предка
	for (i = 0; i < rl.rlim_max; ++i){
		if ( i != sock ) //кроме лог-сокета, чтобы было куда писать
			close(i);
	}
	func_pr( "\n" );
	
	//открываем первые три файловых дескриптора, чтобы библиотечные
	//функции чтения\записи на стандартный ввод\вывод не оказывали
	//влияния
	int fd0, fd1, fd2;
	fd0 = open( "/dev/null", O_RDWR );
	fd1 = dup(0); //дублируем дескрипторы
	fd2 = dup(0);
	
	//получаем доступ к записи в /var/log/syslog
	openlog( process_name, LOG_CONS, LOG_DAEMON );
	if ( fd0 != 0 || fd1 != 1 || fd2 != 2){
		func_pr( "ERROR: Incorrect file descriptors 0,1,2" );
		syslog( LOG_ERR, "incorrect fd: %d %d %d", fd0, fd1, fd2 );
		return -1;
	}
	func_pr( "Demonizing finished." );
	return 0;
}

//обеспечивает запуск демона в единственном экземпляре
//завершает выполнение, если не может открыть файл,
//возвращает 1, если файл уже "занят",
//0, если запуск возможен
int already_running(void){
#define BUFLEN 8
	int fd;
	char buf[BUFLEN];
	
	fd = open( LOCKFILE, O_RDWR|O_CREAT, S_IRUSR|S_IWUSR|S_IRGRP|S_IROTH );
	if (fd < 0){
		func_pr( "ERROR: unable to open %s: %s", LOCKFILE, strerror(errno) );
		syslog( LOG_ERR, "unable to open %s: %s", LOCKFILE, strerror(errno) );
		exit(1);
	}
	
	flock( fd, LOCK_EX|LOCK_NB );
	if ( errno == EWOULDBLOCK ){
		func_pr( ">>> Can't lock file %s: %s\n>>> Is demon already launched?", LOCKFILE, strerror(errno) );
		syslog(LOG_ERR, "unable to lock %s: %s", LOCKFILE, strerror(errno));
		close(fd);
		return 1;
	}
	
	func_pr( "%d - Successfully locked the file.", getpid() );
	snprintf( buf, BUFLEN, "%d", getpid() );
	write( fd, buf, strlen(buf) );
	return 0;
}

void demonFunc(){
	func_pr( "(%d) timemark...", getpid() );
	syslog( LOG_INFO, "(%d) timemark...\n", getpid() );
	sleep(3); 
}

int main(void)
{
	addr.sin_addr.s_addr = 0x0100007f;
	addr.sin_port = htons(7777);
	addr.sin_family = AF_INET;
	
	
	printf( "Demonize...\n" );
	int d = demonize( demonname );
	if ( d > 0 ){
		func_pr( "Parent: finished successfully" );
		return 0;
	}
	else if ( d < 0 ){
		func_pr( "Parent: something went wrong!" );
		return 1;
	}
	
	if ( already_running() ) return 1;
	func_pr( "Successfully demonized." );
	
	while ( 1 ) {demonFunc();}
}
