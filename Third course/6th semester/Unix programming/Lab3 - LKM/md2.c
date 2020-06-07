#include <linux/module.h> 
#include <linux/kernel.h> 
#include <linux/init.h> 

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Hasanzade M.A");

extern char* md1_str_data;
extern int md1_int_data;
extern char* md1_get_str(int num);
extern int md1_factorial(int num);
extern int md1_return_zero(void);

static int __init md2_init(void) {
	printk(KERN_INFO "+md2: Module 2 is loaded.\n");

    	printk(KERN_INFO "+ md2: Export char* from MD1 - %s.\n", md1_str_data);
    	printk(KERN_INFO "+ md2: Export int from MD1 - %d.\n", md1_int_data);

    	printk(KERN_INFO "+ md2: Function 'md1_get_str(1)' from MD1 return %s.\n", md1_get_str(1));
    	printk(KERN_INFO "+ md2: Function 'md1_factorial(5)' from MD1 return %d.\n", md1_factorial(5));
    	printk(KERN_INFO "+ md2: Function 'md1_return_zero' from MD1 return %d.\n", md1_return_zero());
	return 0;
}

static void __exit md2_exit(void) {
	printk(KERN_INFO "+ md2: Module 2 is unloaded.\n");
}

module_init(md2_init);
module_exit(md2_exit);
