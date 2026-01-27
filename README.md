# Rayvn Language Documentation (v0.1)

Rayvn is a small programming language that compiles to bytecode and runs on a custom stack-based virtual machine.

This document describes **only what is currently implemented and working**.

---

## Table of Contents

- Overview
- Program Structure
- Comments
- Variables
- Data Types
- Output
- Operators
- Control Flow
- Loops
- For-In Iteration
- Functions
- Arrays
- Strings
- Indexing
- Ranges
- Execution Model
- Current Limitations
- Roadmap

---

## Overview

Rayvn programs execute top-to-bottom.  
There is no implicit `main` function — top-level code runs immediately.

```rayvn
let x = 10
log x
```

---

## Program Structure

Statements are separated by newlines.  
Blocks are defined using `{}`.

```rayvn
if true {
    log 1
}
```

---

## Comments

### Single-line comments

```rayvn
** this is a comment
```

### Multi-line comments

```rayvn
***
this is
a multi-line
comment
***
```

Comments are ignored by the lexer.

---

## Variables

### Declaration

Variables are declared using `let`.

```rayvn
let x = 5
let name = "Rayvn"
```

### Assignment

```rayvn
x = x + 1
```

Reassigning an undeclared variable is a runtime error.

---

## Data Types

Rayvn currently supports:

- Number (integer)
- Boolean (`true`, `false`)
- String
- Array
- Range
- Function

All type checking happens at runtime.

---

## Output

Use `log` to print values.

```rayvn
log 123
log "hello"
log true
```

---

## Operators

### Arithmetic

```text
+   -   *   /
```

### Comparison

```text
==  !=  >  <  >=  <=
```

### Logical

```text
and
or
not
&&
||
!
```

Logical operators return booleans.

---

## Control Flow

### If / Else If / Else

```rayvn
if x > 10 {
    log "big"
}
elseif x > 5 {
    log "medium"
}
else {
    log "small"
}
```

Conditions must evaluate to a boolean.

---

## Loops

### While Loop

```rayvn
let x = 0

while x < 5 {
    log x
    x = x + 1
}
```

### Break

```rayvn
while true {
    break
}
```

### Continue

```rayvn
while true {
    continue
}
```

Using `break` or `continue` outside a loop raises a runtime error.

---

## For-In Iteration

Rayvn supports iteration over iterable values.

```rayvn
for i in range(0, 5, 1) {
    log i
}
```

Supported iterables:

- Range
- Array
- String

Iterating a non-iterable value raises a runtime error.

---

## Functions

### Definition

```rayvn
fn add(a, b) {
    return a + b
}
```

### Calling Functions

```rayvn
let result = add(3, 4)
log result
```

### Return

```rayvn
fn example() {
    return 10
}
```

If a function does not explicitly return a value, it returns `null`.

Returning outside a function is a runtime error.

---

## Arrays

### Array Literals

```rayvn
let nums = [1, 2, 3]
```

### Indexing

```rayvn
log nums[0]
```

### Assignment

```rayvn
nums[1] = 99
log nums
```

Arrays are mutable.

---

## Strings

### Declaration

```rayvn
let greeting = "Hello"
```

### String Indexing

```rayvn
log greeting[0]   // "H"
```

### String Iteration

```rayvn
for char in greeting {
    log char
}
```

Strings are iterable but immutable.

---

## Indexing

Indexing is supported for:

- Arrays
- Strings
- Numbers (digit indexing)

### Number Indexing

```rayvn
let n = 1345
log n[0]   // 1
log n[2]   // 4
```

Index must be an integer.

---

## Ranges

Ranges are created using:

```rayvn
range(start, end, step)
```

Examples:

```rayvn
range(0, 10, 1)
range(5, 0, -1)
```

Ranges are iterable and lazily evaluated.

---

## Execution Model

Rayvn uses:

- A bytecode compiler
- A stack-based virtual machine
- A call stack for function execution
- A per-function variable environment

Key VM concepts:

- Operand stack
- Instruction pointer (`ip`)
- Call stack (`return address + environment`)
- Loop patching for `break` / `continue`

---

## Current Limitations

- Integers only (no floats)
- No objects or structs
- No dictionaries / maps
- No closures
- No modules or imports
- No standard library beyond `log` and `range`
- No error recovery (runtime errors halt execution)

---

## Roadmap

Planned future features:

- Garbage collection
- Closures
- User-defined types
- Standard library
- Better error messages
- REPL
- Bytecode disassembler
- Debugger
- Optimizations

---

## Status

Rayvn is currently a **fully working educational language** with:

- Lexer
- Parser
- AST
- Bytecode compiler
- Stack-based virtual machine

Everything documented above is implemented and functional.# Rayvn
