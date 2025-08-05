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

let firstNumber = DEFAULT
let secondNumber = DEFAULT;
let currentNumber = 0;
let operator = DEFAULT;
let total=0;


let operatorPressed = false;
let firstValSet=false;
let secondValSet=false;



DISPLAY = document.querySelector('.calculator-display');
DISPLAY.textContent = DEFAULT;

function multiply(firstNumber, secondNumber) {
    return firstNumber * secondNumber;
}

function updateDisplay(button){
    if(firstValSet && operatorPressed== false) {
        //reset the display if an operator was pressed
        DISPLAY.textContent = DEFAULT;
        operatorPressed = true;
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
    DISPLAY.textContent = '';
}

function getValue(button){
    return parseInt(button.textContent);
    
}

function setOperator(button) {
    if (operatorPressed) {
        // If an operator was already pressed, we can just update the operator

        return;
    }
    // If no operator was pressed yet, we set the first number and the operator
    if (firstNumber === DEFAULT) {}
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
    
    if(!firstValSet){
        firstNumber = currentNumber;
        firstValSet = true;
        operator = button.textContent;

        return;
    }
    else if(!secondValSet){
        secondNumber= currentNumber;
        secondValSet = true;
        total = operate(firstNumber, secondNumber, operator);
        display(total);
    }
    else if(firstValSet && secondValSet) {
        // If both first and second values are set, we can perform the operation
        firstNumber = total; // Update firstNumber with the result of the last operation
        operator = button.textContent; // Set new operator
        secondValSet = false; // Reset secondValSet for the next operation
        display(total);
    }

    // if(!secondValSet && operator!== DEFAULT) {
    //     secondNumber = parseFloat(DISPLAY.textContent);
    //     secondValSet = true;
    //     total = operate(firstNumber, secondNumber, operator);
    //     display(total);
    //     firstNumber = total; // Update firstNumber for the next operation
    //     operator = button.textContent; // Set new operator
    //     secondValSet = false; // Reset secondValSet for the next operation
    // }


}


// Add event listeners to number buttons
numbers.forEach(number => {
    number.addEventListener("click", () => {
        currentNumber = updateDisplay(number); // single call only
    });
});


operators.forEach(operator=>
        {operator.addEventListener("click",()=>{handleOperator(operator);})
    })
    




// while (true) {
//     firstNumber = parseFloat(DISPLAY.textContent);
//     console.log(firstNumber);
// }

