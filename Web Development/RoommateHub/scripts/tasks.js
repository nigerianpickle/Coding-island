import { supabase } from "./supabase.js";
import { addItem } from "./shopping.js";

const taskList = document.getElementById("taskList");

export async function loadTasks() {
  const { data: tasks } = await supabase.from("tasks").select("*").eq("completed", false);
  renderTasks(tasks);
}

function renderTasks(tasks) {
  taskList.innerHTML = "";
  tasks?.forEach(t => {
    const li = document.createElement("li");
    li.innerHTML = `
      <span>${t.title}</span>
      <button class="complete-btn" data-id="${t.id}">✅</button>
    `;
    li.querySelector(".complete-btn").onclick = () => completeTask(t.id, t.shopping_item_id);
    taskList.appendChild(li);
  });
}

export async function addTask(title, linkToShopping) {
  let shoppingId = null;
  if (linkToShopping) {
    const { data: item } = await supabase.from("shopping_items")
      .insert({ name: title, purchased: false })
      .select()
      .single();
    shoppingId = item?.id;
  }

  await supabase.from("tasks").insert({
    title,
    completed: false,
    points: 10,
    shopping_item_id: shoppingId
  });

  loadTasks();
}

export async function completeTask(id, shoppingItemId) {
  await supabase.from("tasks").update({ completed: true }).eq("id", id);
  if (shoppingItemId) {
    await supabase.from("shopping_items").update({ purchased: true }).eq("id", shoppingItemId);
  }
  loadTasks();
}
