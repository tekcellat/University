MASM /ZI lr04-2-1.asm,,;
MASM /ZI lr04-2-2.asm,,;
LINK /CO lr04-2-1.obj lr04-2-2.obj ,prog;
del *.obj *.lst *.map