import { SUPABASE_URL, SUPABASE_ANON_KEY } from './supabase.js';

const supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

const authView = document.getElementById('auth-view');
const dashboard = document.getElementById('dashboard');
const welcome = document.getElementById('welcome');
const roomView = document.getElementById('room-view');
let activeRoomId = null;
let realtimeChannel = null;


// --- Auth actions ---
document.getElementById('signup').onclick = async () => {
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;

  const { data, error } = await supabase.auth.signInWithPassword({ email, password });

  if (error && error.message.includes('Invalid login credentials')) {
    const { data: signUpData, error: signupError } = await supabase.auth.signUp({ email, password });
    if (signupError) return alert(signupError.message);

    const user = signUpData.user;
    if (user) {
      await supabase.from('USERS').insert({
        user_id: user.id,
        user_name: email.split('@')[0]
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
  document.getElementById('room-list').innerHTML = '<li>No rooms to show</li>';
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

  const { data: memberships, error } = await supabase
    .from('MEMBERSHIP')
    .select('room_id')
    .eq('user_id', user.id);

  if (error) return console.error(error);

  if (!memberships || memberships.length === 0) {
    document.getElementById('room-list').innerHTML = '<li>No rooms yet</li>';
    return;
  }

  const roomIds = memberships.map(m => m.room_id);
  const { data: rooms } = await supabase
    .from('ROOMS')
    .select('*')
    .in('room_id', roomIds);

  const list = document.getElementById('room-list');
  list.innerHTML = rooms.map(r => `
    <li>
      <strong>Room ${r.room_id}</strong><br/>
      <a href="#" class="enter-room" data-room-id="${r.room_id}">Enter Room</a>
    </li>
  `).join('');
}

document.getElementById('create-room').onclick = async () => {
  const password = document.getElementById('room-password').value;
  const { data: { user } } = await supabase.auth.getUser();

  const { data: room, error } = await supabase
    .from('ROOMS')
    .insert({ password })
    .select()
    .single();

  if (error) return alert(error.message);

  const { error: membershipError } = await supabase
    .from('MEMBERSHIP')
    .insert({ user_id: user.id, room_id: room.room_id });

  if (membershipError) return alert('Membership failed: ' + membershipError.message);

  alert('Room created!');
  loadRooms();
};

document.getElementById('join-room').onclick = async () => {
  const roomId = document.getElementById('join-room-id').value;
  const password = document.getElementById('join-room-password').value;
  const { data: { user } } = await supabase.auth.getUser();

  const { data: room, error } = await supabase
    .from('ROOMS')
    .select('*')
    .eq('room_id', roomId)
    .eq('password', password)
    .single();

  if (error || !room) return alert('Invalid room or password');

  await supabase
    .from('MEMBERSHIP')
    .insert({ user_id: user.id, room_id: room.room_id });

  alert('Joined room!');
  loadRooms();
};

document.getElementById('room-list').addEventListener('click', (e) => {
  if (!e.target.classList.contains('enter-room')) return;
  e.preventDefault();
  enterRoom(e.target.dataset.roomId);
});

function enterRoom(roomId) {
  dashboard.style.display = 'none';
  activeRoomId = roomId;
  document.getElementById('room-view').style.display = 'block';
  loadRoomData();
  subscribeToRoom(roomId);
}

async function loadRoomData() {
  if (!activeRoomId) return console.error('No active room set');

  const { data: room, error } = await supabase
    .from('ROOMS')
    .select('*')
    .eq('room_id', activeRoomId)
    .single();

  if (error) return console.error('Failed to load room:', error);

  document.getElementById('room-title').textContent = `Room ${room.room_id}`;
  loadTasks();
  loadShoppingItems();
}

function subscribeToRoom(roomId) {
  if (realtimeChannel) {
    supabase.removeChannel(realtimeChannel);
  }

  realtimeChannel = supabase
    .channel(`room-${roomId}`)
    .on(
      'postgres_changes',
      { event: '*', schema: 'public', table: 'TASKS', filter: `room_id=eq.${roomId}` },
      () => loadTasks()
    )
    .on(
      'postgres_changes',
      { event: '*', schema: 'public', table: 'SHOPPING_ITEMS', filter: `room_id=eq.${roomId}` },
      () => loadShoppingItems()
    )
    .subscribe((status) => {
      console.log('Realtime status:', status);
    });
}

document.getElementById('exit-room').addEventListener('click', () => {
  if (realtimeChannel) {
    supabase.removeChannel(realtimeChannel);
    realtimeChannel = null;
  }
  document.getElementById('room-view').classList.add('hidden');
  dashboard.style.display = 'block';
  roomView.style.display = 'none';
  activeRoomId = null;
});


// --- Task functions ---
async function loadTasks() {
  const { data: tasks, error } = await supabase
    .from('TASKS')
    .select('*')
    .eq('room_id', activeRoomId)
    .order('created_at', { ascending: true });

  if (error) return console.error('Failed to load tasks:', error);

  const list = document.getElementById('task-list');

  if (!tasks || tasks.length === 0) {
    list.innerHTML = '<li class="text-gray-400">No tasks yet</li>';
    return;
  }

  // fetch usernames separately
  const userIds = [...new Set(tasks.map(t => t.user_id))];
  const { data: users } = await supabase
    .from('USERS')
    .select('user_id, user_name')
    .in('user_id', userIds);

  const userMap = {};
  (users || []).forEach(u => userMap[u.user_id] = u.user_name);

  list.innerHTML = tasks.map(t => `
    <li class="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-50">
      <input
        type="checkbox"
        class="task-checkbox w-4 h-4 accent-indigo-600"
        data-task-id="${t.task_id}"
      />
      <div class="flex-1">
        <span>${t.description}</span>
        <span class="text-xs text-gray-400 ml-2">by ${userMap[t.user_id] ?? 'unknown'}</span>
      </div>
    </li>
  `).join('');
}

document.getElementById('task-list').addEventListener('change', async (e) => {
  if (!e.target.classList.contains('task-checkbox')) return;

  const taskId = e.target.dataset.taskId;

  // remove from UI instantly
  e.target.closest('li').remove();
  const list = document.getElementById('task-list');
  if (list.children.length === 0) {
    list.innerHTML = '<li class="text-gray-400">No tasks yet</li>';
  }

  // delete from Supabase
  const { error } = await supabase
    .from('TASKS')
    .delete()
    .eq('task_id', taskId);

  if (error) console.error('Failed to delete task:', error);
});


// --- Shopping list functions ---
async function loadShoppingItems() {
  const { data: items, error } = await supabase
    .from('SHOPPING_ITEMS')
    .select('*')
    .eq('room_id', activeRoomId)
    .order('is_purchased', { ascending: true })  // unpurchased first
    .order('created_at', { ascending: true });

  if (error) return console.error('Failed to load items:', error);

  const list = document.getElementById('shopping-list');

  if (!items || items.length === 0) {
    list.innerHTML = '<li class="text-gray-400">No items yet</li>';
    return;
  }

  // fetch usernames separately
  const userIds = [...new Set(items.map(i => i.added_by))];
  const { data: users } = await supabase
    .from('USERS')
    .select('user_id, user_name')
    .in('user_id', userIds);

  const userMap = {};
  (users || []).forEach(u => userMap[u.user_id] = u.user_name);

  list.innerHTML = items.map(i => `
    <li class="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-50">
      <input
        type="checkbox"
        class="item-checkbox w-4 h-4 accent-indigo-600"
        data-item-id="${i.item_id}"
        ${i.is_purchased ? 'checked' : ''}
      />
      <div class="flex-1">
        <span class="${i.is_purchased ? 'line-through text-gray-400' : ''}">${i.item}</span>
        <span class="text-xs text-gray-400 ml-2">by ${userMap[i.added_by] ?? 'unknown'}</span>
      </div>
      ${i.item_price > 0 ? `<span class="text-gray-500 text-xs">$${Number(i.item_price).toFixed(2)}</span>` : ''}
    </li>
  `).join('');
}

document.getElementById('shopping-list').addEventListener('change', async (e) => {
  if (!e.target.classList.contains('item-checkbox')) return;

  const itemId = e.target.dataset.itemId;
  const isPurchased = e.target.checked;

  const { error } = await supabase
    .from('SHOPPING_ITEMS')
    .update({ is_purchased: isPurchased })
    .eq('item_id', itemId);

  if (error) return console.error('Failed to update item:', error);

  loadShoppingItems(); // reload to re-sort
});


// --- Merged room-view click handler ---
document.getElementById('room-view').addEventListener('click', async (e) => {

  // Add task
  if (e.target.matches('#add-task')) {
    const input = document.getElementById('task-input');
    const description = input.value.trim();
    if (!description) return;

    // show instantly
    input.value = '';
    const list = document.getElementById('task-list');
    const tempId = 'temp-' + Date.now();
    const noTasks = list.querySelector('.text-gray-400');
    if (noTasks) list.innerHTML = '';
    list.insertAdjacentHTML('beforeend', `
      <li id="${tempId}" class="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-50">
        <input type="checkbox" class="task-checkbox w-4 h-4 accent-indigo-600" disabled />
        <div class="flex-1">
          <span class="text-gray-400">${description} (saving...)</span>
        </div>
      </li>
    `);

    // save to Supabase
    const { data: { user } } = await supabase.auth.getUser();
    const { error } = await supabase
      .from('TASKS')
      .insert({ room_id: activeRoomId, user_id: user.id, description });

    if (error) {
      document.getElementById(tempId)?.remove();
      return alert('Failed to add task: ' + error.message);
    }

    loadTasks(); // replace temp with real data
  }

  // Add shopping item
  if (e.target.matches('#add-item')) {
    const itemInput = document.getElementById('item-input');
    const priceInput = document.getElementById('item-price');
    const item = itemInput.value.trim();
    if (!item) return;

    // show instantly
    const price = parseFloat(priceInput.value) || 0;
    itemInput.value = '';
    priceInput.value = '';
    const list = document.getElementById('shopping-list');
    const tempId = 'temp-' + Date.now();
    const noItems = list.querySelector('.text-gray-400');
    if (noItems) list.innerHTML = '';
    list.insertAdjacentHTML('beforeend', `
      <li id="${tempId}" class="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-50">
        <input type="checkbox" class="item-checkbox w-4 h-4 accent-indigo-600" disabled />
        <div class="flex-1">
          <span class="text-gray-400">${item} (saving...)</span>
        </div>
        ${price > 0 ? `<span class="text-gray-500 text-xs">$${price.toFixed(2)}</span>` : ''}
      </li>
    `);

    // save to Supabase
    const { data: { user } } = await supabase.auth.getUser();
    const { error } = await supabase
      .from('SHOPPING_ITEMS')
      .insert({ room_id: activeRoomId, added_by: user.id, item, item_price: price });

    if (error) {
      document.getElementById(tempId)?.remove();
      return alert('Failed to add item: ' + error.message);
    }

    loadShoppingItems(); // replace temp with real data
  }
});


// --- Load initial state ---
supabase.auth.getSession().then(({ data: { session } }) => {
  session ? showDashboard() : showAuth();
});