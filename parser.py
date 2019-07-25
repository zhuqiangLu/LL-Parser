import sys
#draw the parse table
#this parse table will take each terminal as a string since it keeps 'if' 'print' as a terminal
#use dictionary to represent the table
L ={
"(" : "ER",
"a" : "ER",
"b" : "ER",
"c" : "ER",
"d" : "ER",
"0" : "ER",
"1" : "ER",
"2" : "ER",
"3" : "ER"
}

R = {
"(" : "ER",
"a" : "ER",
"b" : "ER",
"c" : "ER",
"d" : "ER",
"0" : "ER",
"1" : "ER",
"2" : "ER",
"3" : "ER",
"$" : "",
")" : ""
}

E = {
"(" : "(W",
"a" : "V",
"b" : "V",
"c" : "V",
"d" : "V",
"0" : "T",
"1" : "T",
"2" : "T",
"3" : "T"
}

#W IS C PRIME
W = {
"if" : "C)",
"+" : "F)",
"-" : "F)",
"*" : "F)",
"print" : "F)"
}

C = {
"if" : "ifEEX"
}

#x IS C PRIMe
X ={
"(" : "E",
")" : "",
"a" : "E",
"b" : "E",
"c" : "E",
"d" : "E",
"0" : "E",
"1" : "E",
"2" : "E",
"3" : "E"
}

F = {
"+" : "+L",
"-" : "-L",
"*" : "*L",
"print" : "printL"
}

V ={
"a" : "a",
"b" : "b",
"c" : "c",
"d" : "d"
}

T = {
"0" : "0",
"1" : "1",
"2" : "2",
"3" : "3"
}

RULES = {
"L" : L,
"E" : E,
"R" : R,
"W" : W,
"C" : C,
"X" : X,
"F" : F,
"V" : V,
"T" : T,

}
#tokenize terminal,
def token(inputString):
    if inputString[:1] == "(":
        return "("

    elif inputString[:1] == ")":
        return ")"

    elif inputString[:1] == "a":
        return "a"

    elif inputString[:1] == "b":
        return "b"

    elif inputString[:1] == "c":
        return "c"

    elif inputString[:1] == "d":
        return "d"

    elif inputString[:1] == "0":
        return "0"

    elif inputString[:1] == "1":
        return "1"

    elif inputString[:1] == "2":
        return "2"

    elif inputString[:1] == "3":
        return "3"

    elif inputString[:1] == "+":
        return "+"

    elif inputString[:1] == "-":
        return "-"

    elif inputString[:1] == "*":
        return "*"

    elif inputString[:1] == "$":
        return "$"

    elif inputString[:1] == "L":
        return "L"

    elif inputString[:1] == "R":
        return "R"

    elif inputString[:1] == "E":
        return "E"

    elif inputString[:1] == "W":
        return "W"

    elif inputString[:1] == "C":
        return "C"
    elif inputString[:1] == "X":
        return "X"
    elif inputString[:1] == "F":
        return "F"
    elif inputString[:1] == "V":
        return "V"
    elif inputString[:1] == "T":
        return "T"
    elif inputString[:1] == "$":
        return "$"
    elif inputString[:1] == "i":
        if inputString[:2] == "if":
            return "if"
        else:
            return False

    elif inputString[:1] == "p":
        if inputString[:5] == "print":
            return "print"
        else:
            return False
    elif inputString[:1] == "":
        return ""
    else:
        return False
#check whether the first element of the input is a terminal
def isVariables(inputToken):
    if(inputToken == 'L' or
    inputToken == 'R' or
     inputToken == 'E' or
     inputToken == 'W' or
     inputToken == 'C' or
     inputToken == 'X' or
     inputToken == 'F' or
     inputToken == 'T' or
     inputToken == 'V'):
        return True
    else:
        return False

def readFile(path):
    f = open(path, 'r')
    inputString = ""
    lines = f.readlines()
    for line in lines:
        inputString += line.replace('\n', '')
    inputString += '$'
    return inputString

def endOfStack(inputString):
    head = token(inputString)
    if(head == '$' and len(inputString) == 1):
        return True
    else:
        return False

def colourRed(text):
    RED = '\033[91m'
    ENDC = '\033[0m'
    return RED + text + ENDC

def colourGreen(text):
    Green = '\033[92m'
    ENDC = '\033[0m'
    return Green + text + ENDC

def compareChange(number_modification_insert, changes, stack, key):

    if(number_modification_insert == None or number_modification_insert == -1):
        number_modification_insert = changes
        stack.append(key)
    else:
        if(changes < number_modification_insert):
            number_modification_insert = changes
            stack = []
            stack.append(key)
        if(changes == number_modification_insert):
            number_modification_insert = changes
            stack.append(key)
    return number_modification_insert, stack

def endSymbolInInput(inputToken, stackToken, inputString, stackString,  number_modification):
    #special case: when the input contain $: can only be deleted
    number_least_modification = None
    stack = []

    #see how many changes it will lead to
    delete =  parseSimulator(inputString[1:], stackString, number_modification)

    #within 5
    if(delete != None):

        number_least_modification = delete + 1
        stack.append("delete")

    else:

        return None,None

    return stack, number_least_modification

def emptyStackNotEmptyInput(inputToken, stackToken, inputString, stackString,  number_modification):

    number_least_modification = None
    stack = []
    #see how many changes it needs if user delete the head of the input
    changes =  parseSimulator(inputString[len(stackToken):], stackString, number_modification)
    if(changes != None):

        number_least_modification = changes + 1
        stack.append("delete")

    else:
        return None,None

    return stack, number_least_modification

def emptyInputNotEmptyStack(inputToken, stackToken, inputString, stackString,  number_modification):

    number_modification += 1
    number_least_modification = None
    stack = []

    try:
            keys = RULES[stackToken].keys()


            for key in keys:
                #try every expected symbol

                insert = parseSimulator(key + inputString,  stackString, number_modification)

                #compare the changes of inserting each symbol

                if(insert != None):
                    insert += 1

                    number_least_modification, stack = compareChange(number_least_modification, insert, stack, key)





    except:

        #for the case that the expected symbol is ')' sicne it is not a key of the dictionary
        insert = parseSimulator(stackToken + inputString,  stackString, number_modification)

        if(insert != None):
            insert = insert + 1
            if(number_least_modification == None):
                number_least_modification = insert
                stack.append(stackToken)

    return stack, number_least_modification

def bothNotEmpty(inputToken, stackToken, inputString, stackString,  number_modification):
    number_modification += 1
    number_modification_delete = -1
    number_modification_insert = -1
    number_least_modification = None
    stack = []

    try:

        #first try to delete the unexpected symbol
        delete = parseSimulator(inputString[len(inputToken):], stackString, number_modification)

        #if deleting the unexpected symbol works, record the minimum changes it needs
        if(delete != None):
            number_modification_delete = 1 + delete

        #to remove the $ as it might be the wanted symbol
        if "$" in RULES[stackToken].keys():
            keys = RULES[stackToken].keys().remove("$")
        else:
            keys = RULES[stackToken].keys()


        for key in keys:


            #try all wanted symbols
            insert = parseSimulator(key + inputString ,stackString, number_modification)


            if(insert != None):
                insert += 1
                number_modification_insert, stack = compareChange(number_modification_insert, insert, stack, key)



        if(number_modification_insert != -1):
            number_least_modification = number_modification_insert


        #compare the least modification number with the changes required by inserting each expected symbol
        if(number_modification_delete == number_modification_insert and number_modification_insert != -1):
            number_least_modification = number_modification_insert
            stack.append("delete")

        if(number_modification_delete < number_modification_insert and number_modification_delete != -1):
            number_least_modification = number_modification_delete
            stack = []
            stack.append("delete")

    except Exception as e:
        #if this symbol is not found in the table, it must be an invalid symbol
        if(inputToken == False):
            delete = parseSimulator(inputString[1:], stackString, number_modification)
        else:
            delete = parseSimulator(inputString[len(inputToken):], stackString, number_modification)
        if(delete != None):
            number_modification_delete = 1 + delete
            number_least_modification = number_modification_delete
            stack.append("delete")

            #print( number_modification_delete ,number_modification_insert,number_modification_delete, insert)

    return stack, number_least_modification

def suggest(inputToken, stackToken, inputString, stackString,  number_modification):

    #If 5 changes have already made in previous step, then abort this run
    if number_modification >= 5:
        return None, None

    #special case: when the input contain $: can only be deleted
    if(inputToken == "$" and len(inputString) != 1):

        stack, number_least_modification = endSymbolInInput(inputToken,
                                                            stackToken,
                                                            inputString,
                                                            stackString,
                                                            number_modification)


    #can only delete input when the stack is empty
    elif(not endOfStack(inputString) and endOfStack(stackString)):

        stack, number_least_modification = emptyStackNotEmptyInput(inputToken,
                                                                   stackToken,
                                                                   inputString,
                                                                   stackString,
                                                                   number_modification)

    #can only add input when the input string is empty when the stack is not
    elif(endOfStack(inputString) and not endOfStack(stackString)):

        stack, number_least_modification = emptyInputNotEmptyStack(inputToken,
                                                                   stackToken,
                                                                   inputString,
                                                                   stackString,
                                                                   number_modification)
    #if both input and the stack are not empty, then try delete and insert expected symbol
    else:
        stack, number_least_modification =bothNotEmpty(inputToken,
                                                       stackToken,
                                                       inputString,
                                                       stackString,
                                                       number_modification)

    return stack, number_least_modification

def errorRecovery(inputToken, stackToken, inputString, stackString):
    keys = []
    # make sure it is not the end of the stack
    if(not endOfStack(inputString) and not endOfStack(stackString) and inputToken != "$"):

        #since ')' is not a key, it cannot be found using RULES
        if(stackToken != ")"):
            keys = RULES[stackToken].keys()
            counter = len(keys)

            if(inputToken != False and not isVariables(inputToken) ):
                print("Error: got "+ inputToken +  ", but expect {", end = "")

            else:
                print("Error: got  unexpected symbol, but expect {", end = "")
            for key in keys:
                if counter > 1:
                    print(key + ",", end = " ")
                else:
                    print(key + "}" )

                counter -= 1


        else:
                print("Error: got "+ inputToken +  ", but expect { ) }")

    elif( inputToken == "$" and len(inputString) != 1):
        print("Error: got $ before input stack is empty")



    suggest_list, best = suggest(inputToken, stackToken, inputString, stackString, 0)

    #there is not best suggestion
    if(best != None):
        suggest_list = set(suggest_list)
        if 'delete' not in suggest_list:
            print("Recommended correction: insert one of the ", suggest_list)
        else:
            print("Recommended correction: ", end = "")
            suggest_list.remove('delete')
            if(len(suggest_list) != 0):
                print(" insert one of the ", suggest_list, 'or delete')
            else:
                print('delete')


        print("This correction will lead to ", best, " changes")

    else:
        print("Recommend to ABORT this parsing,\nsince all suggestion will lead to more than 5 change ")

    keyword = input(colourRed("Delete") + " or " + colourGreen("Insert") +" input? " )

    keyList = keyword.split()
    if len(keyList) == 0:
        return None
    elif(keyList[0].lower() == "delete"):
        if(inputToken == False):
            inputString = inputString[1:]
        else:
            inputString = inputString[len(inputToken):]
        return inputString

    elif(keyList[0].lower() == "insert"):
        if(len(keyList) >= 2):
            inputString = keyList[1] + inputString
        elif(len(keyList) == 1):
            insert_symbol = input('please enter a symbol to insert: ')
            inputString = insert_symbol + inputString
        return inputString
    else:
        return None

#simply the parser
def parseSimulator(inputString, stackString, number_modification):

    while(1):
        inputToken = token(inputString)
        stackToken = token(stackString)

        #if they both hit the end
        if(endOfStack(inputString) and endOfStack(stackString)):
            return 0

        #it is possible that user enter somthing contains Variables
        if(inputToken == stackToken and not isVariables(inputToken) and not endOfStack(inputString) and inputToken != "$"):

            inputString = inputString[len(inputToken) :]
            stackString = stackString[len(stackToken) :]
            continue
        else:
            #if there is not rule for this variable when it gets this symbol, ask for suggestion
            try:
                temp = RULES[stackToken][inputToken]
                stackString = temp + stackString[len(stackToken):]

            except:
                suggest_list, best_number = suggest(inputToken, stackToken, inputString, stackString, number_modification)
                return best_number

def evaluator(inputToken, stackToken, inputString, stackString):
    if(errorRecov):
        ret = errorRecovery(inputToken, stackToken, inputString, stackString)
        if(ret == None):
            print("REJECTED")
            return None
        else:
            inputString = ret
            return inputString

    else:
        print("REJECTED")
        return None

def parse(inputString, stackString):

    AcceptedString = ""
    while(1):

        if(inputString == None):
            break
        #extract the first e,eme
        inputToken = token(inputString)
        stackToken = token(stackString)

        print(inputString + "   " + stackString )

        #when it is running in errorRecovery mode, then it should not reject an invalid symbol(leave this to user)
        if(not errorRecov):
            #if the first element of the input cannot be recognized or is a variable
            if(inputToken == False or isVariables(inputToken)):
                print("ERROR_INVALID_SYMBOL")
                break

        #when the both input and stack are empty: accpeted
        #unless the input string contains $
        if( endOfStack(inputString) and endOfStack(stackString)):
            print("ACCEPTED", AcceptedString)
            break

        #eliminate the same heads
        if(inputToken == stackToken):

            if((endOfStack(inputString)) or (isVariables(inputToken)) ):
                #use evaluator to check whether it is rejected
                inputString = evaluator(inputToken, stackToken, inputString, stackString)

            else:
                #pop the heads from both satck
                inputString = inputString[len(inputToken) :]
                stackString = stackString[len(stackToken) :]
                AcceptedString += inputToken
                continue

        #if heads are different
        else:

            #see if the input can be parsed
            try:
                #got $ before input reaches end
                if(inputToken == '$' and len(inputString) != 1):
                    inputString = evaluator(inputToken, stackToken, inputString, stackString)
                else:
                    temp = RULES[stackToken][inputToken]
                    stackString = temp + stackString[len(stackToken):]

            #got unexpected symbol from input
            except:
                inputString = evaluator(inputToken, stackToken, inputString, stackString)


inputString = ""
stackString= ""
errorRecov = False

#check command line argument number
try:
    inputString = readFile(sys.argv[1])
    stackString = "L$"
except:
    print("Cannot find input file")
    exit()


if len(sys.argv) == 3:
    stackString = "L$"
    if sys.argv[2] == "error":
        errorRecov = True
        print("Running in error recovery mode")
    else:
        print("This program is not running in error recovery mode")


#remove all the whitespace in inputToken
inputString = inputString.replace(" ", "")
parse(inputString, stackString)
