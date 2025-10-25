import { supabase } from "./supabase.js";
import { loadTasks, addTask, completeTask } from "./tasks.js";
import { loadItems, addItem, markBought } from "./shopping.js";

// Tabs
const tabTasks = document.getElementById("tabTasks");
const tabShopping = document.getElementById("tabShopping");
const tasksSection = document.getElementById("tasksSection");
const shoppingSection = document.getElementById("shoppingSection");

// Tab switching
tabTasks.onclick = () => {
  tabTasks.classList.add("active");
  tabShopping.classList.remove("active");
  tasksSection.classList.add("active");
  shoppingSection.classList.remove("active");
};

tabShopping.onclick = () => {
  tabShopping.classList.add("active");
  tabTasks.classList.remove("active");
  shoppingSection.classList.add("active");
  tasksSection.classList.remove("active");
};

// Load initial data
loadTasks();
loadItems();

// Add task
document.getElementById("addTaskBtn").onclick = async () => {
  const name = document.getElementById("taskInput").value.trim();
  const isShoppingLink = document.getElementById("isShoppingLink").checked;
  if (name) await addTask(name, isShoppingLink);
  document.getElementById("taskInput").value = "";
  document.getElementById("isShoppingLink").checked = false;
};

// Add shopping item
document.getElementById("addItemBtn").onclick = async () => {
  const name = document.getElementById("itemInput").value.trim();
  if (name) await addItem(name);
  document.getElementById("itemInput").value = "";
};
