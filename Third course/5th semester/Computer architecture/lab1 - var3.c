#include <LPC23xx.H>             


void delay(void) {
	unsigned int i;
	for (i=0;i<0xfffff;i++){}
}

int main (void) {  
  PINSEL3 	= 0x00000000;
  IODIR1 = 0x1C000000; 
  IOSET1 = 1<<26; 
  	
  while (1) {
    if ((IOPIN1 &(1<<29))) {
			delay();
			IOCLR1 = 1<<26;
			IOSET1 = (1<<27) | (1<<28);
			delay();
			IOCLR1 = (1<<27) | (1<<28);
			IOSET1 = 1<<26;
		} 
	}
}

