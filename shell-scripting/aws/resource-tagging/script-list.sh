#!/bin/bash

# Reads the arn resources
input="./arns.txt"

# Counter variable
counter=0

# Loop that reads the arns.txt
while read -r line
do
	
	# Consult the resource tags
	command=$(aws resourcegroupstaggingapi get-resources --resource-arn "$line")
	let counter++
	echo -e "$counter. $command $line\n"

# Ends loop
done < "$input"
