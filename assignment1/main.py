import sys

def isOperator(char):
    operators = ['==', '!=', '>', '<', '<=', '=>', '+', '-', '*', '/', '=']
    return char in operators

def isSeparator(char):
    separators = ['$', '(', ')', '{', '}', ';', ',']
    return char in separators

def processSeparator(char, outputFile):
    print(f"SEPARATOR: {char}")
    outputFile.write(f"SEPARATOR: {char}\n")

def processOperator(char, inputFile, outputFile):
    operatorStr = ""
    operatorStr += char

    if char == "!" or char == "=" or char == "<":
        char = inputFile.read(1)
        if char == "=" or char == ">":
            operatorStr += char
        else:
            inputFile.seek(inputFile.tell() - 1, 0)

    print(f"OPERATOR: {operatorStr}")
    outputFile.write(f"OPERATOR: {operatorStr}\n")

def processAlpha(str, outputFile):
    print(f"IDENTIFIER/KEYWORD: {str}")
    outputFile.write(f"IDENTIFIER/KEYWORD: {str}\n")

def processDigit(str, outputFile):
    print(f"INTEGER/REAL: {str}")
    outputFile.write(f"INTEGER/REAL: {str}\n")


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

if __name__ == "__main__":
    main()
















