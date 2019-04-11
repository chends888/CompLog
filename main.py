#!/usr/bin/env python
# -*- coding: utf-8 -*-

import operator
import sys

class Token:
    def __init__(self, tokentype, tokenvalue):
        self.tokentype = tokentype
        self.tokenvalue = tokenvalue

class PrePro:
    def removeComments(origin):
        flag = False
        procorigin = ''
        for i in origin:
            if (i == "'"):
                flag = not flag
                continue
            if (i == '\n'):
                flag = False
            if (flag):
                continue
            procorigin += i
        return procorigin


class Node:
    def __init__(self, value=False, nodes=[]):
        self.value = value
        self.children = nodes
    def Evaluate(self, st):
        pass

class BinOp (Node):
    def Evaluate(self, st):
        # https://stackoverflow.com/questions/18591778/how-to-pass-an-operator-to-a-python-function
        allowed_operators={
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "//": operator.floordiv
        }
        child1 = self.children[0]
        child1 = child1.Evaluate(st)

        child2 = self.children[1]
        child2 = child2.Evaluate(st)
        return allowed_operators[self.value](child1, child2)

class UnOp(Node):
    def Evaluate(self, st):
        child = self.children[0]
        child = child.Evaluate(st)
        if (self.value == '-'):
            return -child
        elif (self.value == '+'):
            return +child

class IntVal(Node):
    def Evaluate(self, st):
        return int(self.value)

class Identifier(Node):
    def Evaluate(self, st):
        return st.getter(self.value)

class NoOp(Node):
    pass

class Statements(Node):
    def Evaluate(self, st):
        for i in self.children:
            i.Evaluate(st)

class Assignment(Node):
    def Evaluate(self, st):
        st.setter(self.children[0], self.children[1].Evaluate(st))

class Print(Node):
    def Evaluate(self, st):
        print(self.children[0].Evaluate(st))

class Tokenizer:
    def __init__(self, origin):
        self.origin = PrePro.removeComments(origin)
        self.position = 0
        self.actual = Token('EOF', 'EOF')
        self.reservedwords = ['PRINT', 'BEGIN', 'END']
        self.selectNext()

    def selectNext(self):
        while (self.position < len(self.origin) and self.origin[self.position] == ' '):
            self.position += 1

        token = ''
        if (self.position >= (len(self.origin))):
            self.actual = Token('EOF', 'EOF')
            return

        elif (self.origin[self.position].isdigit()):
            while (self.origin[self.position].isdigit()):
                token += self.origin[self.position]
                self.position += 1
            self.actual = Token('INT', token)

        elif (self.origin[self.position].isalpha()):
            while (self.origin[self.position].isalpha()):
                token += self.origin[self.position]
                self.position += 1
            token = token.upper()

            if (token in self.reservedwords):
                self.actual = Token('COMM', token)
            else:
                self.actual = Token('IDENT', token)

        else:
            if (not self.origin[self.position].isdigit()):
                token += self.origin[self.position]
                self.position += 1
            if (token == '+'):
                self.actual = Token('PLUS', token)
            elif (token == '-'):
                self.actual = Token('MINUS', token)
            elif (token == '*'):
                self.actual = Token('MULT', token)
            elif (token == '/'):
                self.actual = Token('DIV', '//')
            elif (token == '//'):
                self.actual = Token('DIV', token)
            elif (token == '('):
                self.actual = Token('PAR', token)
            elif (token == ')'):
                self.actual = Token('PAR', token)
            elif (token == '='):
                self.actual = Token('ASSIG', token)
            elif (token == '\n'):
                self.actual = Token('ENDL', token)
            else:
                raise ValueError('Unexpected token %s' %(token))

class SymbolTable:
    def __init__(self):
        self.symtabledict = {}

    def getter(self, identifier):
        return self.symtabledict[identifier]
    def setter(self, identifier, value):
        self.symtabledict[identifier] = value



class Parser:
    def factorExpression():
        try:
            token1 = Parser.tokens.actual
        except:
            raise ValueError('Token not found')
        if (token1.tokentype == 'INT'):
            Parser.tokens.selectNext()
            return IntVal(token1.tokenvalue)

        elif (token1.tokentype == 'PLUS' or token1.tokentype == 'MINUS'):
            if (token1.tokentype == 'PLUS'):
                Parser.tokens.selectNext()
                unop = UnOp('+', [Parser.factorExpression()])
                return unop
            elif (token1.tokentype == 'MINUS'):
                Parser.tokens.selectNext()
                unop = UnOp('-', [Parser.factorExpression()])
                return unop

            else:
                raise SyntaxError('Unexpected unary operation %s' %(token1.tokenvalue))

        elif (token1.tokentype == 'IDENT'):
            Parser.tokens.selectNext()
            return Identifier(token1.tokenvalue)

        elif (token1.tokenvalue == '('):
            Parser.tokens.selectNext()
            expr = Parser.parserExpression()
            if (Parser.tokens.actual.tokenvalue == ')'):
                Parser.tokens.selectNext()
                return expr
            else:
                raise SyntaxError('Unexpected token  %s, expected ")"' %(Parser.tokens.actual.tokenvalue))
        else:
            raise SyntaxError('Invalid token, element %s is not INT' %(token1.tokenvalue))


    def termExpression():
        factor1 = Parser.factorExpression()
        op = Parser.tokens.actual
        termop = factor1

        while (op.tokentype == 'DIV' or op.tokentype == 'MULT'):
            termop = BinOp(op.tokenvalue, [termop])
            Parser.tokens.selectNext()
            factor2 = Parser.factorExpression()
            termop.children.append(factor2)
            op = Parser.tokens.actual
        return termop

    @staticmethod
    def parserExpression():
        term1 = Parser.termExpression()
        op = Parser.tokens.actual
        parserop = term1

        while (op.tokentype == 'PLUS' or op.tokentype == 'MINUS'):
            parserop = BinOp(op.tokenvalue, [parserop])
            Parser.tokens.selectNext()
            term2 = Parser.termExpression()
            parserop.children.append(term2)
            op = Parser.tokens.actual
        return parserop

    def statement():
        actualtoken = Parser.tokens.actual

        if (actualtoken.tokentype == 'COMM' and actualtoken.tokenvalue == 'PRINT'):
            Parser.tokens.selectNext()
            result = Parser.parserExpression()
            printtree = Print('PRINT', [result])
            return printtree
        elif (actualtoken.tokentype == 'IDENT'):
            ident = actualtoken
            Parser.tokens.selectNext()
            if (Parser.tokens.actual.tokentype == 'ASSIG'):
                Parser.tokens.selectNext()
                result = Parser.parserExpression()
                assigtree = Assignment('assig', [ident.tokenvalue, result])
                return assigtree
            else:
                raise ValueError('Expected assignment symbol "=", got %s' %(Parser.tokens.actual.tokenvalue))
        elif (actualtoken.tokentype == 'COMM' and actualtoken.tokenvalue == 'BEGIN'):
            return Parser.statements()
        else:
            return NoOp()

    def statements():
        statements = []
        if (Parser.tokens.actual.tokenvalue == 'BEGIN'):
            Parser.tokens.selectNext()
            if (Parser.tokens.actual.tokenvalue == '\n'):
                Parser.tokens.selectNext()
                while (Parser.tokens.actual.tokenvalue != 'END'):
                    statements.append(Parser.statement())
                    if (Parser.tokens.actual.tokenvalue == '\n'):
                        Parser.tokens.selectNext()
                    else:
                        raise SyntaxError('End line after statement token not found')
                if (Parser.tokens.actual.tokenvalue == 'END'):
                    Parser.tokens.selectNext()
                    if (Parser.tokens.actual.tokenvalue == '\n'):
                        Parser.tokens.selectNext()
                        return Statements('statements', statements)
                    else:
                        raise SyntaxError('End line token not found')
                else:
                    raise SyntaxError('Statement end token "END" not found')
            else:
                raise SyntaxError('End line after BEGIN token not found')
        else:
            raise SyntaxError('Unexpected BEGIN token %s' %(Parser.tokens.actual.tokenvalue))


    def run(code):
        Parser.tokens = Tokenizer(code)
        result = Parser.statements()
        if (Parser.tokens.actual.tokentype == 'EOF'):
            return result
        else:
            raise EOFError('Program ended before EOF')



'''Rotina de Testes'''

with open(sys.argv[1], 'r', encoding='utf-8') as infile:
    lines = infile.read()

st = SymbolTable()
Parser.run(lines).Evaluate(st)
