//fucntions: add, subtractor,multiply,divide,equal, clear button
//displayNum()- to show numbers
//Objects: Number, Operator,Opeartion?
const MULTIPLY= '*';
const DIVIDE= '/';
const ADD= '+';
const SUBTRACT= '-';
const EVALUATE= '=';
const DEFAULT= 0;
const DISPLAY = document.querySelector('.calculator-display');

function multiply(firstNumber, secondNumber) {
    return firstNumber * secondNumber;
}

function updateDisplay(value){

}


function add(firstNumber, secondNumber) {
    return firstNumber + secondNumber;
}

function divide(firstNumber, secondNumber) {
    return firstNumber / secondNumber;
}

function subtract(firstNumber, secondNumber) {
    return firstNumber - secondNumber;
}

function  updateDisplayValue(currentValue,Number){
    if (currentValue === DEFAULT) {
        return Number;
    } else {
        return currentValue + Number*10;
    }



}

function operate(firstNumber, secondNumber, operator) {
    switch(operator){
        case MULTIPLY:
            return multiply(firstNumber, secondNumber);
        case ADD:
            return add(firstNumber, secondNumber);
        case DIVIDE:
            return divide(firstNumber, secondNumber);
        case SUBTRACT:
            return subtract(firstNumber, secondNumber);
        default:
            return 'Invalid operator';
    }
}



function display(value){
    DISPLAY.textContent = value;
}


function clearDisplay() {
    DISPLAY.textContent = '';
}

const calculatorButtons=document.querySelector('.calculator-buttons');
const numberButtons = calculatorButtons.querySelector('.numbers');

const numbers = numberButtons.querySelectorAll('button');


firstNumber = 0
secondNumber = '';
operator = '';



// Add event listeners to number buttons
numbers.forEach(number=>
    {number.addEventListener("click",()=>{console.log(number.textContent);})
    })

    


display("Im the goat");