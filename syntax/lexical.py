stringFlag = False  # if this flag is true, letter will include in string
integerFlag = False  # if this flag is true, letter will include in integer
beforeIntFlag = False  # if present letter is - and this flag is true, it means
doneFlag = False  # if next character is last character of this token, it turns true
wordFlag = False  # if this token includes in id, keyword, type, it turns true
errorFlag = False  # it detects error

LETTER = []
DIGIT = []
ZERO = ['0']
WHITESPACE = ['\t', '\n', ' ']
MINUS = ['-']
OPERATOR = ['+', '*', '/']
OTHERS = ['(', ')', '{', '}', ',', ';', '"']
COMP = ['<', '>', '=', '!']


for i in range(65, 91):  # setting letter list
    LETTER.append(chr(i))
    LETTER.append(chr(i + 32))
for i in range(49, 58):  # setting digit list
    DIGIT.append(chr(i))


def tokenize(input):
    ret = []
    if stringFlag:  # string token
        ret.append("literal")
        ret.append(input)
    elif integerFlag:  # integer token
        ret.append("num")
        ret.append(input)

    # variable type token
    elif input in ["int", "INT"]:
        ret.append("vtype")
        ret.append("INT")
    elif input in ["char", "CHAR"]:
        ret.append("vtype")
        ret.append("CHAR")

    # keyword token
    elif input in ["if", "IF"]:
        ret.append("if")
    elif input in ["else", "ELSE"]:
        ret.append("else")
    elif input in ["while", "WHILE"]:
        ret.append("while")
    elif input in ["return", "RETURN"]:
        ret.append("return")

    # operator token
    elif input in ['+', '-']:
        ret.append("addsub")
        ret.append(input)
    elif input in ['*', '/']:
        ret.append("multdiv")
        ret.append(input)
    elif input == '=':
        ret.append("assign")

    # compare operation token
    elif input == "<":
        ret.append("comp")
        ret.append("<")
    elif input == ">":
        ret.append("comp")
        ret.append(">")
    elif input == "<=":
        ret.append("comp")
        ret.append("<=")
    elif input == ">=":
        ret.append("comp")
        ret.append(">=")
    elif input == "!=":
        ret.append("comp")
        ret.append("!=")
    elif input == "==":
        ret.append("comp")
        ret.append("==")

    # other character token
    elif input == ";":
        ret.append("semi")
    elif input == ",":
        ret.append("comma")
    elif input == "{":
        ret.append("lbrace")
    elif input == "}":
        ret.append("rbrace")
    elif input == "(":
        ret.append("lparen")
    elif input == ")":
        ret.append("rparen")

    # identifier token
    else:
        ret.append("id")
        ret.append(input)
        beforeIntFlag = True
    output.append(ret)


output = []
string = ""

with open("test.c", "rt") as fin:
    buff1 = fin.read(1)
    while True:
        if buff1 == '':  # if present letter is eof -> break the loop
            break
        buff2 = fin.read(1)  # input the next letter

        if buff1 not in LETTER + DIGIT + ZERO + WHITESPACE + MINUS + OPERATOR + COMP + OTHERS:
            errorFlag = True
            break
        elif buff1 == '"':  # if present letter is double quote, it means start or end of string
            if stringFlag:  # it means it is the end of the string token
                beforeIntFlag = False
                tokenize(string)
                stringFlag = False
            else:  # it means start of the string token
                string = ""
                stringFlag = True
        elif stringFlag:  # if this flag is true, it means it already has double quote
            string += buff1
        elif doneFlag:  # second letter of compare token
            string += buff1
            beforeIntFlag = False
            tokenize(string)
            string = ""
            doneFlag = False
        elif buff1 in LETTER:  # present character is letter
            if wordFlag:  # it will be type, keyword, or id
                string += buff1
            else:  # it is the start of type, keyword, or id
                string = buff1
                wordFlag = True
            if buff2 not in LETTER + ZERO + DIGIT:  # next character does not include in word token
                beforeIntFlag = True
                tokenize(string)
                string = ""
                wordFlag = False
        elif buff1 in ZERO + DIGIT:  # present character is digit or zero
            if integerFlag:  # it includes in integer token value
                string += buff1
                if buff2 not in ZERO + DIGIT:  # next character doesn't include integer token
                    tokenize(string)
                    string = ""
                    integerFlag = False
                    beforeIntFlag = True
            elif wordFlag:  # it includes in id token value
                string += buff1
                if buff2 not in ZERO + DIGIT + LETTER:
                    beforeIntFlag = True
                    tokenize(string)
                    string = ""
                    wordFlag = False
            elif buff1 in ZERO:  # it is ZERO token
                integerFlag = True
                tokenize(buff1)
                beforeIntFlag = True
                integerFlag = False
            else:  # it is the start of integer token value
                string = buff1
                integerFlag = True
                if buff2 not in ZERO + DIGIT:  # next character doesn't include integer token value
                    beforeIntFlag = True
                    tokenize(string)
                    integerFlag = False
        elif buff1 in OPERATOR:  # it is OP token
            beforeIntFlag = False
            tokenize(buff1)
        elif buff1 in MINUS:
            if beforeIntFlag:  # previous token is integer so this minus will be OP token
                tokenize(buff1)
                beforeIntFlag = False
            elif buff2 in ZERO:
                tokenize(buff1)
                beforeIntFlag = False
            else:  # it will be start of negative integer token
                string = buff1
                integerFlag = True
        elif buff1 in OTHERS:  # parenthesis, bracket, comma, semicolon token
            beforeIntFlag = False
            tokenize(buff1)
        elif buff1 in ['<', '>', '!', '=']:  # this character will be the start of token
            string = buff1
            if buff2 == '=':  # it will be two characters token
                doneFlag = True
            else:  # it will be one character token
                beforeIntFlag = False
                tokenize(string)
                string = ""
        buff1 = buff2  # next turn


with open("test.out", "wt") as fout:
    if errorFlag:
        fout.write("Error")
    else:
        for element in output:
            if len(element) == 1:
                buffer = element[0] + "\n"
            else:
                buffer = element[0] + "," + element[1] + "\n"
            fout.write(buffer)
