# CPSC 323
# Spring 2024
# Connie Zhu, Sandra Nguyen, Dylan Nguyen

keywords = ["integer", "boolean", "real", "if", "else", "endif", "while", "print", "return", "scan", "endwhile", "true", "false", "function"]

# integer-real fsm
def char_to_col_intreal(char):
    if char.isdigit():
        return 1  # Column for digits
    elif char == '.':
        return 2  # Column for decimal point
    else:
        return 3  # Column for other characters, illegal

def int_realDFSM(str):
    # Starting state
    state = 1

    # Transition table for both integer and real DFAs, including illegal column
    transition_table = [
        # illegals redirected to third column
        
        #   d, ., other
        [0, 1, 2, 3], # labels
        [1, 2, 5, 5], # state = 1
        [2, 2, 3, 5], # state = 2
        [3, 4, 5, 5], # state = 3
        [4, 4, 5, 5], # state = 4
        [5, 5, 5, 5]  # state = 5  
    ] 

    # Accepting states
    accepting_states = [2, 4]

    # Iterate through the characters and transition through DFSM
    for char in str:
        # returns column based on whether digit or '.'
        col = char_to_col_intreal(char)
        # print("state:", state, "col:", col)
        state = transition_table[state][col] # get new state based on current state and column associated
        # print("char:", char, "state:", state)

    # Check if the final state is an accepting state
    if state in accepting_states:
        if '.' in str:  # If the token contains a decimal point, it's a real number
            return "REAL"
        else:
            return "INTEGER"
    else:
        return "INVALID TOKEN"

def char_to_col_identifier(char):
    if char.isalpha():
        return 1  # Column for digits
    elif char.isdigit():
        return 2  # Column for decimal point
    elif char == "_":
        return 3
    else:
        return 4  # Column for other characters, illegal

# identifier FSM
def identifierDFSM(str):
    # Starting state
    state = 1

    transition_table = [
        #   l, d, _, other
        [0, 1, 2, 3, 4],
        [1, 2, 6, 6, 6], # state = 1
        [2, 3, 4, 5, 6], # state = 2
        [3, 3, 4, 5, 6], # state = 3
        [4, 3, 4, 5, 6], # state = 4
        [5, 3, 4, 5, 6], # state = 5
        [6, 6, 6, 6, 6]  # state = 6
    ]

    # Accepting states
    accepting_states = [2, 3, 4, 5]

    # Iterate through the characters and transition through DFSM
    for char in str:
        col = char_to_col_identifier(char)
        # print("state:", state, "col:", col)
        state = transition_table[state][col]
        # print("char:", char, "state:", state)

    if state in accepting_states:
        if str in keywords:
            return "KEYWORD"
        else:
            return "IDENTIFIER"
    else:
        return "INVALID TOKEN"