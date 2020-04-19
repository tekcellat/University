@echo on
MASM.EXE /ZI laba.asm,,,;
MASM.EXE /ZI laba-1.asm,,,;
link.exe /CO LABA.OBJ,,,;

DEL *.OBJ *.LST *.CRF *.MAP

CV.EXE LABA.EXE