import time
from main import *

# turn on printing
switch = True

# TODO: find a way to call lexer to take in, look over for unnecessary returns, return where the lexer is incrementing, or like when theres a terminal?

# test lists
# tokens = ['SEPARATOR', 'KEYWORD', 'IDENTIFIER', 'SEPARATOR', 'IDENTIFIER', 'KEYWORD', 'SEPARATOR', 'IDENTIFIER', 'KEYWORD', 'SEPARATOR', 'SEPARATOR', 'IDENTIFIER', 'OPERATOR', 'IDENTIFIER', 'OPERATOR', 'IDENTIFIER', 'SEPARATOR', 'KEYWORD', 'IDENTIFIER', 'OPERATOR', 'IDENTIFIER', 'SEPARATOR', 'SEPARATOR', 'SEPARATOR', 'KEYWORD', 'SEPARATOR', 'IDENTIFIER', 'SEPARATOR', 'SEPARATOR']
# lexemes = ['$', 'function', 'add', '(', 'num1', 'integer', ',', 'num2', 'integer', ')', '{', 'sum', '=', 'num1', '+', 'num2', ';', 'return', 'sum', '-', 'n3', ';', '}', '$', 'print', '(', 'sum', ')', '$']
        #   0   1           2       3       4       5       6       7       8       9    10    11    12    13     14    15    16     17       18     19   20   21   22    23    24      25    26   27   28

# Define lists for tokens and lexemes
tokens = [
    "SEPARATOR", "KEYWORD", "IDENTIFIER", "SEPARATOR", "IDENTIFIER", "KEYWORD", "SEPARATOR", 
    "SEPARATOR", 
    "KEYWORD", "INTEGER", "OPERATOR", "SEPARATOR", "IDENTIFIER", "OPERATOR", "INTEGER", "SEPARATOR", "OPERATOR", "INTEGER", "SEPARATOR", 
    "SEPARATOR", "SEPARATOR",
    "KEYWORD", "IDENTIFIER", "SEPARATOR", "IDENTIFIER", "SEPARATOR", "IDENTIFIER", "SEPARATOR", "SEPARATOR", 
    "KEYWORD", "SEPARATOR", "IDENTIFIER", "SEPARATOR", "IDENTIFIER", "SEPARATOR", "IDENTIFIER", "SEPARATOR", "SEPARATOR", 
    "KEYWORD", "SEPARATOR", "IDENTIFIER", "OPERATOR", "IDENTIFIER", "SEPARATOR", 
    "SEPARATOR", 
    "KEYWORD", "SEPARATOR", "IDENTIFIER", "SEPARATOR", "SEPARATOR", 
    "KEYWORD", "SEPARATOR", "IDENTIFIER", "SEPARATOR", "IDENTIFIER", "SEPARATOR", "SEPARATOR", "SEPARATOR",
    "IDENTIFIER", "OPERATOR", "IDENTIFIER", "OPERATOR", "IDENTIFIER", "SEPARATOR", "SEPARATOR",
    "KEYWORD", "SEPARATOR"
]

lexemes = [
    "$", "function", "convertx", "(", "fahr", "integer", ")", "{", "return", "5", "*", "(", 
    "fahr", "-", "32", ")", "/", "9", ";", "}", "$", "integer", "low", ",", "high", ",", "step", 
    ";", "$", "scan", "(", "low", ",", "high", ",", "step", ")", ";", "while", "(", "low", "<=", 
    "high", ")", "{", "print", "(", "low", ")", ";", "print", "(", "convertx", "(", "low", ")", 
    ")", ";", "low", "=", "low", "+", "step", ";", "}", "endwhile", "$"
]

# prints to output file and increments tokens
def lexer_incrementor(tokens, lexemes, index):
    if index < len(lexemes)-1:
        if switch:
            print()
            print("{:<{width}}{}".format("Token: " + tokens[index], "Lexeme: " + lexemes[index], width=30))
        output.append([tokens[index], lexemes[index]])
        index += 1
        print("NEW INDEX: ", index, lexemes[index], tokens[index])
    else:
        print("index = len(lexemes)")
    return index


def rat24s(tokens, lexemes, index):
    # R1. <Rat24S>  ::=   $ <Opt Function Definitions>   $ <Opt Declaration List>  $ <Statement List>  $
    # RAT24S ???
    index = lexer_incrementor(tokens,lexemes,index)
    # from above statement
    if lexemes[index-1] == '$':
        if switch:
            print("<Rat24S> -> $ <Opt Function Definitions>")
        output.append("<Rat24S> -> $ <Opt Function Definitions>")
        index = opt_function_definitions(tokens, lexemes, index)
        if lexemes[index] == '$' and index != len(lexemes):
            index = lexer_incrementor(tokens, lexemes, index)
            if switch:
                print("<Rat24S> -> $ <Opt Declaration List>")
            output.append("<Rat24S> -> $ <Opt Declaration List>")
            index = opt_declaration_list(tokens, lexemes, index)
            if lexemes[index] == '$' and index != len(lexemes):
                index = lexer_incrementor(tokens, lexemes, index)
                if switch:
                    print("<Rat24S> -> $ <Statement List>")
                output.append("<Rat24S -> $ <Statement List>")
                index = statement_list(tokens, lexemes, index)
                if lexemes[index] == '$' and index != len(lexemes):
                    index = lexer_incrementor(tokens, lexemes, index)
                    if switch:
                        print("<Rat24S> -> $") 
                        print("Parse completed")  
                    output.append("<Rat24S> -> $")
                else:
                    if switch:
                        print("Error: expected $")
                    output.append("Error: expected $")
            else:
                if switch:
                    print("Error: expected $")
                output.append("Error: expected $")
        else:
            if switch:
                print("Error: expected $")
            output.append("Error: expected $")
    else:
        if switch:
            print("Error: expected $")
        output.append("Error: expected $")


def opt_function_definitions(tokens, lexemes, index):
    # R2. <Opt Function Definitions> ::= <Function Definitions>     |  <Empty>
    if switch:
        print("<Opt Function Definitions> -> <Function Definitions> | <Empty>")
    output.append("<Opt Function Definitions> -> <Function Definitions> | <Empty>")
    # Fixed OR, EXPECTING function 
    if lexemes[index] == "function":
        index = function_definitions(tokens, lexemes, index)
    else:
        empty()
    return index

def function_definitions(tokens, lexemes, index):
    # R3. <Function Definitions> ::= <Function><Function Definitions Prime>
    if switch:
        print("<Function Definitions> -> <Function><Function Definitions Prime>")
    output.append("<Function Definitions> -> <Function><Function Definitions Prime>")
    index = function(tokens, lexemes, index)
    index = function_definitions_prime(tokens, lexemes, index)
    return index


def function_definitions_prime(tokens, lexemes, index):
    # R4. <Function Definitons Prime> ::= e | <Function Definitions>
    if lexemes[index] == "function":
        if switch:
            print("<Function Definitions Prime> -> <Function Definitions>")
        index = function_definitions(tokens, lexemes, index)
    else:
        if switch:
            print("<Function Definitions Prime> -> e")
    return index

def function(tokens, lexemes, index):
    # R5. <Function> ::= function  <Identifier>   ( <Opt Parameter List> )  <Opt Declaration List>  <Body>
    if lexemes[index] == "function":
        index = lexer_incrementor(tokens, lexemes, index)
        if tokens[index] == "IDENTIFIER":
            index = lexer_incrementor(tokens, lexemes, index)
            if switch:
                print("<Function> -> function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>")
            output.append("<Function> -> function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>")
            if lexemes[index] == "(":
                index = lexer_incrementor(tokens, lexemes, index)
                index = opt_parameter_list(tokens, lexemes, index)
                if lexemes[index] == ")":
                    index = lexer_incrementor(tokens, lexemes, index)
                    index = opt_declaration_list(tokens, lexemes, index)
                    index = body(tokens, lexemes, index)
                else:
                    if switch:
                        print("Error: expected )")
                    output.append("Error: expected )")
            else:
                if switch:
                    print("Error: expected (")
                output.append("Error: expected (")
        else:
            if switch:
                print("Error: expected IDENTIFIER")
            output.append("Error: expected IDENTIFIER")
    else:
        if switch:
            print("Error: expected function")
        output.append("Error: expected function")
    return index

def opt_parameter_list(tokens, lexemes, index):
    # R6. <Opt Parameter List> ::=  <Parameter List>    |     <Empty>
    # OR statement: to even start parameter list, we need an identifier
    if tokens[index] == "IDENTIFIER":
        if switch:
            print("<Opt Parameter List> -> <Parameter List>")
        output.append("<Opt Parameter List -> <Parameter List>")
        index = parameter_list(tokens, lexemes, index)
    else: 
        if switch:
            print("<Opt Parameter List> -> <Empty>")
        output.append("<Opt Parameter List> -> <Empty>")
        # formerly index = empty
        empty()
    return index

def parameter_list(tokens, lexemes, index):
    # R7. <Parameter List> ::= <Parameter><Parameter List Prime>
    if switch:
        print("<Parameter List> -> <Parameter><Parameter List Prime>")
    output.append("<Parameter List> -> <Parameter><Parameter List Prime>")
    index = parameter(tokens, lexemes, index)
    index = parameter_list_prime(tokens, lexemes, index)
    return index

def parameter_list_prime(tokens, lexemes, index):
    # R8. <Parameter List Prime> ::= e | <Parameter List>
    # need to go deeper for OR statement because it checks for a list in the parameters
    # need to skip the ',' so call incrementor because EXPECTING identifier
    if lexemes[index] == ",":
        index = lexer_incrementor(tokens, lexemes, index)
        if switch:
            print("<Parameter List Prime> -> <Parameter List>")
        index = parameter_list(tokens, lexemes, index)
    else:
        if switch:
            print("<Parameter List Prime> -> e")
        output.append("<Parameter List Prime> -> e")
    return index

def parameter(tokens, lexemes, index):
    # R9. <Parameter> ::=  <IDs>  <Qualifier> 
    if switch:
        print("<Parameter -> <ID> <Qualifier>")
    output.append("<Parameter> -> <IDs> <Qualifier>")
    index = ids(tokens, lexemes, index)
    index = qualifier(tokens, lexemes, index)
    return index

def qualifier(tokens, lexemes, index):
    # R10. <Qualifier> ::= integer   |    boolean   |  real 
    print("current Index in qualifier: ", lexemes[index])
    if lexemes[index] == "integer":
        index = lexer_incrementor(tokens, lexemes, index)
        if switch:
            print("<Qualifier> -> integer")
        output.append("<Qualifier> -> integer")
    elif lexemes[index] == "boolean":
        index = lexer_incrementor(tokens, lexemes, index)
        if switch:
            print("<Qualifier> -> boolean")
        output.append("<Qualifier> -> boolean")
    elif lexemes[index] == "real":
        index = lexer_incrementor(tokens, lexemes, index)
        if switch:
            print("<Qualifier> -> real")
        output.append("<Qualifier> -> real")
    else:
        if switch:
            print("Error: expected integer, boolean, or real")
        output.append("Error: expected integer, boolean, or real")
    return index

def body(tokens, lexemes, index):
    # R11. <Body>  ::=  {  < Statement List>  }
    print("current lexeme in body: ", lexemes[index])
    if lexemes[index] == "{":
        index = lexer_incrementor(tokens, lexemes, index)
        if switch:
            print("<Body> -> { <Statement List> }")
        output.append("<Body> -> { <Statement List> }")
        index = statement_list(tokens, lexemes, index)
        print("finished statement list in body")
        # index = lexer_incrementor(tokens, lexemes, index) nother
        if lexemes[index] == "}":
            index = lexer_incrementor(tokens, lexemes, index)
        else:
            if switch:
                print("Error: expected }")
            output.append("Error: expected }")
    else:
        if switch:
            print("Error: expected {")
        output.append("Error: expected {")
    return index

def opt_declaration_list(tokens, lexemes, index):
    # R12. <Opt Declaration List> ::= <Declaration List>   |    <Empty>
    # OR fix: EXPECTING qualifier to move on
    print("current lexeme in opt declaration list: ", lexemes[index])
    if lexemes[index] == "integer" or lexemes[index] == "real" or lexemes[index] == "boolean":
        if switch:
            print("<Opt Declaration List> -> <Declaration List>")
        index = declaration_list(tokens, lexemes, index)
    else:
        if switch:
            print("<Opt Declaration List> -> <Empty>")
        # formerly index = empty
        empty()
    return index

def declaration_list(tokens, lexemes, index):
    # R13. <Declaration List> := <Declaration> ;<Declaration List Prime>
    if switch:
        print("<Declaration List> -> <Declaration> ;<Declaration Prime>")
    output.append("<Declaration List> -> <Declaration> ;<Declaration List Prime>")
    index = declaration(tokens, lexemes, index)
    # get next lexeme
    print("finished declaration in declaration list")
    if lexemes[index] == ";":
        index = lexer_incrementor(tokens, lexemes, index)
        index = declaration_list_prime(tokens, lexemes, index)
    else:
        if switch:
            print("Error: expected ;")
        output.append("Error: expected ;")
    return index

def declaration_list_prime(tokens, lexemes, index):
    # R14. <Declaration List Prime> ::= e | <Declaration List>
    if lexemes[index] == "integer" or lexemes[index] == "real" or lexemes[index] == "boolean":
        if switch:
            print("<Declaration List Prime> -> <Declaration List>")
        output.append("<Declaration List Prime> -> <Declaration List>")
        index = declaration_list(tokens, lexemes, index)
    else:
        if switch:
            print("<Declaration List Prime> -> e")
        output.append("<Declaration List Prime> -> e")
    return index

def declaration(tokens, lexemes, index):
    # R15. <Declaration> ::=   <Qualifier > <IDs>    
    if switch:
        print("<Declaration> -> <Qualifier> <IDs>")
    output.append("<Declaration> -> <Qualifier> <IDs>")
    index = qualifier(tokens, lexemes, index)
    index = ids(tokens, lexemes, index)
    return index

def ids(tokens, lexemes, index):
    # R16. <IDs> ::= <Identifier><IDs Prime>
    print("current token in ids: ", tokens[index])
    if tokens[index] == "IDENTIFIER":
        index = lexer_incrementor(tokens, lexemes, index)
        if switch:
            print("<IDs> -> <Identifier><IDs Prime>")
        output.append("<IDs> -> <Identifier><IDs Prime>")
        index = ids_prime(tokens, lexemes, index)
    else:
        if switch:
            print("Error: expected IDENTIFIER")
        output.append("Error: expected IDENTIFIER")
    return index

def ids_prime(tokens, lexemes, index):
    # R17. <IDs Prime> ::= e | , <IDs>
    if lexemes[index] == ",":
        index = lexer_incrementor(tokens, lexemes, index)
        if switch:
            print("<IDs Prime> -> , <IDs Prime>")
        output.append("<IDs Prime> -> , <IDs Prime>")
        index = ids(tokens, lexemes, index)
    else:
        if switch:
            print("<IDs Prime> -> e")
        output.append("<IDs Prime> -> e")
    return index

def statement_list(tokens, lexemes, index):
    # R18. <Statement List> ::= <Statement> <Statement List Prime>
    if switch:
        print("<Statement List> -> <Statement> <Statement List Prime>")
    output.append("<Statement List> -> <Statement> <Statement List Prime>")
    index = statement(tokens, lexemes, index)
    index = statement_list_prime(tokens, lexemes, index)
    return index

def statement_list_prime(tokens, lexemes, index):
    # R19. <Statement List Prime> ::= e | <Statement List>
    print("current index in statement list prime: ", lexemes[index])
    if lexemes[index] == "{" or tokens[index] == "IDENTIFIER" or (tokens[index] == "KEYWORD" and lexemes[index] not in ["integer", "boolean", "real"]):
        if switch:
            print("<Statement List Prime> -> <Statement List>")
        index = statement_list(tokens, lexemes, index)
    else:
        if switch:
            print("<Statement List Prime> -> e")
        output.append("<Statement List Prime> -> e")
    return index

def statement(tokens, lexemes, index):
    # R20. <Statement> ::=   <Compound>  |  <Assign>  |   <If>  |  <Return>   | <Print>   |   <Scan>   |  <While> 
    # OR Fix: EXPECTING...
    # nother does not have this, STOPPED DOING nother here
    if lexemes[index] == "{":
        if switch:
            print("<Statement> -> <Compound>")
        output.append("<Statement> -> <Compound>")
        index = compound(tokens, lexemes, index)
    elif tokens[index] == "IDENTIFIER":
        if switch:
            print("<Statement> -> <Assign>")
        output.append("<Statement> -> <Assign>")
        index = assign(tokens, lexemes, index)
    elif lexemes[index] == "if":
        if switch:
            print("<Statement> -> <If>")
        output.append("<Statement> -> <If>")
        index = If(tokens, lexemes, index)
    elif lexemes[index] == "return":
        if switch:
            print("<Statement> -> <Return>")
        output.append("<Statement> -> <Return>")
        index = Return(tokens, lexemes, index)
    elif lexemes[index] == "print":
        if switch:
            print("<Statement> -> <Print>")
        output.append("<Statement> -> <Print>")
        index = Print(tokens, lexemes, index)
    elif lexemes[index] == "scan":
        if switch:
            print("<Statement> -> <Scan>")
        output.append("<Statement> -> <Scan>")
        index = scan(tokens, lexemes, index)
    elif lexemes[index] == "while":
        if switch:
            print("<Statement> -> <While>")
        output.append("<Statement> -> <While>")
        index = While(tokens, lexemes, index)
    else:
        if switch:
            print("Error: expected Compound, Assign, If, Return, Print, Scan, or While")
        output.append("Error: expected Compound, Assign, If, Return, Print, Scan, or While")
    return index

def compound(tokens, lexemes, index):
    # R21. <Compound> ::=   {  <Statement List>  } 
    if lexemes[index] == "{":
        index = lexer_incrementor(tokens, lexemes, index)
        if switch:
            print("<Compound> -> { <Statement List> }")
        output.append("<Compound> -> { <Statement List> }")
        index = statement_list(tokens, lexemes, index)
        if lexemes[index] == "}":
            index = lexer_incrementor(tokens, lexemes, index)
        else:
            if switch:
                print("Error: expected }")
            output.append("Error: expected }")
    else:
        if switch:
            print("Error: expected {")
        output.append("Error: expected {")
    return index

def assign(tokens, lexemes, index):
    # R22. <Assign> ::=     <Identifier> = <Expression> ;
    # double check for identifier, already moved index forward due to <Statement>
    if tokens[index] == "IDENTIFIER":
        # show identifier
        index = lexer_incrementor(tokens, lexemes, index)
        if switch:
            print("<Assign> -> <Identifier> = <Expression> ;")
        output.append("Assign -> <Identifier> = <Expression> ;")
        # TODO: can skip these, do this during clean up
        if lexemes[index] == "=":
            index = lexer_incrementor(tokens, lexemes, index)
            index = expression(tokens, lexemes, index)
            if lexemes[index-1] != ";":
            #     index = lexer_incrementor(tokens, lexemes, index)
            # else:
                if switch:
                    print("Error: expected ;")
                output.append("Error: expected ;")
        else:
            if switch:
                print("Error: expected =")
            output.append("Error: expected =")
    else:
        if switch:
            print("Error: expected IDENTIFIER")
        output.append("Error: expected IDENTIFIER")
    return index

def If(tokens, lexemes, index):
    # R23. <If> ::= if ( <Condition> ) <Statement> <If Prime>
    # index - 1 from statement
    if lexemes[index] == "if":
        if lexemes[index] == "(":
            index = lexer_incrementor(tokens, lexemes, index)
            if switch:
                print("<If> -> if ( <Condition> ) <Statement> <If Prime>")
            output.append("<If> -> if ( <Condition>")
            index = condition(tokens, lexemes, index)
            if lexemes[index] == ")":
                # TODO: bfdjkk
                if switch:
                    print(" ) <Statement> <If Prime>")
                output.append(" ) <Statement> <If Prime>")
                index = statement(tokens, lexemes, index)
                index = if_prime(tokens, lexemes, index)
            else:
                if switch:
                    print("Error: expected )")
                output.append("Error: expected )")
        else:
            if switch:
                print("Error: expected (")
            output.append("Error: expected (")
    else:
        if switch:
            print("Error: expected if")
        output.append("Error: expected if")
    return index

# TODO: fix this
def if_prime(tokens, lexemes, index):
    # R24. <If Prime> ::= endif     |     else <Statement> endif
    if lexemes == "endif":
        if switch:
            print("<If Prime> -> endif")
        output.append("<If Prime> -> endif")
    elif lexemes == "else":
        if switch:
            print("<If Prime> -> else <Statement> endif")
        output.append("<If Prime> -> else <Statement> endif")
        statement()
        if lexemes == "endif":
            if switch:
                print(" endif")
            output.append(" endif")
        else:
            if switch:
                print("Error: expected endif")
            output.append("Error: expected endif")
    else:
        if switch:
            print("Error: expected endif or else")
        output.append("Error: expected endif or else")

def Return(tokens, lexemes, index):
    # R25. <Return> ::= return <Return Prime>
    if lexemes[index] == "return":
        index = lexer_incrementor(tokens, lexemes, index)
        if switch:
            print("<Return> -> return <Return Prime>")
        output.append("<Return> -> return <Return Prime>")
        index = return_prime(tokens, lexemes, index)
    else:
        if switch:
            print("Error: expected return")
        output.append("Error: expected return")
    return index

def return_prime(tokens, lexemes, index):
    # R26. <Return Prime> ::= ;     |     <Expression> ;
    if lexemes[index] == ";":
        if switch:
            print("<Return Prime> -> ;")
        output.append("<Return Prime> -> ;")
    else:
        if switch:
            print("<Return Prime> -> <Expression> ;")
        index = expression(tokens, lexemes, index)
        # output the semicolon 
        # index = lexer_incrementor(tokens, lexemes, index)
        if lexemes[index-1] != ";":
            # finish up tokens when done
        #     index = lexer_incrementor(tokens, lexemes, index)
        # else:
            if switch:
                print("Error: expected ;")
            output.append("Error: expected ;")
    return index

def Print(tokens, lexemes, index):
    # R27. <Print> ::=    print ( <Expression>);
    if lexemes[index] == "print":
        index = lexer_incrementor(tokens, lexemes, index)
        if lexemes[index] == "(":
            index = lexer_incrementor(tokens, lexemes, index)
            if switch:
                print("<Print> -> print ( <Expression>);")
            output.append("<Print> -> print ( <Expression>);")
            index = expression(tokens, lexemes, index)
            if lexemes[index-1] == ")":
                if lexemes[index] == ";":
                    index = lexer_incrementor(tokens, lexemes, index)
                else:
                    if switch:
                        print("Error: expected ;")
                    output.append("Error: expected ;")
            else:
                if switch:
                    print("Error: expected )")
                output.append("Error: expected )")
        else:
            if switch:
                print("Error: expected (")
            output.append("Error: expected (")
    else:
        if switch:
            print("Error: expected print")
        output.append("Error: expected print")
    return index

def scan(tokens, lexemes, index):
    #R28. <Scan> ::=    scan ( <IDs> );
    if lexemes[index] == "scan":
        index = lexer_incrementor(tokens, lexemes, index)
        if lexemes[index] == "(":
            index = lexer_incrementor(tokens, lexemes, index)
            if switch:
                print("<Scan> -> scan ( <IDs> );")
            output.append("<Scan> -> scan ( <IDs> );")
            index = ids(tokens, lexemes, index)
            if lexemes[index] == ")":
                index = lexer_incrementor(tokens, lexemes, index)
                if lexemes[index] == ";":
                    index = lexer_incrementor(tokens, lexemes, index)
                else:
                    if switch:
                        print("Error: expected ;")
                    output.append("Error: expected ;")
            else:
                if switch:
                    print("Error: expected )")
                output.append("Error: expected )")
        else:
            if switch:
                print("Error: expected (")
            output.append("Error: expected (")
    else:
        if switch:
            print("Error: expected scan")
        output.append("Error: expected scan")
    return index

def While(tokens, lexemes, index):
    # R29. <While> ::=  while ( <Condition>  )  <Statement>  endwhile
    if lexemes[index] == "while":
        index = lexer_incrementor(tokens, lexemes, index)
        if lexemes[index] == "(":
            index = lexer_incrementor(tokens, lexemes, index)
            if switch:
                print("<While> -> while ( <Condition> ) <Statement> endwhile")
            output.append("<While> -> while ( <Condition>")
            index = condition(tokens, lexemes, index)
            if lexemes[index-1] == ")":
                # index = lexer_incrementor(tokens, lexemes, index)
                index = statement(tokens, lexemes, index)
                if lexemes[index] == "endwhile":
                    index = lexer_incrementor(tokens, lexemes, index)
                else:
                    if switch:
                        print("Error: expected endwhile")
                    output.append("Error: expected endwhile")
            else:
                if switch:
                    print("Error: expected )")
                output.append("Error: expected )")
        else:
            if switch:
                print("Error: expected (")
            output.append("Error: expected (")
    else:
        if switch:
            print("Error: expected while")
        output.append("Error: expected while")
    return index

def condition(tokens, lexemes, index):
    # R30. <Condition> ::=     <Expression>  <Relop>   <Expression>
    if switch:
        print("<Condition> -> <Expression> <Relop> <Expression>")
    output.append("<Condition> -> <Expression> <Relop> <Expression>")
    index = expression(tokens, lexemes, index)
    index = relop(tokens, lexemes, index)
    index = expression(tokens, lexemes, index)
    return index

def relop(tokens, lexemes, index):
    # R31. <Relop> ::=   ==   |   !=    |   >     |   <    |  <=   |    =>        
    # term prime causes index-1
    if lexemes[index-1] == "==" or  lexemes[index-1] == "!=" or lexemes[index-1] == ">" or lexemes[index-1] == "<" or lexemes[index-1] == "<=" or lexemes[index] == "=>":
        # index = lexer_incrementor(tokens, lexemes, index)
        if switch:
            print("<Relop> -> ", lexemes[index-1])
        output.append("<Relop> -> " + lexemes[index-1])
    else:
        if switch:
            print("Error: expected ==,!=, >, <, <=, =>")
        output.append("Error: expected ==,!=, >, <, <=, =>")
    return index

def expression(tokens, lexemes, index):
    # time.sleep(3)
    # R32. <Expression> ::= <Term><ExpressionPrime>
    index = lexer_incrementor(tokens, lexemes, index)
    if switch:
        print("<Expression> -> <Term><ExpressionPrime>")
    output.append("<Expression> -> <Term><ExpressionPrime>")
    index = term(tokens, lexemes, index)
    print("we finished term in expression")
    # # # test to match his assignment 6
    # index = lexer_incrementor(tokens, lexemes, index)
    index = expression_prime(tokens, lexemes, index)
    return index

def expression_prime(tokens, lexemes, index):
    # time.sleep(3)
    # R33. <Expression Prime> ::= + <Term><Expression Prime> | - <Term><Expression Prime> | e
    print("current index in expression prime: ", lexemes[index])
    # problems because I printed in term prime index-1
    if lexemes[index-1] == "+" or lexemes[index-1] == "-":
        # index = lexer_incrementor(tokens, lexemes, index)
        if switch:
            print("<Expression Prime> -> ", lexemes[index-1], " <Term><ExpressionPrime>")
        output.append("<Expression Prime> -> " + lexemes[index-1] + " <Term><ExpressionPrime>")
        index = lexer_incrementor(tokens, lexemes, index)
        index = term(tokens, lexemes, index)
        index = expression_prime(tokens, lexemes, index)
    else:
        if switch:
            print("<Expression Prime> -> e")
        output.append("<Expression Prime> -> e")
        # put it here if you want it to be added at the end, index = lexer_incrementor(tokens, lexemes, index)
    print("finished expression prime")
    return index

def term(tokens, lexemes, index):
    # R34. <Term> ::= <Factor><TermPrime>
    print("current index in term: ", index)
    if switch:
        print("<Term> -> <Factor><TermPrime>")
    output.append("<Term> -> <Factor><TermPrime>")
    index = factor(tokens, lexemes, index)
    index = term_prime(tokens, lexemes, index)
    return index

def term_prime(tokens, lexemes, index):
    # print("current index in term prime: ", index)
    # R35. <TermPrime> ::= * <Factor><TermPrime> | / <Factor><TermPrime> | e
    # index-1 incremented from factor domino
    # index = lexer_incrementor(tokens, lexemes, index)
    print("current index in term prime: ", lexemes[index])
    if lexemes[index] == "*" or lexemes[index] == "/":
        index = lexer_incrementor(tokens, lexemes, index)
        if switch:
            print("<Term Prime> -> ", lexemes[index-1], " <Factor><TermPrime>")
        output.append("<Term Prime> -> " + lexemes[index-1] + " <Factor><TermPrime>")
        # print number, messes up if not number 
        # index = lexer_incrementor(tokens, lexemes, index)
        index = factor(tokens, lexemes, index)
        index = term_prime(tokens, lexemes, index)
    else:
        # move incrementor here to match assignment 6 but who cares
        index = lexer_incrementor(tokens, lexemes, index)
        if switch:
            print("<Term Prime> -> e")
        output.append("<Term Prime> -> e")
    print("finished term_prime: ", lexemes[index])
    return index

def factor(tokens, lexemes, index):
    # time.sleep(5)
    # R36. <Factor> ::=      -  <Primary>    |    <Primary>
    if lexemes[index] == "-":
        # i think this is ok, print the - before printing the production
        index = lexer_incrementor(tokens, lexemes, index)
        if switch:
            print("<Factor> -> - <Primary>")
        output.append("<Factor> -> - <Primary>")
        index = lexer_incrementor(tokens, lexemes, index)
        index = primary(tokens, lexemes, index)
    else:
        if switch:
            print("<Factor> -> <Primary>")
        output.append("<Factor> -> <Primary>")
        # index = lexer_incrementor(tokens, lexemes, index)
        index = primary(tokens, lexemes, index)
    return index

def primary(tokens, lexemes, index):
    # R37. <Primary> ::= <Identifier> <Primary Prime>  |  <Integer>  |  ( <Expression )  |  <Real>  |  true  |  false
    # print("token at ")
    # ITS BECAUSE OF ALL EXPRESSION
    if tokens[index - 1] == "IDENTIFIER" or tokens[index] == "IDENTIFIER":
        if switch:
            print("<Primary> -> <Identifier> <Primary Prime>")
        output.append("<Primary> -> <Identifier> <Primary Prime>")
        index = primary_prime(tokens, lexemes, index)
    # THIS IS SO HARDCODED LMAO
    elif tokens[index-1] == "INTEGER" or tokens[index] == "INTEGER": # outputted integer already from expression
        if tokens[index] == "INTEGER":
            index = lexer_incrementor(tokens, lexemes, index)
        if switch:
            print("<Primary> -> <Integer>")
        output.append("<Primary> -> <Integer>")
        # index = lexer_incrementor(tokens, lexemes, index)
    elif tokens[index] == "REAL":
        if switch:
            print("<Primary> -> <Real>")
        output.append("<Primary> -> <Real>")
    elif lexemes[index] == "true" or lexemes[index] == "false":
        if switch:
            print("<Primary> -> ", lexemes[index])
        output.append("<Primary> -> ", lexemes[index])
    elif lexemes[index] == "(": 
        index = lexer_incrementor(tokens, lexemes, index)
        if switch:
            print("<Primary> -> ( <Expression> )")
        output.append("<Primary> -> ( <Expression> )")
        # index = lexer_incrementor(tokens, lexemes, index)
        index = expression(tokens, lexemes, index)
        if lexemes[index-1] != ")":
        #     index = lexer_incrementor(tokens, lexemes, index)
        # else:
            if switch:
                print("Error: expected )")
            output.append("Error: expected )")
    else:
        if switch:
            print("Error: expected identifier, integer, real, true, false, or (")
        output.append("Error: expected identifier, integer, real, true, false, or (")
    print("finished primary: ", lexemes[index])
    return index

def primary_prime(tokens, lexemes, index):
    # R38. <Primary Prime> ::= e  |  ( <IDs> )
    if lexemes[index] == "(":
        index = lexer_incrementor(tokens, lexemes, index)
        if switch:
            print("<Primary Prime> -> ( <IDs> )")
        output.append("<Primary Prime> -> ( <IDs> )")
        index = ids(tokens, lexemes, index)
        if lexemes[index] == ")":
            index = lexer_incrementor(tokens, lexemes, index)
        else:
            if switch:
                print("Error: expected )")
            output.append("Error: expected )")
    else:
        if switch:
            print("<Primary Prime> -> e")
        output.append("<Primary Prime> -> e")
    print("finished primary_prime: ", lexemes[index])
    return index

def empty():
    # R39. <Empty>   ::= e
    if switch:
        print("<Empty> -> e")
    output.append("<Empty> -> e")

def main():
    index = 0

    rat24s(tokens, lexemes, index)


    return 0

if __name__ == "__main__":
    main()