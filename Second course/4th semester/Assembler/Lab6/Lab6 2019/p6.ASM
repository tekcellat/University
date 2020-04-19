public p6
Code    SEGMENT WORD 'CODE'
        ASSUME  CS:Code
p6:
        mov   AX,'6'                ;загрузка в AX адреса сегмента данных
        ret
Code    ENDS
        END  
