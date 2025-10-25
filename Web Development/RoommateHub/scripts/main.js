let roommates = JSON.parse(localStorage.getItem("roommates")) || [
  { name: "Daniel", points: 0 },
  { name: "Alex", points: 0 },
  { name: "Chris", points: 0 }
];

function updateLeaderboard() {
  const list = document.getElementById("leaderboardList");
  list.innerHTML = "";
  roommates
    .sort((a, b) => b.points - a.points)
    .forEach(r => {
      const li = document.createElement("li");
      li.textContent = `${r.name} - ${r.points} pts`;
      list.appendChild(li);
    });
  localStorage.setItem("roommates", JSON.stringify(roommates));
}

updateLeaderboard();
