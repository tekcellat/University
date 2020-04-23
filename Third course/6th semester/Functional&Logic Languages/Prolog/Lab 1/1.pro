domains
    NAME=symbol
    NUM=string
    AREA=integer
    CITY=string
    STREET=string
    HOUSE=integer

predicates
    likes(symbol,symbol)
    abonent(NAME,NUM)
    abonname(NAME,NUM)
    abonnum(NAME,NUM)
    house(NAME,AREA,CITY,STREET,HOUSE)
    housesAddr(NAME,CITY,STREET,HOUSE)
    housesAREA(NAME,AREA)
    mult(NAME,NUM,CITY)
clauses
    likes(ellen,tennis).
    likes(john,football).
    likes(tom,baseball).
    likes(eric,swimming).
    likes(mark,tennis).
    likes(bill,Activity):-likes (tom, Activity).
    abonent(alex,"1111111").
    abonent(alex,"1112121").
    abonent(ivan,"2222222").
    abonent(petr,"3333333").
    abonent(semen,"444444").
    abonent(evgen,"555555").
    abonent(dima,"6666666").
    abonent(semen,"777777").
    abonent(oleg,"888888").
    abonent(roman,"9999999").

    house(alex,2500,"Moscow","Baker",140).
    house(alex,560,"London","Baker",221).
    house(alex,70,"NY","Baker",14).
    house(ivan,2500,"Moscow","Lyubanka",10).
    house(semen,56,"London","Tsentranly",14).
    house(dima,700,"NY","Tsemntr",221).

    abonname(NAME,NUM):-abonent(NAME,NUM).
    abonnum(NAME,NUM):-abonent(NAME,NUM).
    housesAddr(NAME,CITY,STREET,HOUSE):-house(NAME,_,CITY,STREET,HOUSE).
    housesAREA(NAME,AREA):-house(NAME,AREA,_,_,_).
    mult(NAME,NUM,CITY):-house(NAME,_,CITY,_,_),abonent(NAME,NUM).

goal
    abonname(alex,NUM).
    %housesAddr(alex,CITY,STREET,HOUSE).
    %housesAREA(alex,AREA).
    %mult(alex,NUM,ADDRESS).
    %house(alex,_,ADDRESS),abonent(alex,NUM)
