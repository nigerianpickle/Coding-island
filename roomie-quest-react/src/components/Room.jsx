import { useState, useEffect } from 'react';
import { supabase } from '../supabaseClient';


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
  const [userMap, setUserMap] = useState({});
  const [taskInput, setTaskInput] = useState('');
  const [itemInput, setItemInput] = useState('');
  const [itemPrice, setItemPrice] = useState('');

  useEffect(() => {
    loadTasks();
    loadShoppingItems();

    const channel = supabase
      .channel(`room-${roomId}`)
      .on('postgres_changes', { event: '*', schema: 'public', table: 'TASKS', filter: `room_id=eq.${roomId}` }, () => loadTasks())
      .on('postgres_changes', { event: '*', schema: 'public', table: 'SHOPPING_ITEMS', filter: `room_id=eq.${roomId}` }, () => loadShoppingItems())
      .subscribe();

    return () => supabase.removeChannel(channel);
  }, [roomId]);

  async function fetchUserMap(userIds) {
    if (!userIds.length) return;
    const { data: users } = await supabase.from('USERS').select('user_id, user_name').in('user_id', userIds);
    const map = {};
    (users || []).forEach(u => map[u.user_id] = u.user_name);
    setUserMap(prev => ({ ...prev, ...map }));
  }

  async function loadTasks() {
    const { data, error } = await supabase.from('TASKS').select('*').eq('room_id', roomId).order('created_at', { ascending: true });
    if (error) return console.error(error);
    setTasks(data || []);
    fetchUserMap([...new Set((data || []).map(t => t.user_id))]);
  }

  async function loadShoppingItems() {
    const { data, error } = await supabase.from('SHOPPING_ITEMS').select('*').eq('room_id', roomId)
      .order('is_purchased', { ascending: true }).order('created_at', { ascending: true });
    if (error) return console.error(error);
    setItems(data || []);
    fetchUserMap([...new Set((data || []).map(i => i.added_by))]);
  }

  async function addTask() {
    const description = taskInput.trim();
    if (!description) return;
    setTaskInput('');
    const tempTask = { task_id: 'temp-' + Date.now(), description, user_id: user.id, room_id: roomId };
    setTasks(prev => [...prev, tempTask]);
    const { error } = await supabase.from('TASKS').insert({ room_id: roomId, user_id: user.id, description });
    if (error) { alert(error.message); setTasks(prev => prev.filter(t => t.task_id !== tempTask.task_id)); }
  }

  async function deleteTask(taskId) {
    setTasks(prev => prev.filter(t => t.task_id !== taskId));
    await supabase.from('TASKS').delete().eq('task_id', taskId);
  }

  async function addItem() {
    const item = itemInput.trim();
    if (!item) return;
    const price = parseFloat(itemPrice) || 0;
    setItemInput(''); setItemPrice('');
    const tempItem = { item_id: 'temp-' + Date.now(), item, added_by: user.id, is_purchased: false, item_price: price };
    setItems(prev => [...prev, tempItem]);
    const { error } = await supabase.from('SHOPPING_ITEMS').insert({ room_id: roomId, added_by: user.id, item, item_price: price });
    if (error) { alert(error.message); setItems(prev => prev.filter(i => i.item_id !== tempItem.item_id)); }
  }

  async function toggleItem(itemId, currentValue) {
    setItems(prev => {
      const updated = prev.map(i => i.item_id === itemId ? { ...i, is_purchased: !currentValue } : i);
      return [...updated.filter(i => !i.is_purchased), ...updated.filter(i => i.is_purchased)];
    });
    await supabase.from('SHOPPING_ITEMS').update({ is_purchased: !currentValue }).eq('item_id', itemId);
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
          <span style={{ fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: 18, color: '#f0f4ff' }}>RoomieQuest</span>
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
        <div className="fade-up" style={{ marginBottom: 40 }}>
          <h1 style={{ fontSize: 36, fontWeight: 800, margin: 0, letterSpacing: '-0.5px', color: '#f0f4ff' }}>
            Your Room
          </h1>
          <p style={{ color: '#475569', fontSize: 13, marginTop: 6, fontFamily: 'monospace' }}>
            {roomId}
          </p>
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
              <p style={{ color: '#475569', fontSize: 14, textAlign: 'center', padding: '24px 0' }}>No tasks yet</p>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
                {tasks.map(t => (
                  <div key={t.task_id} className="fade-in" style={{
                    display: 'flex', alignItems: 'center', gap: 12,
                    padding: '10px 12px', borderRadius: 10,
                    background: 'rgba(255,255,255,0.02)',
                    opacity: t.task_id.startsWith('temp-') ? 0.5 : 1,
                    transition: 'background 0.15s',
                  }}
                    onMouseEnter={e => e.currentTarget.style.background = 'rgba(255,255,255,0.05)'}
                    onMouseLeave={e => e.currentTarget.style.background = 'rgba(255,255,255,0.02)'}
                  >
                    <input
                      type="checkbox"
                      onChange={() => !t.task_id.startsWith('temp-') && deleteTask(t.task_id)}
                      style={{ accentColor: '#10b981', width: 16, height: 16, cursor: 'pointer' }}
                    />
                    <div style={{ flex: 1 }}>
                      <span style={{ fontSize: 14, color: '#e2e8f0' }}>{t.description}</span>
                      <span style={{ fontSize: 11, color: '#475569', marginLeft: 8 }}>
                        by {userMap[t.user_id] ?? 'you'}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </Card>

          {/* Shopping */}
          <Card icon="🛒" title="Shopping List" count={items.filter(i => !i.is_purchased).length}>
            <div style={{ display: 'flex', gap: 8, marginBottom: 8 }}>
              <input style={inputStyle} placeholder="Item name..." value={itemInput} onChange={e => setItemInput(e.target.value)} onKeyDown={e => e.key === 'Enter' && addItem()} />
              <input
                style={{ ...inputStyle, flex: 'none', width: 72 }}
                placeholder="$0" value={itemPrice} onChange={e => setItemPrice(e.target.value)}
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
              <p style={{ color: '#475569', fontSize: 14, textAlign: 'center', padding: '24px 0' }}>No items yet</p>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
                {items.map(i => (
                  <div key={i.item_id} className="fade-in" style={{
                    display: 'flex', alignItems: 'center', gap: 12,
                    padding: '10px 12px', borderRadius: 10,
                    background: 'rgba(255,255,255,0.02)',
                    opacity: i.item_id.startsWith('temp-') ? 0.5 : 1,
                    transition: 'background 0.15s',
                  }}
                    onMouseEnter={e => e.currentTarget.style.background = 'rgba(255,255,255,0.05)'}
                    onMouseLeave={e => e.currentTarget.style.background = 'rgba(255,255,255,0.02)'}
                  >
                    <input
                      type="checkbox"
                      checked={i.is_purchased}
                      onChange={() => !i.item_id.startsWith('temp-') && toggleItem(i.item_id, i.is_purchased)}
                      style={{ accentColor: '#10b981', width: 16, height: 16, cursor: 'pointer' }}
                    />
                    <div style={{ flex: 1 }}>
                      <span style={{
                        fontSize: 14,
                        color: i.is_purchased ? '#475569' : '#e2e8f0',
                        textDecoration: i.is_purchased ? 'line-through' : 'none',
                      }}>{i.item}</span>
                      <span style={{ fontSize: 11, color: '#475569', marginLeft: 8 }}>
                        by {userMap[i.added_by] ?? 'you'}
                      </span>
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