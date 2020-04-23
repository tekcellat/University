domains
   surname, number, city, street, brand, model, color, bank, account = symbol.
   price, money = integer. % thousand
   address_t = address(city, street, integer, integer).

predicates
    person(surname, number, address_t).
    car(surname, brand, model, color, price).
    deposit(surname, address_t, bank, account, money).
    all_by_phone(number, surname, brand, price).
    brand_by_phone(number, brand).
    by_surname_city(surname, city, street, bank, number).

clauses
    person("Ivanov", "000-000", address("Example", "street", 0, 0)).
    person("Petrov", "001-917", address("St. Petersburg", "Lenina", 24, 42)).
    person("Sidorov", "555-555", address("Los Angeles", "Apple street", 0, 1)).
    person("Krueger ", "013-666", address("Springwood", "Elm street", 13, 13)).
    person("A", "123-456", address("B", "C avnenue", 13, 14)).
    person("Another", "123-321", address("One", "Good street", 3, 12)).
    person("One", "999-666", address("More", "Pioneer street", 3, 4)).
    person("Not", "987-654", address("Enough", "Bad Fantasy avenue", 9, 9)).    
    car("Ivanov", "Bugatti", "La Voiture Noire", "Black", 1178000).
    car("Petrov", "Lada", "Kalina", "White", 200).
    car("Sidorov", "Lada", "Kalina", "White", 200).
    car("Noname", "Ford", "Focus", "Red", 400).    
    deposit("Ivanov", "Sberbank", "0-0-0-0", 999999999).
    deposit("Ivanov", "VTB", "0-0-0-1", 1).
    deposit("Petrov", "Alfa", "1-2-3-4", 999999999).
    deposit("Sidorov", "Mavrodi", "6-9-6-9", 1).
    deposit("Another", "Bankname", "10-20-30-40", 40302010).    
    person_by_car(Brand, Color, Surname, Number, Bank) :- car(Surname, Brand, _, Color, _), person(Surname, Number, _), deposit(Surname, Bank, _, _).

goal
    %person_by_car("Bugatti", "Black", Surname, Number, Bank).
    %person_by_car("Lada", "White", Surname, Number, Bank).
    %person_by_car("Ford", "Red", Surname, Number, Bank).

