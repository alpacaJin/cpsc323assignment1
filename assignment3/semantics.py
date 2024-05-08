memoryAddress = 5000

def semantics(tokens, lexemes):
    global memoryAddress
    symbolTable = []
    declaredIDs = set()
    index = 0

    while index < len(tokens):
        # Handles undeclared idenitifiers by checking declaredIDs
        if tokens[index] == "IDENTIFIER":
            if lexemes[index] not in declaredIDs:
                print(f"Error: {lexemes[index]} not declared")
                break

        # Declarations start with integer, so when this keyword is detected, enter a
        # while loop to look for identifiers and add them to the symbol table and declaredIDs
        if lexemes[index] == "integer":
            index += 1
            while lexemes[index] != ";":
                if tokens[index] == "SEPARATOR":
                    index += 1
                elif tokens[index] == "IDENTIFIER":
                    if not any(entry[0] == lexemes[index] for entry in symbolTable):
                        symbolTable.append([lexemes[index], memoryAddress, "integer"])
                        declaredIDs.add(lexemes[index])
                        memoryAddress += 1
                        index += 1
                    else: # Handles identifiers that are already declared
                        print(f"Error: {lexemes[index]} already declared")
                        break
        else:
            index += 1


    print("Symbol Table")
    print("Identifier\tMemory Address\tType")
    for k in symbolTable:
        print(f"{k[0]}\t\t{k[1]}\t\t{k[2]}")