# CompLog
Repository for the Computer Logic course. Building a compiler from scratch (using Python)


## EBNF:

program = "SUB", "MAIN", "(", ")", "\n", { statement, "\n" }, "END", "SUB";

statement = assignment | print | statements | while | if | dimension;

assignment = identifier, "=", rel expression ;

print = "PRINT", rel expression ;

while = "WHILE", rel expression, "\n", {statement, "\n"}, "WEND" ;

if = "IF", rel expression, "\n", "THEN", {statement, "\n"}, ["else", "\n", {statement, "\n"}], "\n", "END", "IF" ;

dimension = "DIM", identifier, "AS", type ;

type = "INTEGER", "BOOLEAN" ;

rel expression = expression, [(">" | "<" | "="),  expression] ;

expression = term, {("+" | "-" | "OR"), term} ;

term = factor, {("*" | "/" | "AND"), factor} ;

factor = [("+" | "-" | "NOT")], factor | num | identifier | boolean | "(", rel expression, ")" | input ;

identifier = letter, {letter} ;

num = digit, {digit} ;

input = num ;

boolean = "TRUE" | "FALSE" ;

letter = ( a | ... | z | A | ... | Z ) ;

digit = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;




## Syntactic Diagram

![DS2.4](https://github.com/chends888/CompLog/blob/v2.4/assets/ds2.4.png)
