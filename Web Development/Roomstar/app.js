import { supabase } from "./supabase.js";

// --- SESSION ---
const email = localStorage.getItem("email");
const roomCode = localStorage.getItem("roomCode");
const profileId = localStorage.getItem("profileId");
if (!email || !roomCode || !profileId) window.location.href = "login.html";

// --- DOM ---
const tasksTab = document.getElementById("tasksTab");
const shopTab  = document.getElementById("shopTab");
const taskList = document.getElementById("taskList");
const shopList = document.getElementById("shopList");
const coinsDisplay = document.getElementById("coins");
const addBtn = document.querySelector(".add-btn");

// --- STATE ---
let coins = 0;
let tasks = [];
let shopping = [];

// --- BOOT ---
await loadProfile();
await loadTasks();
await loadShopping();
setupRealtime();

// --- LOADERS ---
async function loadProfile() {
  const { data, error } = await supabase
    .from("profiles")
    .select("*")
    .eq("id", profileId)
    .single();
  if (error) { console.error("Profile load error:", error); return; }
  coins = data?.coins ?? 100;
  coinsDisplay.textContent = coins;
}

async function loadTasks() {
  const { data: profiles, error: pErr } = await supabase
    .from("profiles")
    .select("id")
    .eq("room_code", roomCode);
  if (pErr) { console.error("Profiles fetch for tasks error:", pErr); return; }

  const ids = (profiles ?? []).map(p => p.id);
  if (ids.length === 0) { tasks = []; renderTasks(); return; }

  const { data, error } = await supabase
    .from("tasks")
    .select("*")
    .in("profile_id", ids)
    .order("id", { ascending: true });
  if (error) { console.error("Tasks load error:", error); return; }

  tasks = data ?? [];
  renderTasks();
}

async function loadShopping() {
  const { data: profiles, error: pErr } = await supabase
    .from("profiles")
    .select("id")
    .eq("room_code", roomCode);
  if (pErr) { console.error("Profiles fetch for shopping error:", pErr); return; }

  const ids = (profiles ?? []).map(p => p.id);
  if (ids.length === 0) { shopping = []; renderShop(); return; }

  const { data, error } = await supabase
    .from("shopping")
    .select("*")
    .in("profile_id", ids)
    .order("id", { ascending: true });
  if (error) { console.error("Shopping load error:", error); return; }

  shopping = data ?? [];
  renderShop();
}

// --- RENDER ---
function renderTasks() {
  taskList.innerHTML = tasks.length ? "" : "<p class='empty'>No tasks yet — add one!</p>";
  for (const t of tasks) {
    const row = document.createElement("div");
    row.className = "card";
    row.innerHTML = `
      <p style="${t.completed ? 'text-decoration: line-through; opacity:.6;' : ''}">${t.title}</p>
      <button class="btn complete-btn" ${t.completed ? "disabled" : ""}>
        ${t.completed ? "✅ Done" : "Complete"}
      </button>
    `;
    row.querySelector(".complete-btn").addEventListener("click", () => completeTask(t.id, t.completed));
    taskList.appendChild(row);
  }
}

function renderShop() {
  shopList.innerHTML = shopping.length ? "" : "<p class='empty'>No shopping items yet — add one!</p>";
  for (const s of shopping) {
    const row = document.createElement("div");
    row.className = "card";
    row.innerHTML = `
      <p style="${s.done ? 'text-decoration: line-through; opacity:.6;' : ''}">${s.title}</p>
      <button class="btn buy-btn" ${s.done ? "disabled" : ""}>
        ${s.done ? "🛍️ Bought" : "Claim"}
      </button>
    `;
    row.querySelector(".buy-btn").addEventListener("click", () => completeShop(s.id, s.done));
    shopList.appendChild(row);
  }
}

// --- ACTIONS ---
async function completeTask(id, completed) {
  if (completed) return;
  const { error } = await supabase.from("tasks").update({ completed: true }).eq("id", id);
  if (error) { console.error("Task update error (RLS?)", error); return; }
  await updateCoins(10);
  await loadTasks(); // immediate refresh
}

async function completeShop(id, done) {
  if (done) return;
  const { error } = await supabase.from("shopping").update({ done: true }).eq("id", id);
  if (error) { console.error("Shopping update error (RLS?)", error); return; }
  await updateCoins(5);
  await loadShopping(); // immediate refresh
}

async function updateCoins(amount) {
  coins += amount;
  coinsDisplay.textContent = coins;
  const { error } = await supabase.from("profiles").update({ coins }).eq("id", profileId);
  if (error) console.error("Coin update error (RLS?)", error);
}

// --- ADD ---
addBtn.addEventListener("click", async () => {
  const isTaskTab = tasksTab.classList.contains("active");
  const input = prompt(isTaskTab ? "Enter new task:" : "Enter new shopping item:");
  if (!input) return;

  if (isTaskTab) {
    const { error } = await supabase.from("tasks").insert({ title: input, profile_id: profileId });
    if (error) { console.error("Task insert error (RLS?)", error); return; }
    await loadTasks();
  } else {
    const { error } = await supabase.from("shopping").insert({ title: input, profile_id: profileId });
    if (error) { console.error("Shopping insert error (RLS?)", error); return; }
    await loadShopping();
  }
});

// --- TABS ---
tasksTab.addEventListener("click", () => {
  tasksTab.classList.add("active");
  shopTab.classList.remove("active");
  taskList.classList.remove("hidden");
  shopList.classList.add("hidden");
  addBtn.textContent = "➕ Add Task";
});
shopTab.addEventListener("click", () => {
  shopTab.classList.add("active");
  tasksTab.classList.remove("active");
  shopList.classList.remove("hidden");
  taskList.classList.add("hidden");
  addBtn.textContent = "🛒 Add Item";
});

// --- REALTIME ---
function setupRealtime() {
  supabase
    .channel("room_updates")
    .on("postgres_changes", { event: "*", schema: "public", table: "tasks" }, (payload) => {
      console.log("Realtime (tasks):", payload);
      loadTasks();
    })
    .on("postgres_changes", { event: "*", schema: "public", table: "shopping" }, (payload) => {
      console.log("Realtime (shopping):", payload);
      loadShopping();
    })
    .subscribe();
}
