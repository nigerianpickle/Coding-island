import { supabase } from "./supabase.js";

const shoppingList = document.getElementById("shoppingList");

export async function loadItems() {
  const { data: items } = await supabase.from("shopping_items").select("*").eq("purchased", false);
  renderItems(items);
}

function renderItems(items) {
  shoppingList.innerHTML = "";
  items?.forEach(i => {
    const li = document.createElement("li");
    li.innerHTML = `
      <span>${i.name}</span>
      <button class="buy-btn" data-id="${i.id}">🛍️</button>
    `;
    li.querySelector(".buy-btn").onclick = () => markBought(i.id);
    shoppingList.appendChild(li);
  });
}

export async function addItem(name) {
  await supabase.from("shopping_items").insert({ name, purchased: false });
  loadItems();
}

export async function markBought(id) {
  await supabase.from("shopping_items").update({ purchased: true }).eq("id", id);
  loadItems();
}
