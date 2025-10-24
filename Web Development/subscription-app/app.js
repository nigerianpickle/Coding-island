import { supabase } from "./supabase.js";

const authDiv = document.getElementById("auth");
const notesDiv = document.getElementById("notes");
const notesList = document.getElementById("notesList");
const addNoteBtn = document.getElementById("addNote");
const newNote = document.getElementById("newNote");

const signupBtn = document.getElementById("signupBtn");
const loginBtn = document.getElementById("loginBtn");
const logoutBtn = document.getElementById("logoutBtn");

let user = null;

// AUTH ---
signupBtn.addEventListener("click", async () => {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const { data, error } = await supabase.auth.signUp({ email, password });
  if (error) alert(error.message);
  else alert("Check your email to confirm sign up!");
});

loginBtn.addEventListener("click", async () => {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const { data, error } = await supabase.auth.signInWithPassword({ email, password });
  if (error) alert(error.message);
  else user = data.user;
  updateUI();
});

logoutBtn.addEventListener("click", async () => {
  await supabase.auth.signOut();
  user = null;
  updateUI();
});

// UI ---
function updateUI() {
  if (user) {
    authDiv.classList.add("hidden");
    notesDiv.classList.remove("hidden");
    loadNotes();
  } else {
    authDiv.classList.remove("hidden");
    notesDiv.classList.add("hidden");
  }
}

// NOTES ---
async function loadNotes() {
  const { data, error } = await supabase
    .from("notes")
    .select("*")
    .eq("user_id", user.id)
    .order("created_at", { ascending: false });

  if (error) console.error(error);
  renderNotes(data || []);
}

function renderNotes(notes) {
  notesList.innerHTML = "";
  notes.forEach((n) => {
    const div = document.createElement("div");
    div.className = "note";
    div.textContent = n.content;
    div.onclick = async () => {
      if (confirm("Delete this note?")) {
        await supabase.from("notes").delete().eq("id", n.id);
        loadNotes();
      }
    };
    notesList.appendChild(div);
  });
}

addNoteBtn.addEventListener("click", async () => {
  if (!newNote.value.trim()) return;
  await supabase.from("notes").insert({ user_id: user.id, content: newNote.value });
  newNote.value = "";
  loadNotes();
});

// Check session on page load
supabase.auth.getSession().then(({ data }) => {
  user = data.session?.user || null;
  updateUI();
});
