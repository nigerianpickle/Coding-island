const ANIMALS=["Fox","Rabbit"]; 
const FOREST=document.querySelector(".forest");

//By default, the first animal is selected
let selectedAnimal=ANIMALS[0];


class Forest{
    constructor(){
        this.animals=[];
    }

    addAnimal(type,x,y){
        let animal;
        //Fox

            if (selectedAnimal=="Fox"){
                animal=new Fox();
            } else if (selectedAnimal=="Rabbit"){
                animal=new Rabbit();
            }else{
                console.error("Unknown animal type: " + selectedAnimal);
                return null;
            }

             this.animals.push(animal);
             animal.setPosition(x,y);
             return animal;
    }


    
}


class Animal{
    constructor(name){
        this.name=name;
        this.sprite=null; //This will hold the HTML element representing the animal
        this.x=0;
        this.y=0;
    }
    
    get name(){
        return this.name;
    }
    

    //Sets the position of the animal in the forest
     setPosition(x,y){
        this.x=x;
        this.y=y;
    }

    setX(x){
        this.x=x;
    }
    
    setY(y){
        this.y=y;
    }

    
}

class Fox extends Animal{
    constructor(){
        super("Fox");
    }

    get type(){
        return this.name;
    }
}

class Rabbit extends Animal{
    constructor(){
        super("Rabbit");
    }

    get type(){
        return this.name;
    }
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





//Testing the classes
const fox=new Fox();
const rabbit=new Rabbit();
console.log(fox.type); // "Fox"
console.log(rabbit.type); // "Rabbit"