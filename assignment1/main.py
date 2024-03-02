import sys
from lexer import *

separators = ['$', '(', ')', '{', '}', ';', ',']
operators = ['==', '!=', '>', '<', '<=', '=>', '+', '-', '*', '/', '=']

output = []

def isSeparator(char):
    return char in separators

def isOperator(char):
    return char in operators

def processSeparator(char):
    output.append(["SEPARATOR", char])

def processOperator(char, inputFile):
    operatorStr = ""
    operatorStrTemp = ""
    operatorStr += char
    operatorStrTemp += char

    # Handles cases of !=, ==, <=, =>
    if char == "!" or char == "=" or char == "<":
        char = inputFile.read(1)
        operatorStrTemp += char
        
        # If the next char forms a 2 char operator that is in the operators list,
        # update the operatorStr string 
        if operatorStrTemp in operators:
            operatorStr += char
        else:
            inputFile.seek(inputFile.tell() - 1, 0)

    output.append(["OPERATOR", operatorStr])

def processAlpha(str):
    state = identifierDFSM(str)

    if state == "IDENTIFIER":
        output.append(["IDENTIFIER", str])
    elif state == "KEYWORD":
        output.append(["KEYWORD", str])
    elif state == "Invalid Token":
        output.append(["Invalid Token", str])

def processDigit(str):
    state = int_realDFSM(str)

    if state == "INTEGER":
        output.append(["INTEGER", str])
    elif state == "REAL":
        output.append(["REAL", str])
    elif state == "Invalid Token":
        output.append(["Invalid Token", str])

def main():
    inputFileName = input("Enter the input file name (or type exit to exit the program): ")

    if inputFileName == "exit":
        sys.exit(0)
    
    outputFileName = input("Enter the desired output file name: ")

    with open(inputFileName, 'r') as inputFile, open(outputFileName, 'w') as outputFile:

        # Writes source code to terminal and output file
        print("SOURCE CODE:\n\n")
        outputFile.write("SOURCE CODE:\n\n")
        for line in inputFile:
            print(line)
            outputFile.write(f"{line}\n")

        inputFile.seek(0)
        commentFlag = False
        str = ""

        while True:
            char = inputFile.read(1)
            
            if char == "":
                break

            # Handles beginning of comments
            if char == "[":
                char = inputFile.read(1)
                if char == "*":
                    commentFlag = True
                else:
                    inputFile.seek(inputFile.tell() - 1, 0)

            # Handles end of comments
            if char == "*" and commentFlag:
                char = inputFile.read(1)
                if char == "]":
                    commentFlag = False
                    char = inputFile.read(1)
                else:
                    inputFile.seek(inputFile.tell() - 1, 0)
            
            # If part of a comment, skip to next iteration
            if commentFlag:
                continue

            if isSeparator(char):
                processSeparator(char)
                continue

            if isOperator(char):
                processOperator(char, inputFile)
                continue

            if char.isalpha():
                str += char

                char = inputFile.read(1)
                if isOperator(char) or isSeparator(char) or char.isspace():
                    processAlpha(str)
                    str = ""
                    inputFile.seek(inputFile.tell() - 1)
                    continue
                else:
                    inputFile.seek(inputFile.tell() - 1)
                    continue

            if char.isdigit():
                str += char

                char = inputFile.read(1)
                if isOperator(char) or isSeparator(char) or char.isspace():
                    processDigit(str)
                    str = ""
                    inputFile.seek(inputFile.tell() - 1)
                    continue
                elif char == ".":
                    str += char
                    continue
                else:
                    inputFile.seek(inputFile.tell() - 1)
                    continue

        outputFile.write("{:<{width}}{}\n\n".format("TOKENS", "LEXEMES", width=30))
        
        for entry in output:
            outputFile.write("{:<{width}}{}\n".format(entry[0], entry[1], width=30))

if __name__ == "__main__":
    main()
















