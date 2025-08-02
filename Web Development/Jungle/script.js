const ANIMALS=["🦊","🐇"]; 
const FOREST=document.querySelector(".forest");

//By default, the first animal is selected
let selectedAnimal=ANIMALS[0];


function addAnimal(){

}



function switchFox(){
    selectedAnimal=ANIMALS[0];
    console.log("Switched to Fox");
}


function switchRabbit(){
    selectedAnimal=ANIMALS[1];
    console.log("Switched to Rabbit");
}

function  addAnimal(event){
    const animal=selectedAnimal;

    //Creating an element for the animal to be placed in
    const sprite=document.createElement("div");
    sprite.className="animal";
    sprite.textContent=selectedAnimal;

    //Setting the position of the animal based on the mouse click
    sprite.style.left=event.clientX + "px";
    sprite.style.top=event.clientY + "px";
    //Adding the animal to the forest
    FOREST.appendChild(sprite);

    // const posX=event.clientX;
    // const posY=event.clientY;
    // console.log("Adding " + animal + " at position (" + posX + ", " + posY + ")");
    // Here you would add the animal to the game world
}






