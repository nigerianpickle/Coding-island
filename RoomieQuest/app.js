import { SUPABASE_URL, SUPABASE_ANON_KEY } from './supabase.js';

// create Supabase client using CDN global
const supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

const authView = document.getElementById('auth-view');
const dashboard = document.getElementById('dashboard');
const welcome = document.getElementById('welcome');

// --- Auth actions ---
document.getElementById('signup').onclick = async () => {
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  const { data, error } = await supabase.auth.signUp({ email, password });
  if (error) alert(error.message);
  else alert('Check your email to confirm signup!');
};

document.getElementById('login').onclick = async () => {
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  const { data, error } = await supabase.auth.signInWithPassword({ email, password });
  
  if (error) alert(error.message);
  else showDashboard();
};

document.getElementById('logout').onclick = async () => {
  await supabase.auth.signOut();
  showAuth();
};

// --- UI helpers ---
async function showDashboard() {
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) return showAuth();
  authView.style.display = 'none';
  dashboard.style.display = 'block';
  welcome.textContent = `Welcome, ${user.email}!`;
}

function showAuth() {
  dashboard.style.display = 'none';
  authView.style.display = 'block';
}

// --- Load initial state ---
supabase.auth.getSession().then(({ data: { session } }) => {
  session ? showDashboard() : showAuth();
});
