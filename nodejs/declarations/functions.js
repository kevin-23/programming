// Syntax guide - Functions
//
// A function is code block designed to perform a particular task
//

// function syntax
//
function functionName(arg1, arg2) {
    return (`The value for the arg1 is ${arg1}\n\
and the value for the arg2 is ${arg2}`);
}

console.log(functionName("Hello", "World"));

// arrow function, this is the way to write a shorter function
//
let myFunction = (a, b) => a * b;
console.log(myFunction(5,2));

let output = text => console.log(text);
output("Hello");

let myName = () => "My name is Kevin";
console.log(myName());

let multiLine = (word1, word2) => {
    text = `These are the words: ${word1} ${word2}`;
    return text;
}

console.log(multiLine("Hello", "World"));