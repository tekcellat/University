public p4
Code    SEGMENT WORD 'CODE'
        ASSUME  CS:Code
p4:
        mov   AX,'4'                ;загрузка в AX адреса сегмента данных
        ret
Code    ENDS
        END  
