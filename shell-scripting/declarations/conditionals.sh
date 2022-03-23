#!/bin/sh

# Equal to -eq
# Not equal to -ne
# Greater than -gt
# Less than -lt
# Greater than or equal to -ge
# Less than or equal to -le
#
# Type man test in the terminal to obtain more information

# Compare strings
NAME1="Luis"
NAME2="Luis"
if [ $NAME1 = $NAME2 ]
then
	echo "They have the same name" 
elif [ $NAME1 != $NAME2 ]
then
	echo "They do not have the same name"
fi

# Check if the length string is nonzero
WORD1="Hello"
if [ -n $WORD1 ]
then
	echo "The variable WORD1 is nonzero"
fi

# Check if the length string is zero
WORD2=""
if [ -z $WORD2 ]
then
	echo "The variable WORD2 is empty"
fi

# Compare numbers
NUMBER1=85
NUMBER2=50
if [ $NUMBER1 -lt $NUMBER2 ]
then
	echo "$NUMBER1 is less than $NUMBER2"
elif [ $NUMBER1 -gt $NUMBER2 ]
then
	echo "$NUMBER1 is greater than $NUMBER2"
else
	echo "$NUMBER1 is equal to $NUMBER2"
fi

# Validate command result
CMD1=`ls`
CMD2=`ls /`
if [ X"$CMD1" = X"$CMD2" ]
then
	echo $CMD1
else
	echo "The directories are not the same"
fi
