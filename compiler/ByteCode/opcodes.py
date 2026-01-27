from enum import Enum, auto

class OpCode(Enum):

    # --- Stack ---
    PUSH_CONST = auto()      # push constant onto stack
    POP = auto()             # pop top of stack
    DUP = auto()             # duplicate top value

    # --- Variables ---
    LOAD_VAR = auto()        # push variable value
    STORE_VAR = auto()       # store stack top into variable

    # --- Arithmetic ---
    ADD = auto()             # addition
    SUB = auto()             # subtraction
    MUL = auto()             # multiplication
    DIV = auto()             # division
    NEG = auto()             # unary minus

    # --- Comparison ---
    EQ = auto()              # equal
    NEQ = auto()             # not equal
    GT = auto()              # greater than
    GTE = auto()             # greater than or equal
    LT = auto()              # less than
    LTE = auto()             # less than or equal

    # --- Boolean / Logic ---
    NOT = auto()
    AND = auto()             # short-circuit handled by jumps
    OR = auto() 

    # --- Control Flow ---
    JUMP = auto()            # unconditional jump
    JUMP_IF_FALSE = auto()   # pop condition, jump if false
    JUMP_IF_TRUE = auto()    # pop condition, jump if true

    # --- Functions ---
    CALL = auto()            # call function
    RETURN = auto()

    # --- Loops ---
    ITER_INIT = auto()       # initialize iterator
    ITER_NEXT = auto()       # get next value
    ITER_END = auto()        # stop iteration

    # --- Arrays ---
    BUILD_ARRAY = auto()     # build array from N stack values
    BUILD_RANGE = auto()     # build range from two stack values
    INDEX_GET = auto()       # get array index
    INDEX_SET = auto()       # set array index

    # --- Builtins ---
    PRINT = auto()           # print top of stack   

    # --- Program ---
    HALT = auto()            # stop execution