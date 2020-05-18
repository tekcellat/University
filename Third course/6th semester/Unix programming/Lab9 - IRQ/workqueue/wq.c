#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/interrupt.h>
#include <linux/workqueue.h>


MODULE_LICENSE("GPL");
MODULE_AUTHOR("Hasanzade M.A.");

int irq = 1;
int dev_id,scancode;

struct workqueue_struct *que;
struct work_struct *work;

#define KBD_DATA_REG 0x60
#define kbd_read_input() inb(KBD_DATA_REG)

void wq_func(struct work_struct *work) {
	scancode = kbd_read_input();
	if (scancode < 103)
		printk("wq_lab: Keycode %d\n", scancode);
}

static irqreturn_t irq_handler(int irq, void *dev_id) {
	//Планирование на выполнение	
	queue_work(que, work);
	return IRQ_HANDLED;
}

static int __init load_module(void) {
	
	//irq— номер линии запрашиваемого прерывания;
	//handler— указатель на функцию-обработчик типа irqreturn_t;
	//flags- битовая маска опций, связанная с управлением прерыванием;
			//IRQF_SHARED— разрешить разделение (совместное использование) линии IRQ с другими PCI устройствами;
	//name— символьная строка, используемая в /proc/interrupts для отображения владельца прерывания;
	//dev— указатель на уникальный идентификатор устройства на линии IRQ, 
		//для не разделяемых прерываний (например, шины ISA) может указываться NULL.

	int res = request_irq(irq, irq_handler, IRQF_SHARED, "wq_lab", &dev_id);
	if (res < 0) {
		printk(KERN_ERR "wq_lab: Couldn't register interrupt handler!\n");
		return res;
	}


	que = create_workqueue("my_wq");
	if (!que) {
		printk(KERN_ERR "wq_lab: Coulnd't create queue!\n");
		return -1;
	}

	
	work =vmalloc(sizeof(struct work_struct));

	if (!work) {
		printk(KERN_ERR "wq_lab: Can't allocate memory for work!\n");
		return -1;
	}
	//wq_func -функция обработчик
	INIT_WORK(work, wq_func);

	printk(KERN_INFO "wq: Module loaded!\n");
	return 0;
}

static void __exit exit_module(void) {
	free_irq(irq, &dev_id);
	flush_workqueue(que);
	destroy_workqueue(que);
	vfree(work);
	printk(KERN_INFO "wq_lab: Module unloaded!\n");
}

module_init(load_module);
module_exit(exit_module);
