#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/interrupt.h>
#include <linux/sched.h>

struct tasklet_struct *tasklet;
int dev_id,scancode, irq = 1;

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Hasanzade M.A.");

#define KBD_DATA_REG 0x60
#define kbd_read_input() inb(KBD_DATA_REG)

void tasklet_function(unsigned long data)
{
	scancode = kbd_read_input();
	if (scancode < 103) {
		printk(KERN_INFO "tasklet: state: %ld, count: %d, data: %ld\n",
         	tasklet->state, tasklet->count, tasklet->data);
		printk(KERN_INFO "tasklet: Keycode %d\n", scancode);
	}
  	
  return;
}

static irqreturn_t my_interrupt(int irq, void *dev_id)
{
  	tasklet_schedule(tasklet);
		
	
  	return IRQ_HANDLED;
}

static int __init module_tasklet_init(void)
{
	
	
	if (request_irq(irq, my_interrupt, IRQF_SHARED, "my_interrupt", &dev_id))
		return -1;

	
  	tasklet = vmalloc(sizeof(struct tasklet_struct));
  
	
	tasklet_init(tasklet, tasklet_function, 0);
	
	printk(KERN_INFO "tasklet module is loaded.\n");
  	return 0;
}

static void __exit module_tasklet_exit(void)
{
  tasklet_kill(tasklet);
  vfree(tasklet);
  free_irq(irq, &dev_id);
  printk(KERN_INFO "tasklet module is unloaded.\n");
  return;
}

module_init(module_tasklet_init);
module_exit(module_tasklet_exit);
