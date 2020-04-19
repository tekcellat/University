#include <LPC23xx.H>
#define STB 26 //Port1.26
#define CLK 27 //Port1.27
#define DIO	28 //Port1.28

void delay(unsigned int t) {
//Сбросить таймер
	T0TC = 0x00000000;
//Установить задержку в мс в регистре совпадения MCR
	T0MR0 = t;
//Запустить таймер
	T0TCR = 0x00000001;
//Ожидаем окончания счета
	while (T0TCR&0x1) {};
}

void tm1638_sendbyte(unsigned int x) {
		unsigned int i;
		IODIR1 |= (1<<DIO);//Устанавливаем пин DIO на вывод
		for(i = 0; i < 8; i++)
    {
			IOCLR1=(1<<CLK);//Сигнал CLK устанавливаем в 0
			delay(1);//Задержка 
			if (x&1) 	{IOSET1=(1<<DIO);} //Устанавливаем значение на выходе DIO
			else 			{IOCLR1=(1<<DIO);}
			delay(1);//Задержка
      x  >>= 1;
      IOSET1=(1<<CLK);//Сигнал CLK устанавливаем в 1
      delay(2);			
    }

}

unsigned int tm1638_receivebyte() {
		unsigned int i;
		unsigned int x=0;
		IODIR1 &= ~(1<<DIO);//Устанавливаем пин DIO на ввод
		for(i = 0; i < 32; i++)
    {
			IOCLR1=(1<<CLK);//Сигнал CLK устанавливаем в 0
			delay(1);//Задержка 
			if (IOPIN1&(1<<DIO)) {
				x |= (1<<i);
			}
			delay(1);//Задержка
      IOSET1=(1<<CLK);//Сигнал CLK устанавливаем в 1
      delay(2);			
    }
	return x;
}

void tm1638_sendcmd(unsigned int x)
{
			//Устанавливаем пассивный высокий уровень сигнала STB
			IOSET1=(1<<STB);
			//Устанавливаем пины CLK,DIO,STB на вывод
			IODIR1 = (1<<CLK)|(1<<DIO)|(1<<STB);
			//Устанавливаем активный низкий уровень сигнала STB
			IOCLR1=(1<<STB);
			tm1638_sendbyte(x);
}


void tm1638_setadr(unsigned int adr) {
	   	//Установить адрес регистра LED инидикации
		tm1638_sendcmd(0xC0|adr);	
}

void tm1638_init() {

		unsigned int i;
		//Разрешить работу индикации
		tm1638_sendcmd(0x88);	
		//Установить режим адресации: автоинкремент
		tm1638_sendcmd(0x40);
   	//Установить адрес регистра LED инидикации
		tm1638_setadr(0);
		//Сбросить все 
		for (i=0;i<=0xf;i++)
			tm1638_sendbyte(0);
		//Установить режим адресации: фиксированный
		tm1638_sendcmd(0x44);
}


void Timer0_Init(void){
//Предделитель таймера = 12000
	T0PR = 12000;
//Сбросить счетчик и делитель
	T0TCR = 0x00000002;
//При совпадении останавливаем, сбрасываем таймер
	T0MCR = 0x00000006;
//Регистр совпадения = 1000 (1 Гц)
	T0MR0 = 1000;
}	


int main (void) {

	unsigned int flag, i;

	Timer0_Init(); /* Настроить таймер */	

	tm1638_init();/* Конфигурируем TM1638 */	


	while (1) {          /* Бесконечный цикл */		
			flag = 1;
			// Put all lights off
			tm1638_setadr(1);
			tm1638_sendbyte(0);
			tm1638_setadr(3);
			tm1638_sendbyte(0);
			tm1638_setadr(5);
			tm1638_sendbyte(0);
			tm1638_sendcmd(0x46);
			
			i = tm1638_receivebyte();
		
			while (i != 0)
			{
				tm1638_setadr(1);
				tm1638_sendbyte(1);
				delay(0xfff);
				
				tm1638_setadr(1);
				tm1638_sendbyte(0);
				tm1638_setadr(3);
				tm1638_sendbyte(1);
				delay(0xfff);
				
				tm1638_setadr(3);
				tm1638_sendbyte(0);
				tm1638_setadr(5);
				tm1638_sendbyte(1);
				delay(0xfff);
				
				tm1638_setadr(5);
				tm1638_sendbyte(0);
				
				tm1638_sendcmd(0x46);
			}
	}
}
