public p2
Code    SEGMENT WORD 'CODE'
        ASSUME  CS:Code
p2:
        mov   AX,'2'                ;загрузка в AX адреса сегмента данных
        ret
Code    ENDS
        END  
