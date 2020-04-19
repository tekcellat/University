@echo on
MASM.EXE /ZI laba.asm,,,;
link.exe /CO LABA.OBJ,,,;

DEL *.OBJ *.LST *.CRF *.MAP

CV.EXE LABA.EXE