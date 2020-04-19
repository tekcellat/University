public p5
Code    SEGMENT WORD 'CODE'
        ASSUME  CS:Code
p5:
        mov   AX,'5'                ;загрузка в AX адреса сегмента данных
        ret
Code    ENDS
        END  
