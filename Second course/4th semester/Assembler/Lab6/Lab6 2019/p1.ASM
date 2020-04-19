public p1
Code    SEGMENT WORD 'CODE'
        ASSUME  CS:Code
p1:
        mov   AX,'1'                ;загрузка в AX адреса сегмента данных
        ret
Code    ENDS
        END  
