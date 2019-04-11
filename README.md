# CompLog
Repository for the Computer Logic course. Building a compiler from scratch


Compiler EBNF:

statements = "Begin", "\n", statement, "\n", { statement, "\n" }, "End" ;

statement = assignment | print | statements ;

assignment = identifier, "=", expression ;

print = "print", expression ;

expression = term, { ("+" | "-"), term } ;

term = fator, { ("*" | "/"), fator } ;

fator = ("+" | "-"), fator | num | "(", expression, ")" | identifier ;

identifier = letter, { letter | digit | "_" } ;

num = digit, { digit } ;

letter = ( a | ... | z | A | ... | Z ) ;

digit = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;
