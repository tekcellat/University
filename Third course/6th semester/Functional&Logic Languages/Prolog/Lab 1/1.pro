predicates
   student(symbol, symbol, symbol, symbol, real, symbol).
   group(symbol, symbol).
   district(symbol, symbol).
   grantL(symbol).
clauses
   student(ivanova, sophia, iu767, zelenograd, 4.5, no).
   student(krotova, alexandra, iu767, izmaylovo, 4.75, no).
   student(vodova, kristina, iu767, izmaylovo, 3.75, yes).
   student(yegova, natalya, iu767, otradnoye, 4, no).
   student(kruqlova, anna, iu767, otradnoye, 3.0, no).
   student(ivanov, ivan, iu767, balashiha, 3.25, no).
   student(kruqlov, georgiy, iu767, izmaylovo, 5.0, no).
   student(vodov, sanya, iu767, otradnoye, 3.25, yes).

   group(Sur, Group) :-
      student(Sur, _, Group, _, _, _).
   district(Surname, District) :-
      student(Surname, _, _, District, _, _).
   grantL(Surname) :-
      student(Surname, _, _, _, Mean, _),
       Mean>=4.
   grantL(Surname) :-
      student(Surname, _, _, _, _, Info),
      Info=yes.
goal
/* --- part1 --- */
% group (Sur, iu767).
% district (Sur, izmaylovo).
% grantL(Sur).
