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

// Try logging in
const { data, error } = await supabase.auth.signInWithPassword({ email, password });

  if (error && error.message.includes('Invalid login credentials')) {
    // Email not registered yet → sign them up
    const { data: signUpData, error: signupError } = await supabase.auth.signUp({ email, password });
    if (signupError) return alert(signupError.message);

    // After successful signup, insert user into USERS table
    const user = signUpData.user;
    if (user) {
      await supabase.from('USERS').insert({
        user_id: user.id,
        user_name: email.split('@')[0] // basic username
      });
    }

    alert('Check your email to confirm signup!');
  } else {
    alert('Account already exists!');
  }
};
  


document.getElementById('login').onclick = async () => {
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;

  const { data, error } = await supabase.auth.signInWithPassword({ email, password });
  if (error) return alert(error.message);

  // ensure USERS row exists
  const { data: { user } } = await supabase.auth.getUser();
  const { data: existing } = await supabase
    .from('USERS')
    .select('user_id')
    .eq('user_id', user.id)
    .maybeSingle();

  if (!existing) {
    await supabase.from('USERS').insert({
      user_id: user.id,
      user_name: email.split('@')[0]
    });
  }

  showDashboard();
};


document.getElementById('logout').onclick = async () => {
  await supabase.auth.signOut();
  document.getElementById('room-list').innerHTML = '<li>No rooms toshow </li>';
  showAuth();
};

// --- UI helpers ---
async function showDashboard() {
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) return showAuth();
  authView.style.display = 'none';
  dashboard.style.display = 'block';
  welcome.textContent = `Welcome, ${user.email}!`;
  loadRooms();
}

function showAuth() {
  dashboard.style.display = 'none';
  authView.style.display = 'block';
}

// --- Room functions ---
async function loadRooms() {
  const { data: { user } } = await supabase.auth.getUser();

  // get all memberships for the current user
  
  const { data: memberships, error } = await supabase
    .from('MEMBERSHIP')
    .select('room_id')
    .eq('user_id', user.id);

  if (error) return console.error(error);

  // get actual room details
  if (!memberships || memberships.length === 0) {
    document.getElementById('room-list').innerHTML = '<li>No rooms yet</li>';
    return;
  }

  //Joining the rooms based on room id
  const roomIds = memberships.map(m => m.room_id);
  const { data: rooms } = await supabase
    .from('ROOMS')
    .select('*')
    .in('room_id', roomIds);

  const list = document.getElementById('room-list');
  list.innerHTML = rooms.map(r => `
    <li>
      Room ID: ${r.room_id}<br/>
      Password: ${r.password}
    </li>`).join('');
}

document.getElementById('create-room').onclick = async () => {
  const password = document.getElementById('room-password').value;
  const { data: { user } } = await supabase.auth.getUser();

  // create new room
  const { data: room, error } = await supabase
    .from('ROOMS')
    .insert({ password })
    .select()
    .single();

  if (error) return alert(error.message);

  // link the user to the room
    const { data: membership, error: membershipError } = await supabase
    .from('MEMBERSHIP')
    .insert({ user_id: user.id, room_id: room.room_id })
    .select()
    .single();

    if (membershipError) {
    console.error('Membership insert error:', membershipError);
    alert('Membership failed: ' + membershipError.message);
    return;
    }
  alert('Room created!');
  loadRooms();
};

document.getElementById('join-room').onclick = async () => {
  const roomId = document.getElementById('join-room-id').value;
  const password = document.getElementById('join-room-password').value;
  const { data: { user } } = await supabase.auth.getUser();

  // check if the room exists and password matches
  const { data: room, error } = await supabase
    .from('ROOMS')
    .select('*')
    .eq('room_id', roomId)
    .eq('password', password)
    .single();

  if (error || !room) return alert('Invalid room or password');

  // link the user
  await supabase
    .from('MEMBERSHIP')
    .insert({ user_id: user.id, room_id: room.room_id });

  alert('Joined room!');
  loadRooms();
};


// --- Load initial state ---
supabase.auth.getSession().then(({ data: { session } }) => {
  session ? showDashboard() : showAuth();
});
