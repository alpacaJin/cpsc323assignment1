import sys
from lexer import *

separators = ['$', '(', ')', '{', '}', ';', ',']
operators = ['==', '!=', '>', '<', '<=', '=>', '+', '-', '*', '/', '=']

output = []

def isOperator(char):
    return char in operators

def isSeparator(char):
    return char in separators

def processSeparator(char, outputFile):
    output.append(["SEPARATOR", char])

def processOperator(char, inputFile, outputFile):
    operatorStr = ""
    operatorStrTemp = ""
    operatorStr += char
    operatorStrTemp += char

    # Handles cases of !=, ==, <=, =>
    if char == "!" or char == "=" or char == "<":
        char = inputFile.read(1)
        operatorStrTemp += char
        
        if operatorStrTemp in operators:
            operatorStr += char
        else:
            inputFile.seek(inputFile.tell() - 1, 0)

    output.append(["OPERATOR", operatorStr])

def processAlpha(str, outputFile):
    output.append(["IDENTIFIER", str])

def processDigit(str, outputFile):
    output.append(["INTEGER", str])


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

            # Handles comments
            if char == "[":
                char = inputFile.read(1)
                if char == "*":
                    commentFlag = True
                else:
                    inputFile.seek(inputFile.tell() - 1, 0)

            if char == "*" and commentFlag:
                char = inputFile.read(1)
                if char == "]":
                    commentFlag = False
                    char = inputFile.read(1)
                else:
                    inputFile.seek(inputFile.tell() - 1, 0)
            
            if commentFlag:
                continue

            if isSeparator(char):
                processSeparator(char, outputFile)
                continue

            if isOperator(char):
                processOperator(char, inputFile, outputFile)
                continue

            if char.isalpha():
                str += char

                char = inputFile.read(1)
                if isOperator(char) or isSeparator(char) or char.isspace():
                    processAlpha(str, outputFile)
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
                    processDigit(str, outputFile)
                    str = ""
                    inputFile.seek(inputFile.tell() - 1)
                    continue
                else:
                    inputFile.seek(inputFile.tell() - 1)
                    continue

        outputFile.write("{:<{width}}{}\n\n".format("TOKENS", "LEXEMES", width=30))
        
        for entry in output:
            outputFile.write("{:<{width}}{}\n".format(entry[0], entry[1], width=30))

if __name__ == "__main__":
    main()
















