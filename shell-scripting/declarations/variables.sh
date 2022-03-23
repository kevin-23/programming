#!/bin/sh

# Declare a variable
NAME="David"
CMD=`ls`

# Read the variable value
echo "My name's $NAME\nI'll run the command ls\n$CMD"

# Curly brackets
echo "I will create a ${NAME}_file"

# Local variable 
HELLO="Hello" 

hello(){ 
    local HELLO="World"
    echo $HELLO
}

# Print the values
echo $HELLO
hello
