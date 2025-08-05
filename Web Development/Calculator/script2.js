const MULTIPLY = '*';
const DIVIDE = '/';
const ADD = '+';
const SUBTRACT = '-';
const DEFAULT = 0;

const DISPLAY = document.querySelector('.calculator-display');
const calculatorButtons = document.querySelector('.calculator-buttons');
const numberButtons = calculatorButtons.querySelectorAll('.numbers button');
const operatorButtons = calculatorButtons.querySelectorAll('.operators button');

let currentNumber = '';
let firstNumber = null;
let secondNumber = null;
let operator = null;
let resultShown = false;

// Basic operations
const operations = {
    [ADD]: (a, b) => a + b,
    [SUBTRACT]: (a, b) => a - b,
    [MULTIPLY]: (a, b) => a * b,
    [DIVIDE]: (a, b) => b !== 0 ? a / b : 'Error',
};

function updateDisplay(value) {
    DISPLAY.textContent = value;
}

function clear() {
    currentNumber = '';
    firstNumber = null;
    secondNumber = null;
    operator = null;
    resultShown = false;
    updateDisplay(DEFAULT);
}

function handleNumberClick(num) {
    if (resultShown) {
        currentNumber = '';
        resultShown = false;
    }
    currentNumber += num;
    updateDisplay(currentNumber);
}

function handleOperatorClick(op) {
    if (op === 'clear') {
        clear();
        return;
    }

    if (!firstNumber && currentNumber !== '') {
        firstNumber = parseFloat(currentNumber);
        operator = op;
        currentNumber = '';
    } else if (firstNumber !== null && currentNumber !== '') {
        secondNumber = parseFloat(currentNumber);
        if (operator && operations[operator]) {
            const result = operations[operator](firstNumber, secondNumber);
            updateDisplay(result);
            firstNumber = result;
            secondNumber = null;
            operator = op;
            currentNumber = '';
            resultShown = true;
        }
    } else {
        operator = op; // allow changing the operator
    }
}

// Event listeners
numberButtons.forEach(button => {
    button.addEventListener('click', () => handleNumberClick(button.textContent));
});

operatorButtons.forEach(button => {
    button.addEventListener('click', () => 
    
        handleOperatorClick(button.textContent));
});

// Initialize
clear();
