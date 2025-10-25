// import { createClient } from "@supabase/supabase-js";
import { supabase } from "/supabase.js";

const emailInput = document.getElementById("email");
const roomInput = document.getElementById("roomCode");
const loginBtn = document.getElementById("loginBtn");

loginBtn.addEventListener("click", async () => {
  const email = emailInput.value.trim();
  const room = roomInput.value.trim().toUpperCase();
  if (!email || !room) return alert("Please fill both fields!");

  const { data: profile, error } = await supabase
    .from("profiles")
    .upsert({ email, room_code: room })
    .select()
    .single();

  if (error) {
    alert("Login failed: " + error.message);
    return;
  }

  // Save user data locally
  localStorage.setItem("email", email);
  localStorage.setItem("roomCode", room);
  localStorage.setItem("profileId", profile.id);

  // Redirect to main app
  window.location.href = "index.html";
});
