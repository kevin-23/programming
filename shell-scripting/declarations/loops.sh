#!/bin/sh

# Basic loop
for m in 1 2 3
do
	echo $m
done	

# For loop from 0 to 5
for x in `seq 0 5`
do
	echo "The x value is $x"
done

# For loop to get the direcotires in ~/
for i in $(ls ~/)
do
	echo $i
done

# For loop with multiple values
for j in hello 1 * 2 goodbye
do
  echo "Looping ... i is set to $j"
done

# A condition in a while loop
COUNTER1=0
while [ $COUNTER1 -ne 10 ]
do
	echo "The counter is $COUNTER1"
	COUNTER1=`expr $COUNTER1 + 1`
done

# Infinite while loop
while :
do
	echo "Please type something in (^C to quit)"
	read INPUT_STRING
	echo "You typed: $INPUT_STRING"
done
