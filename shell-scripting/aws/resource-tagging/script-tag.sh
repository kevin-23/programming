#!/bin/bash

# Reads the arn resources
input="./arns.txt"

# Counter variable
counter=0

# Loops that reads the arns.txt
while read -r line
do
	
	# Tags the resource	
	command=$(aws resourcegroupstaggingapi tag-resources --resource-arn "$line" --tags environment=dev)
	let counter++
	echo -e "$counter. $command $line\n"

# Ends loop
done < "$input"
