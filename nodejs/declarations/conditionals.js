// Syntax guide - Conditionals
//
// Javascript has the following conditional statements:
// if: it is used to specify a block of code to be executed, if a specified condition is true
// else: it is used to specify a block of code to be executed, if the same condition is false
// else if: it is used to specify a new condition to test, if the first condition is false
//

// if statement
//

let word = "dog";
if (word == "dog") {
    console.log("It is the same word");
}

if (word === "dog") {
    console.log("It is the same word and type");
}

let isTrue = true;
if (isTrue) {
    console.log('The variable value is true');
}

// else statement
//

let isFalse = false;
if (isFalse) {
    console.log("The variable value is true");
} else {
    console.log("The variable value is false");
}

// else if statement
//

let color = "green";
if (color === "red") {
    console.log("It is a red color and string type");
} else if (color === "green") {
    console.log("It is a green color and string type");
} else {
    console.log("It is a red color and string type")
}