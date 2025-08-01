const container=document.querySelector("#container");

const content = document.createElement("div");


content.classList.add("content");

content.textContent = "This is the content";
 
container.appendChild(content);
const paragraph=document.createElement("p");
paragraph.textContent="Hey i'm red";
paragraph.style.color="red";

container.appendChild(paragraph);



// Events
const button=document.querySelector("#bttn");
button.onclick=()=>alert("Hello World");

document.addEventListener("click", function (e) {
  e.target.style.background = "blue";
})