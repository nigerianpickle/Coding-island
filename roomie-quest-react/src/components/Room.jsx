import { useState, useEffect, useCallback } from 'react';
import { supabase } from '../supabaseClient';

const MEMBER_COLORS = [
  '#10b981', '#6366f1', '#f59e0b', '#ef4444', '#8b5cf6',
];

function getInitials(name) {
  if (!name) return '?';
  return name.slice(0, 2).toUpperCase();
}

function getMemberColor(userId) {
  let hash = 0;
  for (let i = 0; i < userId.length; i++) {
    hash = userId.charCodeAt(i) + ((hash << 5) - hash);
  }
  return MEMBER_COLORS[Math.abs(hash) % MEMBER_COLORS.length];
}

const Card = ({ icon, title, count, children }) => (
  <div style={{
    background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.08)',
    borderRadius: 20, overflow: 'hidden',
  }}>
    <div style={{
      padding: '20px 24px', borderBottom: '1px solid rgba(255,255,255,0.06)',
      display: 'flex', alignItems: 'center', gap: 10,
    }}>
      <span style={{
        width: 34, height: 34, borderRadius: 9,
        background: 'linear-gradient(135deg, #10b981, #059669)',
        display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 16,
      }}>{icon}</span>
      <span style={{ fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: 16, color: '#f0f4ff' }}>{title}</span>
      <span style={{
        marginLeft: 'auto', background: 'rgba(16,185,129,0.1)', color: '#10b981',
        fontSize: 12, fontWeight: 700, padding: '3px 10px', borderRadius: 99,
      }}>{count}</span>
    </div>
    <div style={{ padding: 24 }}>{children}</div>
  </div>
);

export default function Room({ roomId, user, onExit }) {
  const [tasks, setTasks] = useState([]);
  const [items, setItems] = useState([]);
  const [members, setMembers] = useState([]);
  const [userMap, setUserMap] = useState({});
  const [taskInput, setTaskInput] = useState('');
  const [itemInput, setItemInput] = useState('');
  const [itemPrice, setItemPrice] = useState('');
  const [roomName, setRoomName] = useState('');
  const [editingName, setEditingName] = useState(false);
  const [nameInput, setNameInput] = useState('');
  const [copied, setCopied] = useState(false);

  const fetchUserMap = useCallback(async (userIds) => {
    if (!userIds.length) return;
    const { data: users } = await supabase
      .from('USERS')
      .select('user_id, user_name')
      .in('user_id', userIds);
    const map = {};
    (users || []).forEach(u => map[u.user_id] = u.user_name);
    setUserMap(prev => ({ ...prev, ...map }));
  }, []);

  const loadTasks = useCallback(async () => {
    const { data, error } = await supabase
      .from('TASKS').select('*')
      .eq('room_id', roomId)
      .order('created_at', { ascending: true });
    if (error) return console.error(error);
    setTasks(data || []);
    fetchUserMap([...new Set((data || []).map(t => t.user_id))]);
  }, [roomId, fetchUserMap]);

  const loadShoppingItems = useCallback(async () => {
    const { data, error } = await supabase
      .from('SHOPPING_ITEMS').select('*')
      .eq('room_id', roomId)
      .order('is_purchased', { ascending: true })
      .order('created_at', { ascending: true });
    if (error) return console.error(error);
    setItems(data || []);
    fetchUserMap([...new Set((data || []).map(i => i.added_by))]);
  }, [roomId, fetchUserMap]);

  const loadRoomName = useCallback(async () => {
    const { data, error } = await supabase
      .from('ROOMS').select('name')
      .eq('room_id', roomId).single();
    if (error) return;
    setRoomName(data.name ?? 'Unnamed Room');
  }, [roomId]);

  const loadMembers = useCallback(async () => {
    const { data: memberships, error } = await supabase
      .from('MEMBERSHIP').select('user_id')
      .eq('room_id', roomId);
    if (error) return console.error(error);

    const userIds = (memberships || []).map(m => m.user_id);
    if (!userIds.length) return;

    const { data: users } = await supabase
      .from('USERS').select('user_id, user_name')
      .in('user_id', userIds);

    setMembers(users || []);
  }, [roomId]);

  useEffect(() => {
    loadTasks();
    loadShoppingItems();
    loadRoomName();
    loadMembers();

    const channel = supabase
      .channel(`room-${roomId}`)
      .on('postgres_changes',
        { event: '*', schema: 'public', table: 'TASKS', filter: `room_id=eq.${roomId}` },
        () => loadTasks()
      )
      .on('postgres_changes',
        { event: '*', schema: 'public', table: 'SHOPPING_ITEMS', filter: `room_id=eq.${roomId}` },
        () => loadShoppingItems()
      )
      .on('postgres_changes',
        { event: '*', schema: 'public', table: 'MEMBERSHIP', filter: `room_id=eq.${roomId}` },
        () => loadMembers()
      )
      .subscribe();

    return () => supabase.removeChannel(channel);
  }, [roomId, loadTasks, loadShoppingItems, loadRoomName, loadMembers]);

  async function addTask() {
    const description = taskInput.trim();
    if (!description) return;
    setTaskInput('');
    const { error } = await supabase
      .from('TASKS')
      .insert({ room_id: roomId, user_id: user.id, description });
    if (error) alert(error.message);
    await loadTasks(); 
  }

  async function deleteTask(taskId) {
    setTasks(prev => prev.filter(t => t.task_id !== taskId));
    await supabase.from('TASKS').delete().eq('task_id', taskId);
  }

  async function addItem() {
    const item = itemInput.trim();
    if (!item) return;
    const price = parseFloat(itemPrice) || 0;
    setItemInput('');
    setItemPrice('');
    const { error } = await supabase
      .from('SHOPPING_ITEMS')
      .insert({ room_id: roomId, added_by: user.id, item, item_price: price });
    if (error) return alert(error.message);
    await loadShoppingItems();
  }

  async function toggleItem(itemId, currentValue) {
    if (String(itemId).startsWith('temp-')) return;

    setItems(prev => {
      const updated = prev.map(i =>
        i.item_id === itemId ? { ...i, is_purchased: !currentValue } : i
      );
      return [
        ...updated.filter(i => !i.is_purchased),
        ...updated.filter(i => i.is_purchased),
      ];
    });

    const { error } = await supabase
      .from('SHOPPING_ITEMS')
      .update({ is_purchased: !currentValue })
      .eq('item_id', itemId);

    if (error) {
      console.error('Failed to update item:', error);
      setItems(prev => {
        const reverted = prev.map(i =>
          i.item_id === itemId ? { ...i, is_purchased: currentValue } : i
        );
        return [
          ...reverted.filter(i => !i.is_purchased),
          ...reverted.filter(i => i.is_purchased),
        ];
      });
    }
  }

  async function saveRoomName() {
    const newName = nameInput.trim();
    if (!newName) return;
    const { error } = await supabase
      .from('ROOMS').update({ name: newName }).eq('room_id', roomId);
    if (error) return alert('Failed to rename: ' + error.message);
    setRoomName(newName);
    setEditingName(false);
  }

  function copyRoomId() {
    navigator.clipboard.writeText(roomId);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  const inputStyle = {
    background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.1)',
    borderRadius: 10, padding: '11px 14px', color: '#f0f4ff', fontSize: 14,
    outline: 'none', fontFamily: 'DM Sans, sans-serif', flex: 1,
  };

  return (
    <div style={{ minHeight: '100vh', background: '#0a0f1e' }}>

      {/* Nav */}
      <div style={{
        borderBottom: '1px solid rgba(255,255,255,0.06)', padding: '0 40px',
        display: 'flex', alignItems: 'center', justifyContent: 'space-between', height: 64,
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <span style={{ fontSize: 20 }}>🏠</span>
          <span style={{ fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: 18, color: '#f0f4ff' }}>
            RoomieQuest
          </span>
        </div>
        <button
          onClick={onExit}
          style={{
            background: 'rgba(255,255,255,0.06)', border: '1px solid rgba(255,255,255,0.1)',
            borderRadius: 10, padding: '8px 16px', color: '#94a3b8', fontSize: 14,
            cursor: 'pointer', fontFamily: 'DM Sans, sans-serif', transition: 'color 0.15s',
          }}
          onMouseEnter={e => e.target.style.color = '#f0f4ff'}
          onMouseLeave={e => e.target.style.color = '#94a3b8'}
        >
          ← Dashboard
        </button>
      </div>

      <div style={{ maxWidth: 1100, margin: '0 auto', padding: '48px 40px' }}>

        {/* Room title + rename */}
        <div className="fade-up" style={{ marginBottom: 32 }}>
          {editingName ? (
            <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
              <input
                value={nameInput}
                onChange={e => setNameInput(e.target.value)}
                onKeyDown={e => {
                  if (e.key === 'Enter') saveRoomName();
                  if (e.key === 'Escape') setEditingName(false);
                }}
                autoFocus
                style={{
                  background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(16,185,129,0.5)',
                  borderRadius: 10, padding: '8px 14px', color: '#f0f4ff',
                  fontSize: 28, fontFamily: 'Syne, sans-serif', fontWeight: 800,
                  outline: 'none', letterSpacing: '-0.5px',
                }}
              />
              <button onClick={saveRoomName} style={{
                background: 'linear-gradient(135deg, #10b981, #059669)',
                border: 'none', borderRadius: 8, padding: '8px 16px',
                color: 'white', fontSize: 13, fontWeight: 600, cursor: 'pointer',
              }}>Save</button>
              <button onClick={() => setEditingName(false)} style={{
                background: 'none', border: 'none', color: '#475569', cursor: 'pointer', fontSize: 13,
              }}>Cancel</button>
            </div>
          ) : (
            <div style={{ display: 'flex', alignItems: 'center', gap: 12, flexWrap: 'wrap' }}>
              <h1 style={{ fontSize: 36, fontWeight: 800, margin: 0, letterSpacing: '-0.5px', color: '#f0f4ff' }}>
                {roomName || 'Loading...'}
              </h1>
              <button
                onClick={() => { setNameInput(roomName); setEditingName(true); }}
                style={{
                  background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.1)',
                  borderRadius: 8, padding: '4px 10px', color: '#475569', fontSize: 12,
                  cursor: 'pointer', fontFamily: 'DM Sans, sans-serif',
                }}
              >rename</button>
            </div>
          )}

          {/* Room ID + share */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginTop: 8 }}>
            <p style={{ color: '#475569', fontSize: 13, fontFamily: 'monospace', margin: 0 }}>
              {roomId}
            </p>
            <button
              onClick={copyRoomId}
              style={{
                background: copied ? 'rgba(16,185,129,0.15)' : 'rgba(255,255,255,0.05)',
                border: `1px solid ${copied ? 'rgba(16,185,129,0.4)' : 'rgba(255,255,255,0.1)'}`,
                borderRadius: 8, padding: '3px 10px',
                color: copied ? '#10b981' : '#475569', fontSize: 12,
                cursor: 'pointer', fontFamily: 'DM Sans, sans-serif',
                transition: 'all 0.2s',
              }}
            >
              {copied ? '✓ Copied!' : 'Copy ID'}
            </button>
          </div>
        </div>

        {/* Members bar */}
        <div style={{
          display: 'flex', alignItems: 'center', gap: 12,
          marginBottom: 32, padding: '14px 20px',
          background: 'rgba(255,255,255,0.02)',
          border: '1px solid rgba(255,255,255,0.06)',
          borderRadius: 14,
        }}>
          <span style={{ fontSize: 13, color: '#475569', fontWeight: 500 }}>Members</span>
          <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
            {members.map(m => (
              <div
                key={m.user_id}
                title={m.user_name}
                style={{
                  display: 'flex', alignItems: 'center', gap: 7,
                  background: 'rgba(255,255,255,0.04)',
                  border: '1px solid rgba(255,255,255,0.08)',
                  borderRadius: 99, padding: '4px 12px 4px 6px',
                }}
              >
                <div style={{
                  width: 26, height: 26, borderRadius: '50%',
                  background: getMemberColor(m.user_id),
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  fontSize: 11, fontWeight: 700, color: 'white',
                  flexShrink: 0,
                }}>
                  {getInitials(m.user_name)}
                </div>
                <span style={{ fontSize: 13, color: '#e2e8f0' }}>{m.user_name}</span>
                {m.user_id === user.id && (
                  <span style={{ fontSize: 11, color: '#475569' }}>(you)</span>
                )}
              </div>
            ))}
          </div>
          <span style={{ marginLeft: 'auto', fontSize: 12, color: '#475569' }}>
            {members.length}/5 members
          </span>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24 }}>

          {/* Tasks */}
          <Card icon="✓" title="Tasks" count={tasks.length}>
            <div style={{ display: 'flex', gap: 8, marginBottom: 20 }}>
              <input
                style={inputStyle}
                placeholder="Add a task..."
                value={taskInput}
                onChange={e => setTaskInput(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && addTask()}
              />
              <button onClick={addTask} style={{
                background: 'linear-gradient(135deg, #10b981, #059669)',
                border: 'none', borderRadius: 10, padding: '0 18px',
                color: 'white', fontWeight: 700, cursor: 'pointer', fontSize: 18,
                boxShadow: '0 4px 16px rgba(16,185,129,0.2)',
              }}>+</button>
            </div>

            {tasks.length === 0 ? (
              <p style={{ color: '#475569', fontSize: 14, textAlign: 'center', padding: '24px 0' }}>
                No tasks yet
              </p>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
                {tasks.map(t => (
                  <div
                    key={t.task_id}
                    className="fade-in"
                    style={{
                      display: 'flex', alignItems: 'center', gap: 12,
                      padding: '10px 12px', borderRadius: 10,
                      background: 'rgba(255,255,255,0.02)',
                      transition: 'background 0.15s',
                    }}
                    onMouseEnter={e => e.currentTarget.style.background = 'rgba(255,255,255,0.05)'}
                    onMouseLeave={e => e.currentTarget.style.background = 'rgba(255,255,255,0.02)'}
                  >
                    <input
                      type="checkbox"
                      onChange={() => deleteTask(t.task_id)}
                      style={{ accentColor: '#10b981', width: 16, height: 16, cursor: 'pointer' }}
                    />
                    <div style={{ flex: 1, display: 'flex', alignItems: 'center', gap: 8 }}>
                      <span style={{ fontSize: 14, color: '#e2e8f0' }}>{t.description}</span>
                      <div style={{
                        width: 20, height: 20, borderRadius: '50%',
                        background: getMemberColor(t.user_id),
                        display: 'flex', alignItems: 'center', justifyContent: 'center',
                        fontSize: 9, fontWeight: 700, color: 'white', flexShrink: 0,
                        title: userMap[t.user_id] ?? 'unknown',
                      }}>
                        {getInitials(userMap[t.user_id] ?? '?')}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </Card>

          {/* Shopping */}
          <Card icon="🛒" title="Shopping List" count={items.filter(i => !i.is_purchased).length}>
            <div style={{ display: 'flex', gap: 8, marginBottom: 8 }}>
              <input
                style={inputStyle}
                placeholder="Item name..."
                value={itemInput}
                onChange={e => setItemInput(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && addItem()}
              />
              <input
                style={{ ...inputStyle, flex: 'none', width: 72 }}
                placeholder="$0"
                value={itemPrice}
                onChange={e => setItemPrice(e.target.value)}
              />
            </div>
            <button onClick={addItem} style={{
              width: '100%', padding: '11px', marginBottom: 20,
              background: 'linear-gradient(135deg, #10b981, #059669)',
              border: 'none', borderRadius: 10, color: 'white',
              fontWeight: 700, fontSize: 14, cursor: 'pointer',
              fontFamily: 'Syne, sans-serif',
              boxShadow: '0 4px 16px rgba(16,185,129,0.2)',
            }}>
              Add Item
            </button>

            {items.length === 0 ? (
              <p style={{ color: '#475569', fontSize: 14, textAlign: 'center', padding: '24px 0' }}>
                No items yet
              </p>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
                {items.map(i => (
                  <div
                    key={i.item_id}
                    className="fade-in"
                    style={{
                      display: 'flex', alignItems: 'center', gap: 12,
                      padding: '10px 12px', borderRadius: 10,
                      background: 'rgba(255,255,255,0.02)',
                      transition: 'background 0.15s',
                    }}
                    onMouseEnter={e => e.currentTarget.style.background = 'rgba(255,255,255,0.05)'}
                    onMouseLeave={e => e.currentTarget.style.background = 'rgba(255,255,255,0.02)'}
                  >
                    <input
                      type="checkbox"
                      checked={i.is_purchased}
                      onChange={() => toggleItem(i.item_id, i.is_purchased)}
                      style={{ accentColor: '#10b981', width: 16, height: 16, cursor: 'pointer' }}
                    />
                    <div style={{ flex: 1, display: 'flex', alignItems: 'center', gap: 8 }}>
                      <span style={{
                        fontSize: 14,
                        color: i.is_purchased ? '#475569' : '#e2e8f0',
                        textDecoration: i.is_purchased ? 'line-through' : 'none',
                      }}>
                        {i.item}
                      </span>
                      <div style={{
                        width: 20, height: 20, borderRadius: '50%',
                        background: getMemberColor(i.added_by),
                        display: 'flex', alignItems: 'center', justifyContent: 'center',
                        fontSize: 9, fontWeight: 700, color: 'white', flexShrink: 0,
                      }}>
                        {getInitials(userMap[i.added_by] ?? '?')}
                      </div>
                    </div>
                    {i.item_price > 0 && (
                      <span style={{
                        fontSize: 12, color: '#10b981', fontWeight: 700,
                        background: 'rgba(16,185,129,0.1)', padding: '2px 8px', borderRadius: 99,
                      }}>
                        ${Number(i.item_price).toFixed(2)}
                      </span>
                    )}
                  </div>
                ))}
              </div>
            )}
          </Card>

        </div>
      </div>
    </div>
  );
}
