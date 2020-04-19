public p3
Code    SEGMENT WORD 'CODE'
        ASSUME  CS:Code
p3:
        mov   AX,'3'                ;загрузка в AX адреса сегмента данных
        ret
Code    ENDS
        END  
