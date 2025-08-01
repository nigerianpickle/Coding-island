const container = document.querySelector('#container');
const HEIGHT=container.style.height = '500px';
const WIDTH=container.style.width = '500px';


function getRandomRgbColor() {
  const r = Math.floor(Math.random() * 256); // Random number between 0 and 255 for Red
  const g = Math.floor(Math.random() * 256); // Random number between 0 and 255 for Green
  const b = Math.floor(Math.random() * 256); // Random number between 0 and 255 for Blue
  return `rgb(${r}, ${g}, ${b})`;

}



for (let i = 0; i < 16*16; i++) {
        const square = document.createElement('div');
        square.classList.add('square');

        square.style.backgroundColor = getRandomRgbColor();
        // square.style.border = '1px solid black';
        container.appendChild(square);


}