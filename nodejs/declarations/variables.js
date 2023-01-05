// Syntax guide - Variables
//
// The let keyword was added in ES6. Let variables can not 
// be used without first declaring
//

let name = "Kevin"; // This variable can not be redeclared but its value can change
let number;
console.log(name)

number = 10;
name = "Luis";

console.log(name, number)

// The const keyword was also added in ES6. The difference with let variables
// is that they can not change their value.
//

const PI = 3.14;
console.log(`The PI value is: ${PI}`)

//PI = 3.141; it will be error
//