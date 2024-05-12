# from string import lower

# Assignment 3, Simplified Rat24s: no R3 and R5 (no functions), and real
# Statements:
# Compound: don't need to do anything for it
# Assign
# Return: don't need to do anything for it; no functions now
# Print: easy
# Scan: easy
# While

# turn on/off printing
switch = False
output = []
output2 = []
# increment by 1 when identifier declared and placed in table
memoryAddress = 5000
instructionTableIndex = 1
instructionTable = []
symbolTable = []
jumpStack = []
output = []

# prints to output file and increments tokens
def lexer_incrementor(tokens, lexemes, index):
    # print(range(len(tokens)))
    if index < len(lexemes)-1:
        if switch:
            print()
            print("{:<{width}}{}".format("Token: " + tokens[index], "Lexeme: " + lexemes[index], width=30))
        output.append("")
        output.append("{:<{width}}{}".format(f"TOKEN: {tokens[index]}", f"LEXEME: {lexemes[index]}", width=20))
        index += 1
        # print("NEW INDEX: ", index, lexemes[index], tokens[index])
    return index

# ----------------------------------------------------------------

def semantics(tokens, lexemes):
    global memoryAddress, symbolTable, instructionTable
    declaredIDs = set()
    index = 0

    while index < len(tokens):
        # Handles undeclared idenitifiers by checking declaredIDs
        if tokens[index] == "IDENTIFIER":
            if lexemes[index] not in declaredIDs:
                print(f"Error: {lexemes[index]} not declared")
                index += 1

        # Declarations start with integer, so when this keyword is detected, enter a
        # while loop to look for identifiers and add them to the symbol table and declaredIDs
        if lexemes[index] == "integer" or lexemes[index] == "boolean":
            currentType = lexemes[index]
            index += 1
            while lexemes[index] != ";":
                if tokens[index] == "SEPARATOR":
                    index += 1
                elif tokens[index] == "IDENTIFIER":
                    if not any(entry[0] == lexemes[index] for entry in symbolTable):
                        symbolTable.append([lexemes[index], memoryAddress, currentType])
                        declaredIDs.add(lexemes[index])
                        memoryAddress += 1
                        index += 1
                    else: # Handles identifiers that are already declared
                        print(f"Error: {lexemes[index]} already declared")
                        index += 1
        else:
            index += 1

    rat24s(tokens, lexemes, index=0)

    output2.append("Instruction Table")
    for entry in instructionTable:
        if switch:
            print(entry)
        output2.append(str(entry))

    if switch:
        print("")
        print("Symbol Table")
        print("Identifier\tMemory Address\tType")
    output2.append("")
    output2.append("Symbol Table")
    output2.append("Identifier\tMemory Address\tType")
    for k in symbolTable:
        if switch:
            print(f"{k[0]}\t\t{k[1]}\t\t{k[2]}")
        output2.append(f"{k[0]}\t\t{k[1]}\t\t{k[2]}")

    if switch:
        print("")
    output2.append("")
    for k in range(0, len(tokens)):
        if switch:
            print(f"{tokens[k]}: {lexemes[k]}")
        output2.append(f"{tokens[k]}: {lexemes[k]}")

    outputFileName = input("Enter the desired output file name (with .txt at the end): ")

    with open(outputFileName, 'w') as outputFile:
        for line in output2:
            outputFile.write(str(line) + "\n")
    
    print("Tokens and lexemes productions have succesfully been written to the output file.")
                
# done in semantics
# def insert_symbol(tokens, lexemes, index):
#     global symbol_table, memory_address
#     if tokens[index] in symbol_table:
#         print(f"Error: {lexemes[index]} already declared")
#     else:
#         symbol_table.append([lexemes[index], memory_address, tokens[index]])
#         memory_address += 1

def generateInstruction(operation, operand):
    global instructionTableIndex, instructionTable
    instructionTable.append([instructionTableIndex, operation, operand])
    instructionTableIndex += 1

def getAddress(id):
    global symbolTable
    for entry in symbolTable:
        if entry[0] == id:
            return entry[1]
    return -1


def backPatch(jumpAddr):
    global instructionTable, jumpStack
    # print("jumpstack")
    # for entry in jumpStack:
    #     print(entry)
    addr = jumpStack.pop()
    instructionTable[addr][2] = jumpAddr

def type_match(tokens, lexemes, index):
    for index in range(len(tokens)):
        if lexemes[index] in ["!=", ">", "<", "<=", "=>", "+", "-", "*", "==", "/"]:
            for entry in symbolTable:
                if entry[0] == lexemes[index-1]:
                    previousType = entry[2]
                if entry[0] == lexemes[index+1]:
                    nextType = entry[2]

            if lexemes[index-1] in [entry[0] for entry in symbolTable] and lexemes[index+1] in [entry[0] for entry in symbolTable]:
                if previousType != nextType:
                    # print("previousType != nextType called")
                    print(f"Error: {lexemes[index-1]} and {lexemes[index+1]} do not match: {previousType}, {nextType}")
                    output2.append(f"Error: {lexemes[index-1]} and {lexemes[index+1]} do not match: {previousType}, {nextType}")
                    continue
                elif lexemes[index] in ["+", "-", "*", "/"] and previousType == "boolean" and nextType == "boolean":
                    print(f"Error: arithmetic operations not allowed for booleans: {lexemes[index-1]} and {lexemes[index+1]}, {lexemes[index]}")
                    output2.append(f"Error: arithmetic operations not allowed for boolean: {lexemes[index-1]} and {lexemes[index+1]}, {lexemes[index]}")
                    continue
            if lexemes[index-1] in [entry[0] for entry in symbolTable] and tokens[index+1] != "IDENTIFIER":
                if previousType != tokens[index+1] and tokens[index+1] != "INTEGER":
                    # print("previousType != tokens[index+1] called")
                    print(f"Error: {lexemes[index-1]} and {lexemes[index+1]} do not match: {previousType}, {tokens[index+1]}")
                    output2.append(f"Error: {lexemes[index-1]} and {lexemes[index+1]} do not match: {previousType}, {tokens[index+1]}")
                    continue
                elif lexemes[index] in ["+", "-", "*", "/"] and previousType == "boolean" and tokens[index+1] == "boolean":
                    print(f"Error: arithmetic operations not allowed for booleans: {lexemes[index-1]} and {lexemes[index+1]}, {lexemes[index]}")
                    output2.append(f"Error: arithmetic operations not allowed for booleans: {lexemes[index-1]} and {lexemes[index+1]}, {lexemes[index]}")
                    continue
            elif lexemes[index+1] in [entry[0] for entry in symbolTable] and tokens[index-1] != "IDENTIFIER":
                if tokens[index-1] != nextType and tokens[index-1] != "INTEGER":
                    # print("tokens[index-1] != nextType called")
                    print(f"Error: {lexemes[index-1]} and {lexemes[index+1]} do not match: {tokens[index-1]}, {nextType}")
                    output2.append(f"Error: {lexemes[index-1]} and {lexemes[index+1]} do not match: {tokens[index-1]}, {nextType}")
                    continue
                elif lexemes[index] in ["+", "-", "*", "/"] and lexemes[index-1] == "boolean" and nextType == "boolean":
                    print(f"Error: arithmetic operations not allowed for booleans: {lexemes[index-1]} and {lexemes[index+1]}, {lexemes[index]}")
                    output2.append(f"Error: arithmetic operations not allowed for booleans: {lexemes[index-1]} and {lexemes[index+1]}, {lexemes[index]}")
                    continue
            if lexemes[index] in ["+", "-", "*", "/"] and tokens[index-1] == "boolean" and tokens[index+1] == "boolean":
                # print("boolean called")
                print(f"Error: arithmetic operations not allowed for booleans: {lexemes[index-1]} and {lexemes[index+1]}, {lexemes[index]}")
                output2.append(f"Error: arithmetic operations not allowed for booleans: {lexemes[index-1]} and {lexemes[index+1]}, {lexemes[index]}")
                continue
            # if tokens[index-1] != tokens[index+1]:
            #     print("regular called")
            #     print(f"Error: {lexemes[index-1]} and {lexemes[index+1]} do not match: {tokens[index-1]}, {tokens[index+1]}")
            #     continue
        index += 1
# ----------------------------------------------------------------
def rat24s(tokens, lexemes, index):
    # R1. <Rat24S>  ::=   $ <Opt Function Definitions>   $ <Opt Declaration List>  $ <Statement List>  $
    index = lexer_incrementor(tokens,lexemes,index)
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
                # ----------------------------------------------------------------
                type_match(tokens, lexemes, index)
                # ----------------------------------------------------------------
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

    # outputFileName = input("Enter the desired output file name (with .txt at the end): ")

    # with open(outputFileName, 'w') as outputFile:
    #     for line in output:
    #         outputFile.write(str(line) + "\n")

    # print("Tokens and lexemes productions have succesfully been written to the output file.")
    return True

def opt_function_definitions(tokens, lexemes, index):
    # R2. <Opt Function Definitions> ::= <Function Definitions>     |  <Empty>
    # Fixed OR, EXPECTING function 
    if lexemes[index] == "function":
        if switch:
            print("<Opt Function Definitions> -> <Function Definitions>")
        output.append("<Opt Function Definitions> -> <Function Definitions>")
        index = function_definitions(tokens, lexemes, index)
    else:
        if switch:
            print("<Opt Function Definitions> -> <Empty>")
        output.append("<Opt Function Definitions> -> <Empty>")
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
        output.append("<Function Definitions Prime> -> <Function Definitions>")
        index = function_definitions(tokens, lexemes, index)
    else:
        if switch:
            print("<Function Definitions Prime> -> e")
        output.append("<Function Definitions Prime> -> e")
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
    if lexemes[index] == ",":
        index = lexer_incrementor(tokens, lexemes, index)
        if switch:
            print("<Parameter List Prime> -> <Parameter List>")
        output.append("<Parameter List Prime> -> <Parameter List>")
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
    if lexemes[index] == "{":
        index = lexer_incrementor(tokens, lexemes, index)
        if switch:
            print("<Body> -> { <Statement List> }")
        output.append("<Body> -> { <Statement List> }")
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

def opt_declaration_list(tokens, lexemes, index):
    # R12. <Opt Declaration List> ::= <Declaration List>   |    <Empty>
    # OR fix: EXPECTING qualifier to move on
    if lexemes[index] == "integer" or lexemes[index] == "real" or lexemes[index] == "boolean":
        if switch:
            print("<Opt Declaration List> -> <Declaration List>")
        output.append("<Opt Declaration List> -> <Declaration List>")
        index = declaration_list(tokens, lexemes, index)
    else:
        if switch:
            print("<Opt Declaration List> -> <Empty>")
        output.append("<Opt Declaration List> -> <Empty>")
        empty()
    return index

def declaration_list(tokens, lexemes, index):
    # R13. <Declaration List> := <Declaration> ;<Declaration List Prime>
    if switch:
        print("<Declaration List> -> <Declaration> ;<Declaration Prime>")
    output.append("<Declaration List> -> <Declaration> ;<Declaration List Prime>")
    index = declaration(tokens, lexemes, index)
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
    if lexemes[index] == "{" or tokens[index] == "IDENTIFIER" or lexemes[index] in ["if", "return", "print", "scan", "while"]:
        if switch:
            print("<Statement List Prime> -> <Statement List>")
        output.append("<Statement List Prime> -> <Statement List>")
        index = statement_list(tokens, lexemes, index)
    else:
        if switch:
            print("<Statement List Prime> -> e")
        output.append("<Statement List Prime> -> e")
    return index

def statement(tokens, lexemes, index):
    # time.sleep(5)
    # R20. <Statement> ::=   <Compound>  |  <Assign>  |   <If>  |  <Return>   | <Print>   |   <Scan>   |  <While> 
    # OR Fix: EXPECTING...
    if lexemes[index] == "{":
        index = lexer_incrementor(tokens, lexemes, index)
        index = index - 1
        if switch:
            print("<Statement> -> <Compound>")
        output.append("<Statement> -> <Compound>")
        index = compound(tokens, lexemes, index)
    elif tokens[index] == "IDENTIFIER":
        index = lexer_incrementor(tokens, lexemes, index)
        index = index - 1
        if switch:
            print("<Statement> -> <Assign>")
        output.append("<Statement> -> <Assign>")
        index = assign(tokens, lexemes, index)
    elif lexemes[index] == "if":
        index = lexer_incrementor(tokens, lexemes, index)
        index = index - 1
        if switch:
            print("<Statement> -> <If>")
        output.append("<Statement> -> <If>")
        index = If(tokens, lexemes, index)
    elif lexemes[index] == "return":
        index = lexer_incrementor(tokens, lexemes, index)
        index = index - 1
        if switch:
            print("<Statement> -> <Return>")
        output.append("<Statement> -> <Return>")
        index = Return(tokens, lexemes, index)
    elif lexemes[index] == "print":
        index = lexer_incrementor(tokens, lexemes, index)
        index = index - 1
        if switch:
            print("<Statement> -> <Print>")
        output.append("<Statement> -> <Print>")
        index = Print(tokens, lexemes, index)
    elif lexemes[index] == "scan":
        index = lexer_incrementor(tokens, lexemes, index)
        index = index - 1
        if switch:
            print("<Statement> -> <Scan>")
        output.append("<Statement> -> <Scan>")
        index = scan(tokens, lexemes, index)
    elif lexemes[index] == "while":
        index = lexer_incrementor(tokens, lexemes, index)
        index = index - 1
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
        index = index + 1
        # index = lexer_incrementor(tokens, lexemes, index)
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
    if tokens[index] == "IDENTIFIER":
        # show identifier
        # index = lexer_incrementor(tokens, lexemes, index)
        # ----------------------------------------------------------------
        savedID = lexemes[index]
        # ----------------------------------------------------------------
        index = index + 1
        if switch:
            print("<Assign> -> <Identifier> = <Expression> ;")
        output.append("Assign -> <Identifier> = <Expression> ;")
        if lexemes[index] == "=":
            index = lexer_incrementor(tokens, lexemes, index)
            index = expression(tokens, lexemes, index)
            # ----------------------------------------------------------------
            generateInstruction("POPM", getAddress(savedID))
            # ----------------------------------------------------------------
            if lexemes[index-1] != ";":
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
    if lexemes[index] == "if":
        index = index + 1
        # index = lexer_incrementor(tokens, lexemes, index)
        if lexemes[index] == "(":
            index = lexer_incrementor(tokens, lexemes, index)
            if switch:
                print("<If> -> if ( <Condition> ) <Statement> <If Prime>")
            output.append("<If> -> if ( <Condition> ) <Statement> <If Prime>")
            index = condition(tokens, lexemes, index)
            if lexemes[index-1] == ")":
                index = statement(tokens, lexemes, index)
                # ----------------------------------------------------------------
                backPatch(instructionTableIndex)
                # ----------------------------------------------------------------
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

# TODO: need to be tested
def if_prime(tokens, lexemes, index):
    # R24. <If Prime> ::= endif     |     else <Statement> endif
    if lexemes[index] == "endif":
        # ----------------------------------------------------------------
        generateInstruction("LABEL", "nil")
        # ----------------------------------------------------------------
        index = lexer_incrementor(tokens, lexemes, index)
        if switch:
            print("<If Prime> -> endif")
        output.append("<If Prime> -> endif")
    elif lexemes[index] == "else":
        # ----------------------------------------------------------------
        generateInstruction("LABEL", "nil")
        # ----------------------------------------------------------------
        index = lexer_incrementor(tokens, lexemes, index)
        if switch:
            print("<If Prime> -> else <Statement> endif")
        output.append("<If Prime> -> else <Statement> endif")
        index = statement(tokens, lexemes, index)
        if lexemes[index] == "endif":
            index = lexer_incrementor(tokens, lexemes, index)
        else:
            if switch:
                print("Error: expected endif")
            output.append("Error: expected endif")
    else:
        if switch:
            print("Error: expected endif or else")
        output.append("Error: expected endif or else")
    return index

def Return(tokens, lexemes, index):
    # R25. <Return> ::= return <Return Prime>
    if lexemes[index] == "return":
        index = index + 1
        # index = lexer_incrementor(tokens, lexemes, index)
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
        index = lexer_incrementor(tokens, lexemes, index)
        if switch:
            print("<Return Prime> -> ;")
        output.append("<Return Prime> -> ;")
    else:
        if switch:
            print("<Return Prime> -> <Expression> ;")
        output.append("<Return Prime> -> <Expression> ;")
        index = expression(tokens, lexemes, index)
        if lexemes[index-1] != ";":
            if switch:
                print("Error: expected ;")
            output.append("Error: expected ;")
    return index

def Print(tokens, lexemes, index):
    # R27. <Print> ::=    print ( <Expression>);
    if lexemes[index] == "print":
        index = index + 1
        # index = lexer_incrementor(tokens, lexemes, index)
        if lexemes[index] == "(":
            index = lexer_incrementor(tokens, lexemes, index)
            if switch:
                print("<Print> -> print ( <Expression>);")
            output.append("<Print> -> print ( <Expression>);")
            index = expression(tokens, lexemes, index)
            if lexemes[index-1] == ")":
                if lexemes[index] == ";":
                    generateInstruction("SOUT", "")
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
        index = index + 1
        # index = lexer_incrementor(tokens, lexemes, index)
        if lexemes[index] == "(":
            index = lexer_incrementor(tokens, lexemes, index)
            # ----------------------------------------------------------------
            generateInstruction("SIN", "")
            # ----------------------------------------------------------------
            if switch:
                print("<Scan> -> scan ( <IDs> );")
            output.append("<Scan> -> scan ( <IDs> );")
            # ----------------------------------------------------------------
            index2 = index
            while (lexemes[index2] != ")"):
                if tokens[index2] == "IDENTIFIER":
                    generateInstruction("POPM", getAddress(lexemes[index]))
                index2 = index2 + 1
            # ----------------------------------------------------------------
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
    # ----------------------------------------------------------------
    global instructionTableIndex
    instructAddr = instructionTableIndex
    # ----------------------------------------------------------------
    
    if lexemes[index] == "while":
        # ----------------------------------------------------------------
        generateInstruction("LABEL", "nil")
        # ----------------------------------------------------------------
        index = index + 1
        # index = lexer_incrementor(tokens, lexemes, index)
        if lexemes[index] == "(":
            index = lexer_incrementor(tokens, lexemes, index)
            if switch:
                print("<While> -> while ( <Condition> ) <Statement> endwhile")
            output.append("<While> -> while ( <Condition> ) <Statement> endwhile")
            index = condition(tokens, lexemes, index)
            if lexemes[index-1] == ")":
                index = statement(tokens, lexemes, index)
                # ----------------------------------------------------------------
                generateInstruction("JUMP", instructAddr)
                backPatch(instructionTableIndex)
                # ----------------------------------------------------------------
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
    # ----------------------------------------------------------------
    op = lexemes[index-1]
    # ----------------------------------------------------------------
    index = expression(tokens, lexemes, index)
    # ----------------------------------------------------------------
    if op == "<":
        generateInstruction("LES", "nil")
        jumpStack.append(instructionTableIndex)
        generateInstruction("JUMP0", "nil")
    elif op == ">":
        generateInstruction("GRT", "nil")
        jumpStack.append(instructionTableIndex)
        generateInstruction("JUMP0", "nil")
    elif op == "==":
        generateInstruction("EQU", "nil")
        jumpStack.append(instructionTableIndex)
        generateInstruction("JUMP0", "nil")
    elif op == "!=":
        generateInstruction("NEQ", "nil")
        jumpStack.append(instructionTableIndex)
        generateInstruction("JUMP0", "nil")
    elif op == "<=":
        generateInstruction("LEQ", "nil")
        jumpStack.append(instructionTableIndex)
        generateInstruction("JUMP0", "nil")
    elif op == "=>":
        generateInstruction("GEQ", "nil")
        jumpStack.append(instructionTableIndex)
        generateInstruction("JUMP0", "nil")
    # ----------------------------------------------------------------

    return index

def relop(tokens, lexemes, index):
    # R31. <Relop> ::=   ==   |   !=    |   >     |   <    |  <=   |    =>        
    # term prime causes index-1
    if lexemes[index-1] == "==" or  lexemes[index-1] == "!=" or lexemes[index-1] == ">" or lexemes[index-1] == "<" or lexemes[index-1] == "<=" or lexemes[index] == "=>":
        if switch:
            print("<Relop> -> ", lexemes[index-1])
        output.append("<Relop> -> " + lexemes[index-1])
    else:
        if switch:
            print("Error: expected ==,!=, >, <, <=, =>")
        output.append("Error: expected ==,!=, >, <, <=, =>")
    return index

def expression(tokens, lexemes, index):
    # R32. <Expression> ::= <Term><Expression Prime>
    index = lexer_incrementor(tokens, lexemes, index)
    if switch:
        print("<Expression> -> <Term><Expression Prime>")
    output.append("<Expression> -> <Term><Expression Prime>")
    index = term(tokens, lexemes, index)
    index = expression_prime(tokens, lexemes, index)
    return index

def expression_prime(tokens, lexemes, index):
    # time.sleep(3)
    # R33. <Expression Prime> ::= + <Term><Expression Prime> | - <Term><Expression Prime> | e
    # term prime causes index-1
    if lexemes[index-1] == "+" or lexemes[index-1] == "-":
        # ----------------------------------------------------------------
        operator = lexemes[index-1]
        # ----------------------------------------------------------------
        if switch:
            print("<Expression Prime> -> ", lexemes[index-1], " <Term><Expression Prime>")
        output.append("<Expression Prime> -> " + lexemes[index-1] + " <Term><Expression Prime>")

        index = lexer_incrementor(tokens, lexemes, index)
        index = term(tokens, lexemes, index)
        # ----------------------------------------------------------------
        if operator == "+":
            generateInstruction("A", "nil")
        else:
            generateInstruction("S", "nil")
        # ----------------------------------------------------------------
        index = expression_prime(tokens, lexemes, index)
    else:
        if switch:
            print("<Expression Prime> -> e")
        output.append("<Expression Prime> -> e")
    return index

def term(tokens, lexemes, index):
    # R34. <Term> ::= <Factor><Term Prime>
    if switch:
        print("<Term> -> <Factor><Term Prime>")
    output.append("<Term> -> <Factor><Term Prime>")
    index = factor(tokens, lexemes, index)
    index = term_prime(tokens, lexemes, index)
    return index

def term_prime(tokens, lexemes, index):
    # R35. <Term Prime> ::= * <Factor><Term Prime> | / <Factor><Term Prime> | e
    if lexemes[index] == "*" or lexemes[index] == "/":
        # ----------------------------------------------------------------
        operator = lexemes[index]
        # ----------------------------------------------------------------
        index = lexer_incrementor(tokens, lexemes, index)
        if switch:
            print("<Term Prime> -> ", lexemes[index-1], " <Factor><Term Prime>")
        output.append("<Term Prime> -> " + lexemes[index-1] + " <Factor><Term Prime>")
        # # added this because of test case 1 for multiplication
        # index = lexer_incrementor(tokens, lexemes, index)
        index = factor(tokens, lexemes, index)
        # ----------------------------------------------------------------
        if operator == "*":
            generateInstruction("M", "nil")
        else:
            generateInstruction("D", "nil")
        # ----------------------------------------------------------------
        index = term_prime(tokens, lexemes, index)
    else:
        index = lexer_incrementor(tokens, lexemes, index)
        if switch:
            print("<Term Prime> -> e")
        output.append("<Term Prime> -> e")
    return index

def factor(tokens, lexemes, index):
    # R36. <Factor> ::=      -  <Primary>    |    <Primary>
    if lexemes[index] == "-":
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
        index = primary(tokens, lexemes, index)
    return index

def primary(tokens, lexemes, index):
    # R37. <Primary> ::= <Identifier> <Primary Prime>  |  <Integer>  |  ( <Expression> )  |  <Real>  |  true  |  false
    # expression causes index-1
    if tokens[index-1] == "IDENTIFIER" or tokens[index] == "IDENTIFIER":
        # for regulars
        if tokens[index] == "IDENTIFIER":
            # ----------------------------------------------------------------
            generateInstruction("PUSHM", getAddress(lexemes[index]))
            # ----------------------------------------------------------------
            index = lexer_incrementor(tokens, lexemes, index)
        # ----------------------------------------------------------------
        else:
            generateInstruction("PUSHM", getAddress(lexemes[index-1]))
        # ----------------------------------------------------------------
        if switch:
            print("<Primary> -> <Identifier> <Primary Prime>")
        output.append("<Primary> -> <Identifier> <Primary Prime>")
        index = primary_prime(tokens, lexemes, index)
    elif tokens[index-1] == "INTEGER" or tokens[index] == "INTEGER":
        if tokens[index] == "INTEGER":
            # ----------------------------------------------------------------
            generateInstruction("PUSHI", lexemes[index])
            # ----------------------------------------------------------------
            index = lexer_incrementor(tokens, lexemes, index)
        # ----------------------------------------------------------------
        else:
            generateInstruction("PUSHI", lexemes[index-1])
        # ----------------------------------------------------------------
        if switch:
            print("<Primary> -> <Integer>")
        output.append("<Primary> -> <Integer>")
    elif tokens[index-1] == "REAL" or tokens[index] == "REAL":
        if tokens[index] == "REAL":
            index = lexer_incrementor(tokens, lexemes, index)
        if switch:
            print("<Primary> -> <Real>")
        output.append("<Primary> -> <Real>")
    elif lexemes[index-1] in ["true","false"] or lexemes[index] in ["true", "false"]:
        if lexemes[index] in ["true", "false"]:
            # ----------------------------------------------------------------
            if lexemes[index] == "true":
                generateInstruction("PUSHI", "1")
            elif lexemes[index] == "false":
                generateInstruction("PUSHI", "0")
            # ----------------------------------------------------------------
            index = lexer_incrementor(tokens, lexemes, index)
            if switch:
                print("<Primary> -> ", lexemes[index-1])
            output.append("<Primary> -> " + lexemes[index-1])
        else:
            # ----------------------------------------------------------------
            if lexemes[index-1] == "true":
                generateInstruction("PUSHI", "1")
            elif lexemes[index-1] == "false":
                generateInstruction("PUSHI", "0")
            # ----------------------------------------------------------------
            if switch:
                print("<Primary> -> ", lexemes[index-1])
            output.append("<Primary> -> " + lexemes[index-1])
    elif lexemes[index] == "(": 
        index = lexer_incrementor(tokens, lexemes, index)
        if switch:
            print("<Primary> -> ( <Expression> )")
        output.append("<Primary> -> ( <Expression> )")
        index = expression(tokens, lexemes, index)
        if lexemes[index-1] != ")":
            if switch:
                print("Error: expected )")
            output.append("Error: expected )")
    else:
        if switch:
            print("Error: expected identifier, integer, real, true, false, or (")
        output.append("Error: expected identifier, integer, real, true, false, or (")
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
    return index

def empty():
    # R39. <Empty>   ::= e
    if switch:
        print("<Empty> -> e")
    output.append("<Empty> -> e")