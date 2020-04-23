//LKM
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/proc_fs.h>
#include <linux/string.h>
#include <linux/vmalloc.h>
#include <linux/uaccess.h>

MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Message/text Input/Output Kernel Module");
MODULE_AUTHOR("Hasanzade M.A.");

#define MAX_LENGTH PAGE_SIZE

static char* storage;
static int index;
static int next;
static struct proc_dir_entry *proc_entry;
static struct proc_dir_entry *proc_slink;
static struct proc_dir_entry *proc_dir;

ssize_t storage_write(struct file *filp, const char __user *buff,
                        size_t len, loff_t *data) {
    int space_available = (MAX_LENGTH-index)+1;

    if (len > space_available) {
        printk(KERN_INFO "storage: Storage is full!\n");
        return -ENOSPC;
    }

    if (copy_from_user(&storage[index], buff, len)) 
        return -ENOSPC;

    index += len;
    storage[index-1] = 0;
    return len;
}

ssize_t storage_read(struct file *filp, char __user *buffer, size_t count, loff_t *off) {
    int len;

    if (*off > 0 || index == 0) 
        return 0;

    if (next >= index)
        next = 0;

    len = copy_to_user(buffer, &storage[next], count);
    next += len;
    *off += len;
    return len;
}


static const struct file_operations proc_file_fops = {
 .owner = THIS_MODULE,
 .write  = storage_write,
 .read  = storage_read,
};

static int __init my_module_init(void) {
    int ret = 0;

    storage = (char *)vmalloc(MAX_LENGTH);

    if (!storage) 
        ret = -ENOMEM;
    else {
        memset(storage, 0, MAX_LENGTH); 
        proc_dir = proc_mkdir("directory", NULL);
        proc_entry = proc_create("storage", 0644, proc_dir, &proc_file_fops); 
        proc_slink = proc_symlink("sym_to_storage", proc_dir, "/proc/directory/storage");

        if (proc_entry == NULL) {
            ret = -ENOMEM;
            vfree(storage);
            printk(KERN_INFO "storage: Couldn't create proc entry\n");
        }
        else {
            index = 0;
            next = 0;
            printk(KERN_INFO "storage: Module loaded.\n");
        }
    }

    return ret;
}

static void __exit my_module_cleanup(void) {
    remove_proc_entry("storage", NULL);
    remove_proc_entry("directory", NULL);
    remove_proc_entry("sym_to_storage", NULL);
    if (storage)
        vfree(storage);

    printk(KERN_INFO "storage: Module exited.\n");
}

module_init(my_module_init);
module_exit(my_module_cleanup);

