memoryAddress = 5000
assemblyIndex = 0
instructionTableIndex = 1
instructionTable = []
symbolTable = []
jumpStack = []
output = []

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

    start(tokens, lexemes)

    for entry in instructionTable:
        print(entry)
        output.append(str(entry))

    print("Symbol Table")
    output.append("Symbol Table")
    print("Identifier\tMemory Address\tType")
    output.append("Identifier\tMemory Address\tType")
    for k in symbolTable:
        print(f"{k[0]}\t\t{k[1]}\t\t{k[2]}")
        output.append(f"{k[0]}\t\t{k[1]}\t\t{k[2]}")

    for k in range(0, len(tokens)):
        print(f"{tokens[k]}: {lexemes[k]}")
        output.append(f"{tokens[k]}: {lexemes[k]}")

    outputFileName = input("Enter the desired output file name (with .txt at the end): ")

    with open(outputFileName, 'w') as outputFile:
        for line in output:
            outputFile.write(str(line) + "\n")

def type_match(tokens, lexemes):
    global assemblyIndex

    for entry in symbolTable:
        print(entry)

    while assemblyIndex < len(tokens):
        print(lexemes[assemblyIndex])
        print(lexemes[assemblyIndex-1] in symbolTable)
        if lexemes[assemblyIndex] in ["!=", ">", "<", "<=", "=>", "+", "-", "*", "==", "/"]:
            for entry in symbolTable:
                if entry[0] == lexemes[assemblyIndex-1]:
                    previousType = entry[2]
                if entry[0] == lexemes[assemblyIndex+1]:
                    nextType = entry[2]
            if lexemes[assemblyIndex-1] in symbolTable and lexemes[assemblyIndex+1] in symbolTable:
                if previousType != nextType:
                    print("previousType != nextType called")
                    print(f"Error: {lexemes[assemblyIndex-1]} and {lexemes[assemblyIndex+1]} do not match: {previousType}, {nextType}")
                    continue
                elif previousType == "boolean" and nextType == "boolean":
                    print(f"Error: arithmetic operations not allowed for booleans: {lexemes[assemblyIndex-1]} and {lexemes[assemblyIndex+1]}, {lexemes[assemblyIndex]}")
                    continue
            if lexemes[assemblyIndex-1] in symbolTable:
                if previousType != tokens[assemblyIndex+1]:
                    print("previousType != tokens[assemblyIndex+1] called")
                    print(f"Error: {lexemes[assemblyIndex-1]} and {lexemes[assemblyIndex+1]} do not match: {previousType}, {tokens[assemblyIndex+1]}")
                    continue
                elif previousType == "boolean" and tokens[assemblyIndex+1] == "boolean":
                    print(f"Error: arithmetic operations not allowed for booleans: {lexemes[assemblyIndex-1]} and {lexemes[assemblyIndex+1]}, {lexemes[assemblyIndex]}")
                    continue
            elif lexemes[assemblyIndex+1] in symbolTable:
                if tokens[assemblyIndex-1] != nextType:
                    print("tokens[assemblyIndex-1] != nextType called")
                    print(f"Error: {lexemes[assemblyIndex-1]} and {lexemes[assemblyIndex+1]} do not match: {tokens[assemblyIndex-1]}, {nextType}")
                    continue
                elif lexemes[assemblyIndex-1] == "boolean" and nextType == "boolean":
                    print(f"Error: arithmetic operations not allowed for booleans: {lexemes[assemblyIndex-1]} and {lexemes[assemblyIndex+1]}, {lexemes[assemblyIndex]}")
                    continue
            if tokens[assemblyIndex-1] == "boolean" and tokens[assemblyIndex+1] == "boolean":
                print("boolean called")
                print(f"Error: arithmetic operations not allowed for booleans: {lexemes[assemblyIndex-1]} and {lexemes[assemblyIndex+1]}, {lexemes[assemblyIndex]}")
                continue
            # if tokens[assemblyIndex-1] != tokens[assemblyIndex+1]:
            #     print("regular called")
            #     print(f"Error: {lexemes[assemblyIndex-1]} and {lexemes[assemblyIndex+1]} do not match: {tokens[assemblyIndex-1]}, {tokens[assemblyIndex+1]}")
            #     continue
        assemblyIndex += 1

def start(tokens, lexemes):
    global assemblyIndex

    while assemblyIndex < len(tokens) - 1:
        # print(f"{tokens[assemblyIndex]}: {lexemes[assemblyIndex]}")
        # print(assemblyIndex)

        print("max" in symbolTable)

        while (lexemes[assemblyIndex] == "$"):
            assemblyIndex += 1

        # Handles/skips declaration portion of programs
        if lexemes[assemblyIndex] == "integer" or lexemes[assemblyIndex] == "boolean":
            while lexemes[assemblyIndex] != ";":
                assemblyIndex += 1
            assemblyIndex += 1
        if tokens[assemblyIndex] == "IDENTIFIER":
            assignment(tokens, lexemes)
        elif lexemes[assemblyIndex] == "while":
            whileStatement(tokens, lexemes)
        elif lexemes[assemblyIndex] == "if":
            ifStatement(tokens, lexemes)
        elif lexemes[assemblyIndex] == "print":
            printStatement(tokens, lexemes)
        elif lexemes[assemblyIndex] == "scan":
            scanStatement(tokens, lexemes)
        else:
            assemblyIndex += 1

def generateInstruction(op, oprnd):
    global instructionTableIndex, instructionTable
    print("op: ", op, " oprnd: ", oprnd)
    instructionTable.append([instructionTableIndex, op, oprnd])
    instructionTableIndex += 1

def getAddress(id):
    global symbolTable
    for entry in symbolTable:
        if entry[0] == id:
            return entry[1]
    return -1

def backPatch(jumpAddr):
    global instructionTable, jumpStack
    print("jumpstack")
    for entry in jumpStack:
        print(entry)
    addr = jumpStack.pop()
    instructionTable[addr][2] = jumpAddr

def assignment(tokens, lexemes):
    global assemblyIndex
    savedID = lexemes[assemblyIndex] # Maybe put this in an assignment function?
    assemblyIndex += 1
    if lexemes[assemblyIndex] == "=":
        assemblyIndex += 1
        E(tokens, lexemes)
        generateInstruction("POPM", getAddress(savedID))
    else:
        print("ERROR: = expected")

def whileStatement(tokens, lexemes):
    global assemblyIndex, instructionTableIndex
    instructAddr = instructionTableIndex
    generateInstruction("LABEL", "nil")
    assemblyIndex += 1
    if lexemes[assemblyIndex] == "(":
        assemblyIndex += 1
        C(tokens, lexemes)
        if lexemes[assemblyIndex] == ")":
            assemblyIndex += 1
            S(tokens, lexemes)
            generateInstruction("JUMP", instructAddr)
            backPatch(instructionTableIndex)
            # assemblyIndex += 1
            if lexemes[assemblyIndex] == "endwhile":
                assemblyIndex += 1
            else:
                print("ERROR: endwhile expected")
        else:
            print("ERROR: ) expected")
    else:
        print("ERROR: ( expected")

def ifStatement(tokens, lexemes):
    global assemblyIndex
    assemblyIndex += 1
    if lexemes[assemblyIndex] == "(":
        assemblyIndex += 1
        C(tokens, lexemes)
        if lexemes[assemblyIndex] == ")":
            assemblyIndex += 1
            S(tokens, lexemes)
            backPatch(instructionTableIndex)
            if lexemes[assemblyIndex] == "endif":
                assemblyIndex += 1
            else:
                print("ERROR: endif expected")

def printStatement(tokens, lexemes):
    global assemblyIndex
    assemblyIndex += 1
    if lexemes[assemblyIndex] == "(":
        assemblyIndex += 1
        while (lexemes[assemblyIndex] != ")"):
            if tokens[assemblyIndex] == "IDENTIFIER":
                E(tokens, lexemes)
                generateInstruction("SOUT", "")
            elif tokens[assemblyIndex] == "INTEGER":
                E(tokens, lexemes)
                generateInstruction("SOUT", "")
            elif lexemes[assemblyIndex] == "true" or lexemes[assemblyIndex] == "false":
                E(tokens, lexemes)
                generateInstruction("SOUT", "")
            else:
                print("ERROR: ) expected")
    else:
        print("ERROR: ( expected")

def scanStatement(tokens, lexemes):
    global assemblyIndex
    assemblyIndex += 1
    if lexemes[assemblyIndex] == "(":
        assemblyIndex += 1
        generateInstruction("SIN", "")
        while (lexemes[assemblyIndex] != ")"):
            if tokens[assemblyIndex] == "IDENTIFIER":
                generateInstruction("POPM", getAddress(lexemes[assemblyIndex]))
            else:
                print("ERROR: ) expected")

            assemblyIndex += 1
    else:
        print("ERROR: ( expected")

def E(tokens, lexemes):
    global assemblyIndex
    T(tokens, lexemes)
    EPrime(tokens, lexemes)

def EPrime(tokens, lexemes):
    global assemblyIndex
    if lexemes[assemblyIndex] == "+":
        assemblyIndex += 1
        T(tokens, lexemes)
        generateInstruction("A", "nil")
        EPrime(tokens, lexemes)
    elif lexemes[assemblyIndex] == "-":
        assemblyIndex += 1
        T(tokens, lexemes)
        generateInstruction("S", "nil")
        EPrime(tokens, lexemes)

def T(tokens, lexemes):
    global assemblyIndex
    F(tokens, lexemes)
    TPrime(tokens, lexemes)

def TPrime(tokens, lexemes):
    global assemblyIndex
    if lexemes[assemblyIndex] == "*":
        assemblyIndex += 1
        F(tokens, lexemes)
        generateInstruction("M", "nil")
        TPrime(tokens, lexemes)
    elif lexemes[assemblyIndex] == "/":
        assemblyIndex += 1
        F(tokens, lexemes)
        generateInstruction("D", "nil")
        TPrime(tokens, lexemes)

def F(tokens, lexemes):
    global assemblyIndex
    # if tokens[assemblyIndex] == "INTEGER" or tokens[assemblyIndex] == "IDENTIFIER":
    #     generateInstruction("PUSHI", lexemes[assemblyIndex])
    #     assemblyIndex += 1
    if lexemes[assemblyIndex].isnumeric():
        generateInstruction("PUSHI", lexemes[assemblyIndex])
        assemblyIndex += 1
    elif lexemes[assemblyIndex].isnumeric() == False:
        generateInstruction("PUSHM", getAddress(lexemes[assemblyIndex]))
        assemblyIndex += 1
    elif lexemes[assemblyIndex] == "true":
        generateInstruction("PUSHI", "1")
        assemblyIndex += 1
    elif lexemes[assemblyIndex] == "false":
        generateInstruction("PUSHI", "0")
        assemblyIndex += 1
    else:
        print("ERROR: ID expected")

def C(tokens, lexemes):
    global assemblyIndex, instructionTableIndex
    E(tokens, lexemes)
    if lexemes[assemblyIndex] in ["==", "!=", ">", "<", "=>", "<="]:
        op = lexemes[assemblyIndex]
        assemblyIndex += 1
        E(tokens, lexemes)
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
        else:
            print("ERROR: Relational operator expected")

# <Compound> ?

# Statement
def S(tokens, lexemes):
    global assemblyIndex

    while assemblyIndex < len(tokens):
        if tokens[assemblyIndex] == "IDENTIFIER":
            assignment(tokens, lexemes)
        elif lexemes[assemblyIndex] == "while":
            whileStatement(tokens, lexemes)
        elif lexemes[assemblyIndex] == "if":
            ifStatement(tokens, lexemes)
        elif lexemes[assemblyIndex] == "print":
            printStatement(tokens, lexemes)
        elif lexemes[assemblyIndex] == "scan":
            scanStatement(tokens, lexemes)
        elif lexemes[assemblyIndex] in ["endwhile", "endif"]:
            break
        else:
            assemblyIndex += 1
