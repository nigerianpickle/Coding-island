const choices=["rock","paper","scissors"];
const rounds=5;
playerScore=0;
computerScore=0;

function playRound(userChoice, computerChoice) {
    if (userChoice==computerChoice){
        return "It's a tie! You both chose " + userChoice + ".";
    }
    else if(userChoice=="rock"&&computerChoice=="scissors"){
        playerScore++;
        return "you win! Rock beats scissors";
    }
    else if(userChoice=="paper"&&computerChoice=="rock"){
        playerScore++;
        return "you win! Rock beats scissors";
    }
    else if(userChoice=="scissors"&&computerChoice=="paper"){
        playerScore++;
        return "you win! scissors beats paper";
    }
    else{
        computerScore++;
        return "you lose! " + computerChoice + " beats " + userChoice + ".";
    }
}

function getHumanChoice(){
    return prompt("Enter your choice (rock, paper, scissors): (Enter 'exit' to quit)");
}

function getComputerChoice(){
    choice=Math.random()*3;
    return choices[Math.floor(choice)];
}

function goodByeText(){
    console.log("Exiting the game!");
    console.log("Your Score:"+playerScore + " Computer Score:" + computerScore);
}


function playGame(rounds){
        i=rounds;
        while(i>0){
            const humanChoice=getHumanChoice();
            if(humanChoice=="exit"){
                goodByeText();
                return;
            }
            const computerChoice=getComputerChoice();

            console.log(playRound(humanChoice, computerChoice));
            i--;
        }
        goodByeText();
}


function sumOfTripledEvens(){
    
}



playGame(rounds);
// console.log("Game over! Thanks for playing.");
