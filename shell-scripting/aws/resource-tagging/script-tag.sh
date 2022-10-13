#!/bin/bash
input="./arns.txt"
counter=0
while read -r line
do
	
	command=$(aws resourcegroupstaggingapi tag-resources --resource-arn "$line" --tags environment=dev)
	let counter++
	echo -e "$counter. $command $line\n"

done < "$input"
