MASM /ZI lr04-1-1.asm,,;
MASM /ZI lr04-1-2.asm,,;
LINK /CO lr04-1-1.obj lr04-1-2.obj ,prog;
del *.obj *.lst *.map