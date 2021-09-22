#*******************************************************************************************************

##     #####  # #   #####   ####  #####  ##       #####  #   #  #####  ##     #   #  #####  #####  #####
##     ##     # #     #    ##     #   #  ##       #   #  ##  #  #   #  ##      # #      #   ##     ##  #
##     ####    #      #    ##     #####  ##       #####  # # #  #####  ##       #      #    ####   #####
##     ##     # #     #    ##     #   #  ##       #   #  #  ##  #   #  ##       #     #     ##     ## #
#####  #####  # #   #####   ####  #   #  #####    #   #  #   #  #   #  #####    #    #####  #####  ##  #

#*******************************************************************************************************
class LexicalAnalyzer:
    def __init__(self):
        self.state_table = [
             #   0    1    2    3    4    5    6
             #   l    d    $/_  Sp   .    Op   Space
                [1,   1,   1,   1,   1,   1,   1], # 0
                [2,   3,   0,   6,   4,   7,   1], # 1
                [2,   2,   2,   0,   0,   0,   0], # 2
                [0,   3,   0,   0,   4,   0,   0], # 3
                [0,   5,   0,   0,   0,   0,   0], # 4
                [0,   5,   0,   0,   0,   0,   0], # 5
                [0,   0,   0,   0,   0,   0,   0], # 6
                [0,   0,   0,   0,   0,   0,   0]  # 7
                ]

        self.KEYWORDS = ["int", "float", "bool", "True", "False", "if", "else", "then", "endif", "endelse", "while", "whileend", "do", "enddo", "for", "endfor", "STDinput", "STDoutput", "and", "or", "not", "begin", "end"]

        self.SEPARATORS = ['(', ')', '{', '}', '[', ']', ',', '.', ':', ';']

        self.OPERATORS = ['*', '+', '-', '=', '/', '>', '<', '%']

        self.isComment = False

        self.line_number = 0

    def isKeyword(self, lexeme):
        if lexeme in self.KEYWORDS:
            return True
        return False

    def isSeparator(self, lexeme):
        if lexeme in self.SEPARATORS:
            return True
        return False

    def isOperator(self, lexeme):
        if lexeme in self.OPERATORS:
            return True
        return False

    def isSpace(self, string):
        if string == " " or string == "\n" or string == "\t":
            return True
        return False

    # Returns column number based on character
    def char_to_col(self, c):
        if c.isalpha():
            return 0
        elif c.isdigit():
            return 1
        elif c == '$' or c == '_':
            return 2
        elif c in self.SEPARATORS:
            if c == '.':
                return 4
            else:
                return 3
        elif c in self.OPERATORS:
            return 5
        elif self.isSpace(c):
            return 6
        else:
            return None

    def lexer(self, line):
        col = 0
        curr_state = 1
        prev_state = 1
        token_list = []
        lexeme = ""
        i = 0
        self.line_number += 1

        while i < len(line):
            # Checking for comment
            if line[i] == '!':
                if self.isComment:
                    self.isComment = False
                    if i + 1 != len(line):
                        i += 1
                    else:
                        break
                else:
                    self.isComment = True

            if not self.isComment:
                col = self.char_to_col(line[i])
                if col == None:
                    print("ERROR: Invalid character found in file")
                    return -1

                prev_state = curr_state
                curr_state = self.state_table[curr_state][col]

                # Building lexeme
                if curr_state != 0 and not self.isSpace(line[i]):
                    lexeme += line[i]

                # Identifying token for lexeme
                if curr_state == 0 and lexeme != "":
                    # Keyword
                    if self.isKeyword(lexeme):
                        token_list.append(["KEYWORD", lexeme, self.line_number])
                    # Separator
                    elif prev_state == 6 or self.isSeparator(lexeme):
                        token_list.append(["SEPARATOR", lexeme, self.line_number])
                    # Operator
                    elif self.isOperator(lexeme):
                        token_list.append(["OPERATOR", lexeme, self.line_number])
                    # Integer
                    elif prev_state == 3:
                        token_list.append(["INTEGER", lexeme, self.line_number])
                    # Real
                    elif prev_state == 5:
                        token_list.append(["REAL", lexeme, self.line_number])
                    # Identifier
                    else:
                        token_list.append(["IDENTIFIER", lexeme, self.line_number])

                    # Resetting values
                    lexeme = ""
                    curr_state = 1
                    i -= 1
            i += 1

        return token_list

#************************************************************************************************

 ###   #   #  #   #  #####  #####  # #     #####  #   #  #####  ##     #   #  #####  #####  #####
#       # #   ##  #    #    #   #  # #     #   #  ##  #  #   #  ##      # #      #   ##     ##  #
 ###     #    # # #    #    #####   #      #####  # # #  #####  ##       #      #    ####   #####
    #    #    #  ##    #    #   #  # #     #   #  #  ##  #   #  ##       #     #     ##     ## #
 ###     #    #   #    #    #   #  # #     #   #  #   #  #   #  #####    #    #####  #####  ##  #

#************************************************************************************************

class SyntaxAnalyzer:
    def __init__(self, record):
        self.index = 0
        self.prev_i = -1
        self.print_rules = True

        do = True
        while do:
            self.printInfo(record)
            if self.S(record):
                pass
            else:
                return

            self.index += 1
            if self.index >= len(record):
                do = False

    def forward(self, record):
        self.index += 1
        if self.index >= len(record):
            self.index -= 1
            return False
        if self.index > self.prev_i:
            self.printInfo(record)
            self.prev_i = self.index
        return True

    def printInfo(self, record):
        #if self.print_rules:
        print("\nToken:", record[self.index][0], "\tLexeme:", record[self.index][1])

    # Statement
    def S(self, record):
        if self.print_rules:
            print("\t<Statement> --> <Assign> | <Expression Semicolon> | <Declarative> | <If Statement> | <While Statement> | <Begin Statement>")

        if self.ID(record[self.index][0]):
            if self.index + 1 < len(record):
                if self.A(record):
                    return True
                elif self.E_S(record):
                    return True
            else:
                print("ERROR: Incomplete statement at line", record[self.index][2])
                return False
        elif self.E_S(record):
            return True
        elif self.D(record):
            return True
        elif record[self.index][1] == "if":
            if self.IF_S(record):
                return True
        elif record[self.index][1] == "while":
            if self.WHILE_S(record):
                return True
        elif record[self.index][1] == "begin":
            if self.BEGIN_S(record):
                return True
        else:
            print("ERROR: Invalid statement at line", record[self.index][2])
        return False

    # More statements
    def MORE_S(self, record):
        if self.print_rules:
            print("\t<More Statements> --> ; <Statement> <More Statements> | <Epsilon>")

        if record[self.index][1] == ";":
            if not self.forward(record):
                return False
            if record[self.index][1] == "else" or record[self.index][1] == "endif" or record[self.index][1] == "whileend":
                self.index -= 1
                return True
            if self.S(record):
                if not self.forward(record):
                    return False
                if self.MORE_S(record):
                    return True
            self.index -= 1
        else:
            self.index -= 1
            return True

        print("ERROR: Invalid statement at line", record[self.index][2])
        return False

    # Multiple statements
    def MULTIPLE_S(self, record):
        if self.print_rules:
            print("\t<Multiple Statements> --> <Statement> <More Statements>")

        if self.S(record):
            if self.index + 1 >= len(record):
                return False
            if self.MORE_S(record):
                return True

        print("ERROR: Invalid statement at line", record[self.index][2])
        return False

    # If statement
    def IF_S(self, record):
        if self.print_rules:
            print("\t<If Statement> --> if <Conditional> then <Multiple Statements> <Else Statement> endif")

        if record[self.index][1] == "if":
            if not self.forward(record):
                return False
            if self.C(record):
                if not self.forward(record):
                    return False
                if record[self.index][1] == "then":
                    if not self.forward(record):
                        return False
                    if self.MULTIPLE_S(record):
                        if not self.forward(record):
                            return False
                        if self.ELSE_S(record):
                            if not self.forward(record):
                                return False
                            if record[self.index][1] == "endif":
                                return True
                            else:
                                print("ERROR: Invalid if-statement; missing \"endif\" at line", record[self.index][2])
                            self.index -= 1
                        self.index -= 1
                    self.index -= 1
                else:
                    print("ERROR: Invalid if-statement; missing \"then\" at line", record[self.index][2])
                self.index -= 1
            self.index -= 1

        print("ERROR: Invalid if-statement at line", record[self.index][2])
        return False

    def ELSE_S(self, record):
        if self.print_rules:
            print("\t<Else Statement> --> else <Multiple Statements> | <Epsilon>")

        if record[self.index][1] == "else":
            if not self.forward(record):
                return False
            if self.MULTIPLE_S(record):
                return True
            self.index -= 1
        else:
            self.index -= 1
            return True

        print("ERROR: Invalid else-statement at line", record[self.index][2])
        return False

    # While statement
    def WHILE_S(self, record):
        if self.print_rules:
            print("\t<While Statement> --> while <Conditional> do <Multiple Statements> whileend")

        if record[self.index][1] == "while":
            if not self.forward(record):
                return False
            if self.C(record):
                if not self.forward(record):
                    return False
                if record[self.index][1] == "do":
                    if not self.forward(record):
                        return False
                    if self.MULTIPLE_S(record):
                        if not self.forward(record):
                            return False
                        if record[self.index][1] == "whileend":
                            return True
                        else:
                            print("ERROR: Invalid while-loop. Missing \"whileend\" at line", record[self.index][2])
                            return False
                        self.index -= 1
                    self.index -= 1
                else:
                    print("ERROR: Invalid while-loop. Missing \"do\" at line", record[self.index][2])
                self.index -= 1
            self.index -= 1
        return False

    # Begin statement
    def BEGIN_S(self, record):
        if self.print_rules:
            print("\t<Begin Statement> --> begin <Multiple Statements> end")

        if record[self.index][1] == "begin":
            if not self.forward(record):
                return False
            if self.MULTIPLE_S(record):
                if not self.forward(record):
                    return False
                if record[self.index][1] == "end":
                    return True
                self.index -= 1
            self.index -= 1
        print("ERROR: Invalid begin-statement at line", record[self.index][2])
        return False

    # Conditional
    def C(self, record):
        if self.print_rules:
            print("\t<Conditional> --> <Expression> <Conditional Prime>")

        if self.E(record):
            if not self.forward(record):
                return False
            if self.C_PRIME(record):
                return True
            self.index -= 1
        print("ERROR: Invalid condition at line", record[self.index][2])
        return False

    # Conditional Prime
    def C_PRIME(self, record):
        if self.print_rules:
            print("\t<Conditional Prime> --> <Relop> <Expression> | <Epsilon>")

        if self.R(record):
            if not self.forward(record):
                return False
            if self.E(record):
                return True
            self.index -= 1
        else:
            self.index -= 1
            return True
        return False

    # Relop
    def R(self, record):
        if self.print_rules:
            print("\t<Relop> --> < | <= | == | <> | >= | >")

        # <=, <>, <
        if record[self.index][1] == "<":
            if not self.forward(record):
                return False
            # <=
            if record[self.index][1] == "=":
                return True
            # <>
            elif record[self.index][1] == ">":
                return True
            # <
            else:
                self.index -= 1
                return True
        # ==
        elif record[self.index][1] == "=":
            if not self.forward(record):
                return False
            if record[self.index][1] == "=":
                return True
        # >=, >
        elif record[self.index][1] == ">":
            if not self.forward(record):
                return False
            # >=
            if record[self.index][1] == "=":
                return True
            # >
            else:
                self.index -= 1
                return True

        print("ERROR: Invalid relational operator at line", record[self.index][2])
        return False

    # Expression
    def E(self, record):
        if self.print_rules:
            print("\t<Expression> --> <Term> <Expression Prime>")

        if self.T(record):
            if not self.forward(record):
                return False
            if self.E_PRIME(record):
                return True
            else:
                print("ERROR: Invalid expression at line", record[self.index][2])
            self.index -= 1
        return False

    # Expression Prime
    def E_PRIME(self, record):
        if self.print_rules:
            print("\t<Expression Prime> --> + <Term> <Expression Prime> | - <Term> <Expression Prime> | <Epsilon>")

        if record[self.index][1] == "+" or record[self.index][1] == "-":
            if not self.forward(record):
                return False
            if self.T(record):
                if not self.forward(record):
                    return False
                if self.E_PRIME(record):
                    return True
                self.index -= 1
            self.index -= 1
        else:
            self.index -= 1
            return True
        return False

    # Expression semicolon
    def E_S(self, record):
        if self.print_rules:
            print("\t<Expression Semicolon> --> <Expression> ;")

        if self.E(record):
            if not self.forward(record):
                return False
            if record[self.index][1] == ";":
                return True
            else:
                print("ERROR: Invalid expression; missing \";\" at line", record[self.index][2])
            self.index -= 1
        return False

    # Term
    def T(self, record):
        if self.print_rules:
            print("\t<Term> --> <Factor> <Term Prime>")

        if self.F(record):
            if not self.forward(record):
                return False
            if self.T_PRIME(record):
                return True
            self.index -= 1
        return False

    # Term Prime
    def T_PRIME(self, record):
        if self.print_rules:
            print("\t<Term Prime> --> * <Factor> <Term Prime> | / <Factor> <Term Prime> | <Epsilon>")

        if record[self.index][1] == "*" or record[self.index][1] == "/":
            if not self.forward(record):
                return False
            if self.F(record):
                if not self.forward(record):
                    return False
                if self.T_PRIME(record):
                    return True
                self.index -= 1
            self.index -= 1
        else:
            self.index -= 1
            return True
        return False

    # Factor
    def F(self, record):
        if self.print_rules:
            print("\t<Factor> --> ( <Expression> ) | <Identifier>")

        if record[self.index][1] == "(":
            if not self.forward(record):
                return False
            if self.E(record):
                if not self.forward(record):
                    return False
                if record[self.index][1] == ")":
                    return True
                else:
                    print("ERROR: Invalid factor; missing \")\" at line", record[self.index][2])
                self.index -= 1
            self.index -= 1
        if self.ID(record[self.index][0]):
            return True
        return False

    # Assignment
    def A(self, record):
        if self.print_rules:
            print("\t<Assign> --> <Identifier> = <Expression Semicolon>")

        if self.ID(record[self.index][0]):
            if not self.forward(record):
                return False
            if record[self.index][1] == "=":
                if not self.forward(record):
                    return False
                if self.E(record):
                    if not self.forward(record):
                        return False
                    if record[self.index][1] == ";":
                        return True
                    else:
                        print("ERROR: Invalid assignment; missing \";\" at line", record[self.index][2])
                    self.index -= 1
                self.index -= 1
                print("ERROR: Invalid assignment at line", record[self.index][2])
            self.index -= 1
        return False

    # Declarative
    def D(self, record):
        if self.print_rules:
            print("\t<Declarative> --> <Type> <Identifier> <More IDs> ;")

        if self.TYPE(record):
            if not self.forward(record):
                return False
            if self.ID(record[self.index][0]):
                if not self.forward(record):
                    return False
                if self.M_IDs(record):
                    if not self.forward(record):
                        return False
                    if record[self.index][1] == ";":
                        return True
                    else:
                        print("ERROR: Invalid declaration; missing \";\" at line", record[self.index][2])
                    self.index -= 1
                self.index -= 1
            print("ERROR: Invalid declaration at line", record[self.index][2])
            self.index -= 1
        return False

    # Identifier
    def ID(self, token):
        if token == "IDENTIFIER":
            if self.print_rules:
                print("\t<Identifier> --> id")
            return True
        return False

    # More Identifiers
    def M_IDs(self, record):
        if self.print_rules:
            print("\t<More IDs> --> , <Identifier> <More IDs> | <Epsilon>")

        if record[self.index][1] == ",":
            if not self.forward(record):
                return False
            if self.ID(record[self.index][0]):
                if not self.forward(record):
                    return False
                if self.M_IDs(record):
                    return True
                self.index -= 1
            self.index -= 1
        else:
            self.index -= 1
            return True
        return False

    # Variable type
    def TYPE(self, record):
        if record[self.index][1] == "bool":
            if self.print_rules:
                print("\t<Type> --> bool")
            return True
        elif record[self.index][1] == "float":
            if self.print_rules:
                print("\t<Type> --> float")
            return True
        elif record[self.index][1] == "int":
            if self.print_rules:
                print("\t<Type> --> int")
            return True
        return False

#*********************************

 ###   #####  ##  ##  #####  #####
#   #    #    ##  ##  ##     ##  #
#   #    #    ######  ####   #####
#   #    #    ##  ##  ##     ## #
 ###     #    ##  ##  #####  ##  #

#*********************************

def printTokens(token_list):
    print("{: <20} {: <20} {: <20}".format(*["TOKENS", "LEXEMES", "LINE"]))
    print()
    for token in token_list:
        print("{: <20} {: <20} {: <20}".format(*token))

    print("\nTotal:", len(token_list))

def analyzeFile():
    file_name = input("Input the name of the file you want to open: ")
    print()

    try:
        file = open(file_name, 'r')
    except:
        print("ERROR: File not found")
        return
    print('-'*100)
    print()

    # Lexical Analysis
    token_list = []
    lxr = LexicalAnalyzer()

    for line in file:
        line_tokens = lxr.lexer(line)
        if line_tokens == -1:
            return
        token_list += line_tokens
    file.close()

    #printTokens(token_list)
    #print()
    #print('-'*100)

    # Syntax Analysis
    SyntaxAnalyzer(token_list)

analyzeFile()