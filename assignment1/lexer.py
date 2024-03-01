# integer FSM

# real FSM


# psuedocode
# function DFSM (w : string)  // w = omega, some string
# // hard code transitions into table
# table = array [1..nstates, 1..nalphabets] of integer; /* Table N for the transitions*/  
# {  
# state = 1; (the starting state)  
# // assume omega is size of 5 characters, then we will loop 5 times
# // for i to length of omega, can also use while loop i <= length of omega
# for i = to length (w) do  
# 	{  
# 	// char to col, given a character, what column is it, a = 1
# 	col = char_to_col (w[i]);  
# 	// get new state???
# 	state = table[state, col];  
# 	}  
# // accepting state
# if state is in F then return 1 /* accept */  
# else return 0  
# }  

# Note: the function char_to_col(ch) returns the column number of  
# the ch in the table 13


# integer-real fsm
def char_to_col_intreal(char):
    if char.isdigit():
        return 1  # Column for digits
    elif char == '.':
        return 2  # Column for decimal point
    else:
        return 3  # Column for other characters, end probably
    
def char_to_col_identifier(char):
    if char.isalpha():
        return 1  # Column for digits
    elif char.isdigit():
        return 2  # Column for decimal point
    elif char == "_":
        return 3
    else:
        return 0  # Column for other characters, false


def int_realDFSM(str):
    # Starting state
    state = 1

    # Transition table for both integer and real DFAs, including illegal column
    transition_table = [
        # 0, d, ., illegal
        [0, 1, 2, 0],
        [1, 2, 0, 0],
        [2, 2, 3, 0],
        [3, 4, 0, 0],
        [4, 4, 0, 0],
        [5, 5, 5, 5]

    ] # do i need to add a 5, even if it goes to nothing???

    # Accepting states
    accepting_states = [2, 4]

    # Iterate through the characters and transition through DFSM
    for char in str:
        # if char is other tokens, end with current state
        col = char_to_col_intreal(char)
        # print(state, col)
        state = transition_table[state][col] # get new state based on current state and column associated
        # print(char, state, "\n")
        if state == 0:
            return "Invalid Token"
        
    # # Track the index of the current character
    # index = 0

    # # Iterate through the characters and transition the DFA
    # while index < len(str):
    #     char = str[index]
    #     col = char_to_col(char)
    #     next_state = transition_table[state][col]
        
    #     # Check if the next state is a failing state
    #     if next_state == 0:
    #         # Backtrack by one character
    #         index -= 1
    #         break

    #     state = next_state
    #     index += 1

    # Check if the final state is an accepting state
    if state in accepting_states:
        if '.' in str:  # If the token contains a decimal point, it's a real number
            return "REAL"
        else:
            return "INTEGER"
    else:
        return "Invalid Token"
    
    # alternatively:
    # if state == 4:
    #     return "REAL"
    # elif state == 2:
    #     return "INTEGER"
    # else:
    #     return "Invalid Token"

# terminate once it sees the plus since theresno digit

# Test cases
print(int_realDFSM("2738682fksfkhue234.67"))  # Output: Invalid Token
print(int_realDFSM("1234"))  # Output: INTEGER
print(int_realDFSM("12.34"))  # Output: REAL
print(int_realDFSM("abc"))  # Output: Invalid Token
print(int_realDFSM("123+123"))  # Output: Invalid Token

# identifier FSM
def identifierDFSM(str):
    
    transition_table = [
        # l, d, _
        [0, 1, 2, 3],
        [1, 2, 0, 0],
        [2, 3, 4, 0],
        [3, 3, 4, 0],
        [4, 3, 4, 0],
    ]

    # Starting state
    state = 1

    # Accepting states
    accepting_states = [2, 3, 4, 5, 6]

    # Iterate through the characters and transition through DFSM
    for char in str:
        col = char_to_col_identifier(char)
        print("state:", state, "col:", col)
        state = transition_table[state][col]
        print("char:", char, "state:", state)

    if state in accepting_states:
        return "IDENTIFIER"
    else:
        return "INVALID TOKEN"
    
print("\n")
print(identifierDFSM("Great"))  # Output: INTEGER
print(identifierDFSM("_bruh_"))  # Output: REAL
print(identifierDFSM("abc"))  # Output: Invalid Token
print(identifierDFSM("hello_bye"))  # Output: Invalid Token
