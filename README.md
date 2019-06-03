# CompLog
Repository for the Computer Logic course. Building a compiler from scratch (using Python)


## EBNF:

program = subdec | funcdec ;

subdec = "SUB", identifier, "(", {(identifier, "AS", type)}, ")", "\n", {(statement, "\n")}, "END", "SUB" ;

funcdec = "FUNCTION", identifier, "(", {(identifier, "AS", type)}, ")", "AS", type, "\n", {(statement, "\n")}, "END", "FUNCTION" ;

statement = assignment | print | statements | while | if | dimension | ("CALL", identifier,"(",  {(relexpression, {",", "relexpression"})}) ;

assignment = identifier, "=", relexpression ;

print = "PRINT", relexpression ;

while = "WHILE", relexpression, "\n", {statement, "\n"}, "WEND" ;

if = "IF", relexpression, "\n", "THEN", {statement, "\n"}, ["else", "\n", {statement, "\n"}], "\n", "END", "IF" ;

dimension = "DIM", identifier, "AS", type ;

type = "INTEGER", "BOOLEAN" ;

relexpression = expression, [(">" | "<" | "="),  expression] ;

expression = term, {("+" | "-" | "OR"), term} ;

term = factor, {("*" | "/" | "AND"), factor} ;

factor = [("+" | "-" | "NOT")], factor | num | identifier | boolean | "(", relexpression, ")" | input | (identifier,"(",  {(relexpression, {",", "relexpression"})}) ;

identifier = letter, {(letter | "_")} ;

input = num ;

num = digit, {digit} ;

boolean = "TRUE" | "FALSE" ;

letter = ( a | ... | z | A | ... | Z ) ;

digit = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;




## Syntactic Diagram

![DS2.4](https://github.com/chends888/CompLog/blob/v2.4/assets/ds2.4.png)
