const HEIGHT=500;
const WIDTH=500;
let GRID_SIZE=16;
const container = document.querySelector('#container');
container.style.height = HEIGHT+'px';
container.style.width = WIDTH+'px';


function getRandomRgbColor() {
  const r = Math.floor(Math.random() * 256); // Random number between 0 and 255 for Red
  const g = Math.floor(Math.random() * 256); // Random number between 0 and 255 for Green
  const b = Math.floor(Math.random() * 256); // Random number between 0 and 255 for Blue
  return `rgb(${r}, ${g}, ${b})`;

}


function createGrid(){
  console.log(`Creating grid with size ${GRID_SIZE}x${GRID_SIZE}`);
  for (let i = 0; i < GRID_SIZE*GRID_SIZE; i++) {

          const square = document.createElement('div');
          square.classList.add('square');
          square.style.height = (HEIGHT/GRID_SIZE)+'px';
          square.style.width = (WIDTH/GRID_SIZE)+'px';
          // square.style.backgroundColor = getRandomRgbColor();
    
          container.appendChild(square);

  }

  const squares = document.querySelectorAll('.square');
  squares.forEach(square => {
      square.addEventListener('mouseover', () => {
          square.style.backgroundColor = 'black';
      });
  });
}





function resizeGrid() {
    GRID_SIZE = parseInt(prompt("Enter new grid size (e.g., 16 for 16x16):"));
    if (isNaN(GRID_SIZE) || GRID_SIZE <= 0) {
        alert("Invalid grid size. Please enter a positive number.");
        return;
    }else if (GRID_SIZE > 100) {
        alert("Grid size too large. Please enter a number less than or equal to 100.");
        return;
    }
    console.log(`Resizing grid to ${GRID_SIZE}x${GRID_SIZE}`);
}




createGrid();





const resetButton = document.querySelector('#clear');
resetButton.addEventListener('click', () => {
    resizeGrid();
    container.innerHTML = ''; // Clear the existing grid
    createGrid();
    squares.forEach(square => {
        square.style.backgroundColor = 'white';
    });
});



const resizeGridButton = document.querySelector('#resize');
resizeGridButton.addEventListener('click', () => {
    resizeGrid();
    container.innerHTML = ''; // Clear the existing grid
    createGrid();
});