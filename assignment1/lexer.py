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
def char_to_col(char):
    if char.isdigit():
        return 1  # Column for digits
    elif char == '.':
        return 2  # Column for decimal point
    else:
        return 0  # Column for other characters, end probably

def int_realDFSM(str):
    # Starting state
    state = 1

    # Transition table for both integer and real DFAs
    transition_table = [
        [0, 'd', '.'],
        [1, 2, 0],
        [2, 2, 3],
        [3, 4, 0],
        [4, 4, 0],

    ] # do i need to add a 5, even if it goes to nothing???

    # Accepting states
    accepting_states = [2, 4]

    # Iterate through the characters and transition through DFSM
    for char in str:
        col = char_to_col(char)
        print(state, col)
        state = transition_table[state][col] # get new state based on current state and column associated
        print(char, state, "\n")
        if state == 0:
            return "Invalid Token"

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
    #         return "INTEGER"
    # else:
    #     return "Invalid Token"

# Test cases
print(int_realDFSM("2738682fksfkhue234.67"))  # Output: Invalid Token
print(int_realDFSM("1234"))  # Output: INTEGER
print(int_realDFSM("12.34"))  # Output: REAL
print(int_realDFSM("abc"))  # Output: Invalid Token
print(int_realDFSM("123+123"))  # Output: Invalid Token