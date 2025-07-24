function playRound(){

}


function

const humanChoice=getHumanChoice();
const computerChoice=getComputerChoice();



console.log("Hello world");
    computerchoice="";
done=false;
while (!done){

    
    userchoice=prompt("Enter your choice (rock, paper, scissors): (Enter 'exit' to quit)");

    if (userchoice=="exit"){
        console.log("Exiting the game. Goodbye!");
        done=true;
        break;
    }



    // Determine computer's choice based on random number
    number=Math.random();
    if (number>0.66){
        computerchoice="rock";
    }
    else if (number>0.33){
        computerchoice="paper";
    }
    else{
        computerchoice="scissors";
    }


    if (userchoice==computerchoice){
        console.log("It's a tie! You both chose " + userchoice + ".");
    }
    else if(userchoice=="rock" && computerchoice=="scissors"){
        console.log("You win! Rock beats Scissors.");
    }
    else if(userchoice=="paper" && computerchoice=="rock"){
        console.log("You win! Paper beats Rock.");
    }
    else if(userchoice=="scissors" && computerchoice=="paper"){
        console.log("You win! Scissors beats Paper.");
    }
    else{
        console.log("You lose! " + computerchoice + " beats " + userchoice + ".");
    }
}