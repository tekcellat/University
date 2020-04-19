@echo on


MASM /Zi lab2.asm,,,;

LINK /CO lab2.OBJ,,;

del *.OBJ *.LST *.CRF *.MAP