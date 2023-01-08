// Syntax guide - Loops
//
// You can run the same code over and over again with a loop.
//

// for statement
//
for (let counter = 1; counter < 4; counter++) {
    console.log(`The counter is on: ${counter}`);
}

// for of statement, this statement return the object value
//
const names = ["Jhon", "Marcela", "Mike"];
for (let x of names) {
    console.log(`This name is on the list: ${x}`);
}

let car = "BMW";
for (let n of car) {
    console.log(n);
}

// for in statement, this another statement return the index of the value
//
let color = "green";
for (let l in color) {
    console.log(`The letter ${color[l]} has the index ${l}`);
}

const fruits = {
    fruit1:"Apple",
    fruit2:"Watermelon",
    fruit3:"Blueberry"
};
for (let h in fruits) {
    if (fruits[h] !== "Watermelon") {
        console.log(fruits[h]);
    }
}
