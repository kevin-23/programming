#!/bin/sh

# Using a case in a conversation
echo "Please talk to me ..."

# Declare a loop simulating a menu
while :
do
  read INPUT_STRING
  
  # The case is waiting to be matched with 
  # the INPUT_STRING variable
  case $INPUT_STRING in
	hello)
		echo "Hello yourself!"
		;;
	bye)
		echo "See you again!"
		break
		;;
	*)
		echo "Sorry, I don't understand"
		;;
  esac
done
echo 
echo "That's all folks!"
