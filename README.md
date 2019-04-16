# CompLog
Repository for the Computer Logic course. Building a compiler from scratch


Compiler EBNF:

statements = statement, "\n", { statement, "\n" };

statement = assignment | print | statements | while | if ;

assignment = identifier, "=", (expression, "input") ;

print = "print", expression ;

while = "while", relexpression, "\n", statements, "\n", "WEND" ;

if = "if", relexpression, "\n", "then", statements, {"else", statements}, "end if" ;

relexpression = expression, {">", "<", "="},  expression

expression = term, { ("+" | "-" | ">" | "<" | "="), term } ;

term = factor, { ("*" | "/"), factor } ;

factor = ("+" | "-"), factor | num | "(", expression, ")" | identifier ;

identifier = letter, { letter | digit | "_" } ;

num = digit, { digit } ;

letter = ( a | ... | z | A | ... | Z ) ;

digit = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;


