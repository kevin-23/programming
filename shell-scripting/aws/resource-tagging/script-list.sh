#!/bin/bash
input="./arns.txt"
counter=0
while read -r line
do
	
	command=$(aws resourcegroupstaggingapi get-resources --resource-arn "$line")
	let counter++
	echo -e "$counter. $command $line\n"

done < "$input"
