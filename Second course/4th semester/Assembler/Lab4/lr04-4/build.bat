MASM /ZI lr04-4-1.asm,,;
MASM /ZI lr04-4-2.asm,,;
LINK /CO lr04-4-1.obj lr04-4-2.obj ,prog;
del *.obj *.lst *.map