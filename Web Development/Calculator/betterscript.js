//fucntions: add, subtractor,multiply,divide,equal, clear button
//displayNum()- to show numbers
//Objects: Number, Operator,Opeartion?
const MULTIPLY= '*';
const DIVIDE= '/';
const ADD= '+';
const SUBTRACT= '-';
const EVALUATE= '=';
const DEFAULT= 0;
const calculatorButtons=document.querySelector('.calculator-buttons');
const numberButtons = calculatorButtons.querySelector('.numbers');
const operatorButtons = calculatorButtons.querySelector('.operators');


const numbers = numberButtons.querySelectorAll('button');
const operators = operatorButtons.querySelectorAll('button');

let firstNumber = null
let secondNumber = null;
let total=null;
let currentNumber = 0;
let operator = DEFAULT;
let clearScreen=false;






DISPLAY = document.querySelector('.calculator-display');
DISPLAY.textContent = DEFAULT;

function multiply(firstNumber, secondNumber) {
    return firstNumber * secondNumber;
}

function updateDisplay(button){
    if(clearScreen) {
        //reset the display if an operator was pressed
        DISPLAY.textContent = DEFAULT;
        clearScreen = false;
    }

    currentValue = DISPLAY.textContent;
    number = parseFloat(button.textContent);
                newValue = parseFloat(currentValue)*10 + number;
                DISPLAY.textContent = newValue;
                return newValue;
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



function operate(firstNumber, secondNumber, operator) {

    switch(operator){
        case MULTIPLY:
            DISPLAY.textContent = multiply(firstNumber, secondNumber);
            return multiply(firstNumber, secondNumber);
        case ADD:
            DISPLAY.textContent = add(firstNumber, secondNumber);
            return add(firstNumber, secondNumber);
        case DIVIDE:
            DISPLAY.textContent = divide(firstNumber, secondNumber);
            return divide(firstNumber, secondNumber);
        case SUBTRACT:
            DISPLAY.textContent = subtract(firstNumber, secondNumber);
            return subtract(firstNumber, secondNumber);
        default:
            return 'Invalid operator';
    }
}





function display(value){
    DISPLAY.textContent = value;
}


function clearDisplay() {
    DISPLAY.textContent = DEFAULT;
}

function getValue(button){
    return parseInt(button.textContent);
    
}



function showNumber(button) {
    //Making sure the first number is set
    if(firstNumber==DEFAULT) {
        firstNumber= getValue(button);
        display(firstNumber);
        return;
    }
    else{
        updateDisplayValue(firstNumber, getValue(button)); 
    }
}


function handleOperator(button) {
    
    if(!firstNumber){
        firstNumber=parseFloat(DISPLAY.textContent);
        operator = button.textContent;
        clearScreen = true; // Set flag to clear display on next number input
        console.log(`First number set to: ${firstNumber}, Operator: ${operator}`);
        return;
    }
    else if(firstNumber && !secondNumber) {
        secondNumber = parseFloat(DISPLAY.textContent);
        total = operate(firstNumber, secondNumber, operator);
        console.log(`Second number set to: ${secondNumber}, Total: ${total}`);
        display(total);
        firstNumber = total; // Update firstNumber for the next operation
        clearScreen = true; // Set flag to clear display on next number input
        return
    }
    else{
        // If an operator was already pressed, we can just update the operator
        operator = button.textContent;
        total = operate(firstNumber, secondNumber, operator);
        console.log(`Total now: ${total}`);
        display(total);
        firstNumber = total; // Update firstNumber for the next operation
        clearScreen = true; // Set flag to clear display on next number input
        return;
    }
    


}


// Add event listeners to number buttons
numbers.forEach(number => {
    number.addEventListener("click", () => {
        currentNumber = updateDisplay(number); // single call only
    });
});


operators.forEach(operator=>
        {operator.addEventListener("click",()=>{
        if(operator.textContent === 'clear') {
            clearDisplay();
            return;
        }
            handleOperator(operator);})
    })
    


