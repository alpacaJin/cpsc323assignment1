import sys
from lexer import int_realDFSM, identifierDFSM

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

def processIdentifier(str):
    state = identifierDFSM(str)

    if state == "IDENTIFIER":
        output.append(["IDENTIFIER", str])
    elif state == "KEYWORD":
        output.append(["KEYWORD", str])
    elif state == "INVALID TOKEN":
        print("processIdentifier: invalid token")
        output.append(["INVALID TOKEN", str])

def processIntReal(str):
    state = int_realDFSM(str)

    if state == "INTEGER":
        output.append(["INTEGER", str])
    elif state == "REAL":
        output.append(["REAL", str])
    elif state == "INVALID TOKEN":
        print("processIntReal: invalid token")
        output.append(["INVALID TOKEN", str])

def main():
    inputFileName = input("Enter the input file name (or type exit to exit the program): ")

    if inputFileName == "exit":
        sys.exit(0)
    
    outputFileName = input("Enter the desired output file name (please add .txt): ")

    with open(inputFileName, 'r') as inputFile, open(outputFileName, 'w') as outputFile:

        # Writes source code to terminal and output file
        outputFile.write("SOURCE CODE:\n\n")
        for line in inputFile:
            outputFile.write(f"{line}\n")
        outputFile.write("\n")

        inputFile.seek(0)
        commentFlag = False
        str = ""

        while True:
            char = inputFile.read(1)
            
            if char == "":
                break
            
            print("current char: %s" % char)
            print("current pos: ", inputFile.tell())
            print("current str: %s" % str)
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

            if char.isalnum():
                str += char
                print("is alnum str: %s" % str)

                char = inputFile.read(1)
                print("next char: %s" % char)
                if isOperator(char) or isSeparator(char) or char.isspace():
                    if (any(c.isalpha() for c in str)):
                        print("first")
                        processIdentifier(str)
                    else:
                        print("callingintreal")
                        processIntReal(str)

                    str = ""
                    inputFile.seek(inputFile.tell() - 1)
                    continue
                else:
                    # check for end of alnum
                    if char == "":
                        if (any(c.isalpha() for c in str)):
                            processIdentifier(str)
                        else:
                            print("callingintreal2")
                            print("in not char: %s" % str)
                            processIntReal(str)
                        continue
                    elif not char.isalnum() and char != ".":
                        if (any(c.isalpha() for c in str)):
                            processIdentifier(str)
                        else:
                            print("callingintreal5")
                            processIntReal(str)
                        str = ""
                        inputFile.seek(inputFile.tell() - 1)
                        continue
                    else:
                        inputFile.seek(inputFile.tell() - 1)
                        continue
                    
            if char == ".":
                str += char
                # TODO: if previous was white space or if next was white space, call invalid on the str through int_realDFSM
                print("char: %s" % char)
                # inputFile.seek(inputFile.tell() - 2)
                # prevChar = inputFile.read(1)
                # inputFile.seek(inputFile.tell() + 1)
                print("elif . :%s" % str)
                nextChar = inputFile.read(1)
                # print("prev char: %s" % prevChar)
                print("next char: %s" % nextChar)
                # print("elif . :%s" % str)
                # char2 = inputFile.tell() + 1
                # print("tell: %s" % char2)
                # nextChar is a number, add it to the str
                if nextChar.isalnum() or nextChar == ".":
                    inputFile.seek(inputFile.tell() - 1)
                    continue
                else:
                    # print("callingintreal3")
                    if (any(c.isalpha() for c in str)):
                            processIdentifier(str)
                    else:
                        print("callingintreal2")
                        processIntReal(str)
                    str = ""
                # if nextChar == " ":
                #     print("callingintreal3")
                #     processIntReal(str)
                #     str = ""

                # print("issue?")
                continue
            else:
                # handles every other illegal tokens
                if char.isspace():
                    continue
                print("end else: invalid token: %s" % char)
                output.append(["INVALID TOKEN", char])
                if char == "":
                    print("yay")
            

        outputFile.write("{:<{width}}{}\n\n".format("TOKENS", "LEXEMES", width=30))
        
        for entry in output:
            outputFile.write("{:<{width}}{}\n".format(entry[0], entry[1], width=30))

        print("Source code and tokens have succesfully been written to the output file.")

if __name__ == "__main__":
    main()

