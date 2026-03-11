import { useState, useEffect } from 'react';
import { supabase } from '../supabaseClient';

const ADJECTIVES = ['Purple', 'Golden', 'Silent', 'Cosmic', 'Lazy', 'Brave', 'Fuzzy', 'Mighty', 'Swift', 'Chill'];
const NOUNS = ['Penguin', 'Cactus', 'Noodle', 'Rocket', 'Panda', 'Waffle', 'Comet', 'Pickle', 'Sloth', 'Mango'];

function generateRoomName() {
  const adj = ADJECTIVES[Math.floor(Math.random() * ADJECTIVES.length)];
  const noun = NOUNS[Math.floor(Math.random() * NOUNS.length)];
  return `${adj} ${noun}`;
}

const btnBase = {
  border: 'none', borderRadius: 10, fontSize: 14,
  fontWeight: 600, cursor: 'pointer', fontFamily: 'DM Sans, sans-serif',
  transition: 'transform 0.15s, opacity 0.15s',
};

export default function Dashboard({ user, onEnterRoom }) {
  const [rooms, setRooms] = useState([]);
  const [roomPassword, setRoomPassword] = useState('');
  const [joinRoomId, setJoinRoomId] = useState('');
  const [joinPassword, setJoinPassword] = useState('');

  useEffect(() => { loadRooms(); }, []);

  async function loadRooms() {
    const { data: memberships, error } = await supabase
      .from('MEMBERSHIP').select('room_id').eq('user_id', user.id);
    if (error || !memberships?.length) return setRooms([]);

    const roomIds = memberships.map(m => m.room_id);
    const { data: rooms } = await supabase.from('ROOMS').select('*').in('room_id', roomIds);
    setRooms(rooms || []);
  }

  async function createRoom() {
    if (rooms.length >= 3) return alert('You can only be in up to 3 rooms.');

    const name = generateRoomName();

    const { data: room, error } = await supabase
      .from('ROOMS')
      .insert({ password: roomPassword, name })
      .select()
      .single();

    if (error) return alert(error.message);

    const { error: membershipError } = await supabase
      .from('MEMBERSHIP')
      .insert({ user_id: user.id, room_id: room.room_id });

    if (membershipError) return alert(membershipError.message);

    setRoomPassword('');
    loadRooms();
  }

  async function joinRoom() {
    if (rooms.length >= 3) return alert('You can only be in up to 3 rooms.');

    const { data: room, error } = await supabase
      .from('ROOMS').select('*')
      .eq('room_id', joinRoomId).eq('password', joinPassword).single();

    if (error || !room) return alert('Invalid room or password');

    const { error: membershipError } = await supabase
      .from('MEMBERSHIP')
      .insert({ user_id: user.id, room_id: room.room_id });

    if (membershipError) return alert(membershipError.message);

    setJoinRoomId('');
    setJoinPassword('');
    loadRooms();
  }

  const inputStyle = {
    background: 'rgba(255,255,255,0.05)',
    border: '1px solid rgba(255,255,255,0.1)',
    borderRadius: 10, padding: '11px 14px',
    color: '#f0f4ff', fontSize: 14, outline: 'none',
    fontFamily: 'DM Sans, sans-serif', width: '100%',
  };

  return (
    <div style={{ minHeight: '100vh', background: '#0a0f1e', padding: '0 0 60px' }}>

      {/* Nav */}
      <div style={{
        borderBottom: '1px solid rgba(255,255,255,0.06)',
        padding: '0 40px',
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        height: 64,
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <span style={{ fontSize: 20 }}>🏠</span>
          <span style={{ fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: 18, color: '#f0f4ff' }}>
            RoomieQuest
          </span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
          <span style={{ color: '#64748b', fontSize: 14 }}>{user.email}</span>
          <button
            onClick={() => supabase.auth.signOut()}
            style={{ ...btnBase, padding: '8px 16px', background: 'rgba(239,68,68,0.1)', color: '#f87171', border: '1px solid rgba(239,68,68,0.2)' }}
          >
            Logout
          </button>
        </div>
      </div>

      <div style={{ maxWidth: 1100, margin: '0 auto', padding: '48px 40px' }}>

        {/* Hero text */}
        <div className="fade-up" style={{ marginBottom: 48 }}>
          <h1 style={{ fontSize: 42, fontWeight: 800, margin: 0, letterSpacing: '-1px', color: '#f0f4ff' }}>
            Your Rooms
          </h1>
          <p style={{ color: '#64748b', marginTop: 8, fontSize: 16 }}>
            {rooms.length}/3 rooms · Manage your shared spaces.
          </p>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 380px', gap: 32, alignItems: 'start' }}>

          {/* Rooms grid */}
          <div>
            {rooms.length === 0 ? (
              <div className="fade-in" style={{
                border: '1px dashed rgba(255,255,255,0.1)',
                borderRadius: 16, padding: '60px 40px',
                textAlign: 'center', color: '#475569',
              }}>
                <div style={{ fontSize: 40, marginBottom: 12 }}>🚪</div>
                <p style={{ fontSize: 16, fontWeight: 500 }}>No rooms yet</p>
                <p style={{ fontSize: 14, marginTop: 4 }}>Create or join a room to get started</p>
              </div>
            ) : (
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(240px, 1fr))', gap: 16 }}>
                {rooms.map((r, i) => (
                  <div
                    key={r.room_id}
                    className="fade-up"
                    style={{
                      animationDelay: `${i * 0.05}s`,
                      background: 'rgba(255,255,255,0.03)',
                      border: '1px solid rgba(255,255,255,0.08)',
                      borderRadius: 16, padding: '24px',
                      cursor: 'pointer', transition: 'border-color 0.2s, transform 0.2s',
                    }}
                    onMouseEnter={e => { e.currentTarget.style.borderColor = 'rgba(16,185,129,0.4)'; e.currentTarget.style.transform = 'translateY(-2px)'; }}
                    onMouseLeave={e => { e.currentTarget.style.borderColor = 'rgba(255,255,255,0.08)'; e.currentTarget.style.transform = 'translateY(0)'; }}
                    onClick={() => onEnterRoom(r.room_id)}
                  >
                    <div style={{
                      width: 40, height: 40, borderRadius: 10, marginBottom: 16,
                      background: 'linear-gradient(135deg, #10b981, #059669)',
                      display: 'flex', alignItems: 'center', justifyContent: 'center',
                      fontSize: 18,
                    }}>🏠</div>
                    <p style={{ fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: 15, margin: 0, color: '#f0f4ff' }}>
                      {r.name ?? 'Unnamed Room'}
                    </p>
                    <p style={{ fontSize: 11, color: '#475569', margin: '4px 0 16px', fontFamily: 'monospace' }}>
                      ID: {r.room_id.slice(0, 8)}...
                    </p>
                    <span style={{ fontSize: 13, color: '#10b981', fontWeight: 600 }}>
                      Enter →
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Actions panel */}
          <div className="fade-up" style={{ animationDelay: '0.1s' }}>
            <div style={{
              background: 'rgba(255,255,255,0.03)',
              border: '1px solid rgba(255,255,255,0.08)',
              borderRadius: 20, padding: 28,
            }}>

              {/* Create */}
              <div style={{ marginBottom: 32 }}>
                <p style={{ fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: 16, margin: '0 0 14px', color: '#f0f4ff' }}>
                  Create Room
                </p>
                <div style={{ display: 'flex', gap: 8 }}>
                  <input
                    style={inputStyle}
                    placeholder="Set a password"
                    value={roomPassword}
                    onChange={e => setRoomPassword(e.target.value)}
                    onKeyDown={e => e.key === 'Enter' && createRoom()}
                  />
                  <button
                    onClick={createRoom}
                    disabled={rooms.length >= 3}
                    style={{
                      ...btnBase, padding: '11px 18px', whiteSpace: 'nowrap',
                      background: rooms.length >= 3 ? 'rgba(255,255,255,0.05)' : 'linear-gradient(135deg, #10b981, #059669)',
                      color: rooms.length >= 3 ? '#475569' : 'white',
                      boxShadow: rooms.length >= 3 ? 'none' : '0 4px 16px rgba(16,185,129,0.2)',
                      cursor: rooms.length >= 3 ? 'not-allowed' : 'pointer',
                    }}
                  >
                    {rooms.length >= 3 ? 'Limit reached' : 'Create'}
                  </button>
                </div>
                <p style={{ fontSize: 11, color: '#475569', marginTop: 8 }}>
                  A fun name will be auto-generated 🎲
                </p>
              </div>

              <div style={{ borderTop: '1px solid rgba(255,255,255,0.06)', marginBottom: 28 }} />

              {/* Join */}
              <div>
                <p style={{ fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: 16, margin: '0 0 14px', color: '#f0f4ff' }}>
                  Join Room
                </p>
                <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                  <input style={inputStyle} placeholder="Room ID" value={joinRoomId} onChange={e => setJoinRoomId(e.target.value)} />
                  <input style={inputStyle} placeholder="Password" value={joinPassword} onChange={e => setJoinPassword(e.target.value)} onKeyDown={e => e.key === 'Enter' && joinRoom()} />
                  <button
                    onClick={joinRoom}
                    disabled={rooms.length >= 3}
                    style={{
                      ...btnBase, padding: '12px', marginTop: 4,
                      background: rooms.length >= 3 ? 'rgba(255,255,255,0.03)' : 'rgba(255,255,255,0.06)',
                      color: rooms.length >= 3 ? '#475569' : '#f0f4ff',
                      border: '1px solid rgba(255,255,255,0.1)',
                      cursor: rooms.length >= 3 ? 'not-allowed' : 'pointer',
                    }}
                  >
                    {rooms.length >= 3 ? 'Limit reached' : 'Join Room'}
                  </button>
                </div>
              </div>

            </div>
          </div>

        </div>
      </div>
    </div>
  );
}
