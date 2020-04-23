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
    person("Ivanov", "111-111", address("City-17", "Gordon street", 0, 0)).
    person("Petrov", "001-917", address("St. Petersburg", "Lenina", 24, 42)).
    person("Sidorov", "555-555", address("Los Angeles", "Apple street", 0, 1)).
    person("A", "123-456", address("B", "C avnenue", 13, 14)).
    person("Another", "123-321", address("One", "Good street", 3, 12)).
    person("One", "999-666", address("More", "Pioneer street", 3, 4)).
    person("Not", "987-654", address("Enough", "Bad Fantasy avenue", 9, 9)).
    
    car("Ivanov", "Bugatti", "La Voiture Noire", "Black", 1178000).
    car("Ivanov", "Aston Martin", "Valkyrie", "Grey", 230000).
    car("Petrov", "Lada", "Kalina", "White", 200).
    car("Sidorov", "Ford", "Focus", "Red", 400).
    
    deposit("Ivanov", address("Example", "street", 0, 0), "Sberbank", "0-0-0-0", 999999999).
    deposit("Ivanov", address("Example", "street", 0, 0), "VTB", "0-0-0-1", 1).
    deposit("Ivanov", address("City-17", "Gordon street", 0, 0), "Tinkoff", "0-1-0-1", 987654).
    deposit("Petrov", address("St. Petersburg", "Lenina", 24, 42), "Alfa", "1-2-3-4", 999999999).
    deposit("Sidorov", address("Los Angeles", "Apple street", 0, 1), "Mavrodi", "6-9-6-9", 1).
    
Brand, _).
    by_surname_city(Surname, City, Street, Bank, Number) :- person(Surname, Number, address(City, Street, _, _)), deposit(Surname, address(City, Street, _, _), Bank, _, _).
    person("Another", "123-321", address("One", "Good street", 3, 12)).
    person("One", "999-666", address("More", "Pioneer street", 3, 4)).
    person("Not", "987-654", address("Enough", "Bad Fantasy avenue", 9, 9)).
    
    car("Ivanov", "Bugatti", "La Voiture Noire", "Black", 1178000).
    car("Ivanov", "Aston Martin", "Valkyrie", "Grey", 230000).
    car("Petrov", "Lada", "Kalina", "White", 200).
    car("Sidorov", "Ford", "Focus", "Red", 400).
    
    deposit("Ivanov", address("Example", "street", 0, 0), "Sberbank", "0-0-0-0", 999999999).
    deposit("Ivanov", address("Example", "street", 0, 0), "VTB", "0-0-0-1", 1).
    deposit("Ivanov", address("City-17", "Gordon street", 0, 0), "Tinkoff", "0-1-0-1", 987654).
    deposit("Petrov", address("St. Petersburg", "Lenina", 24, 42), "Alfa", "1-2-3-4", 999999999).
    deposit("Sidorov", address("Los Angeles", "Apple street", 0, 1), "Mavrodi", "6-9-6-9", 1).
    deposit("Another", address("One", "Good street", 3, 12), "Bankname", "10-20-30-40", 40302010).
    
    all_by_phone(Number, Surname, Brand, Price) :- person(Surname, Number, _), car(Surname, Brand, _, _, Price).
    brand_by_phone(Number, Brand) :- all_by_phone(Number, _, Brand, _).
    by_surname_city(Surname, City, Street, Bank, Number) :- person(Surname, Number, address(City, Street, _, _)), deposit(Surname, address(City, Street, _, _), Bank, _, _).

goal
    %all_by_phone("000-000", Surname, Brand, Price).    
    %brand_by_phone("000-000", Brand).
    %by_surname_city("Ivanov", "Example", Street, Bank, Number).


