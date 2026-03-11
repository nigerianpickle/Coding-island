import { useState } from 'react';
import { supabase } from '../supabaseClient';

export default function Auth() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleLogin() {
    setLoading(true);
    const { error } = await supabase.auth.signInWithPassword({ email, password });
    if (error) alert(error.message);
    setLoading(false);
  }

  async function handleSignup() {
    setLoading(true);
    const { error: loginError } = await supabase.auth.signInWithPassword({ email, password });

    if (loginError && loginError.message.includes('Invalid login credentials')) {
      const { data: signUpData, error: signupError } = await supabase.auth.signUp({ email, password });
      if (signupError) { alert(signupError.message); setLoading(false); return; }

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
    setLoading(false);
  }

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: '#0a0f1e',
      padding: '24px',
      position: 'relative',
      overflow: 'hidden',
    }}>
      {/* Background glow effects */}
      <div style={{
        position: 'absolute', width: 600, height: 600,
        borderRadius: '50%',
        background: 'radial-gradient(circle, rgba(16,185,129,0.08) 0%, transparent 70%)',
        top: '-200px', right: '-200px', pointerEvents: 'none'
      }} />
      <div style={{
        position: 'absolute', width: 400, height: 400,
        borderRadius: '50%',
        background: 'radial-gradient(circle, rgba(99,102,241,0.08) 0%, transparent 70%)',
        bottom: '-100px', left: '-100px', pointerEvents: 'none'
      }} />

      <div className="fade-up" style={{
        width: '100%', maxWidth: 420,
        background: 'rgba(255,255,255,0.03)',
        border: '1px solid rgba(255,255,255,0.08)',
        borderRadius: 20,
        padding: '48px 40px',
        backdropFilter: 'blur(20px)',
        position: 'relative',
      }}>
        {/* Logo */}
        <div style={{ marginBottom: 32 }}>
          <div style={{
            display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
            width: 48, height: 48, borderRadius: 14,
            background: 'linear-gradient(135deg, #10b981, #059669)',
            fontSize: 22, marginBottom: 20,
            boxShadow: '0 0 24px rgba(16,185,129,0.3)',
          }}>🏠</div>
          <h1 style={{ fontSize: 32, fontWeight: 800, margin: 0, letterSpacing: '-0.5px', color: '#f0f4ff' }}>
            RoomieQuest
          </h1>
          <p style={{ color: '#64748b', fontSize: 15, marginTop: 6 }}>
            Live smarter together.
          </p>
        </div>

        {/* Inputs */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 12, marginBottom: 24 }}>
          {[
            { id: 'email', type: 'email', placeholder: 'Email address', value: email, set: setEmail },
            { id: 'pass', type: 'password', placeholder: 'Password', value: password, set: setPassword },
          ].map(field => (
            <input
              key={field.id}
              type={field.type}
              placeholder={field.placeholder}
              value={field.value}
              onChange={e => field.set(e.target.value)}
              style={{
                background: 'rgba(255,255,255,0.05)',
                border: '1px solid rgba(255,255,255,0.1)',
                borderRadius: 12, padding: '14px 16px',
                color: '#f0f4ff', fontSize: 15, outline: 'none',
                fontFamily: 'DM Sans, sans-serif',
                transition: 'border-color 0.2s',
              }}
              onFocus={e => e.target.style.borderColor = 'rgba(16,185,129,0.5)'}
              onBlur={e => e.target.style.borderColor = 'rgba(255,255,255,0.1)'}
            />
          ))}
        </div>

        {/* Buttons */}
        <div style={{ display: 'flex', gap: 10 }}>
          <button
            onClick={handleSignup}
            disabled={loading}
            style={{
              flex: 1, padding: '14px',
              background: 'linear-gradient(135deg, #10b981, #059669)',
              color: 'white', border: 'none', borderRadius: 12,
              fontSize: 15, fontWeight: 600, cursor: 'pointer',
              fontFamily: 'Syne, sans-serif',
              boxShadow: '0 4px 20px rgba(16,185,129,0.25)',
              transition: 'transform 0.15s, box-shadow 0.15s',
            }}
            onMouseEnter={e => { e.target.style.transform = 'translateY(-1px)'; e.target.style.boxShadow = '0 6px 24px rgba(16,185,129,0.35)'; }}
            onMouseLeave={e => { e.target.style.transform = 'translateY(0)'; e.target.style.boxShadow = '0 4px 20px rgba(16,185,129,0.25)'; }}
          >
            Sign Up
          </button>
          <button
            onClick={handleLogin}
            disabled={loading}
            style={{
              flex: 1, padding: '14px',
              background: 'rgba(255,255,255,0.06)',
              color: '#f0f4ff', border: '1px solid rgba(255,255,255,0.1)',
              borderRadius: 12, fontSize: 15, fontWeight: 600,
              cursor: 'pointer', fontFamily: 'Syne, sans-serif',
              transition: 'background 0.15s, transform 0.15s',
            }}
            onMouseEnter={e => { e.target.style.background = 'rgba(255,255,255,0.1)'; e.target.style.transform = 'translateY(-1px)'; }}
            onMouseLeave={e => { e.target.style.background = 'rgba(255,255,255,0.06)'; e.target.style.transform = 'translateY(0)'; }}
          >
            Log In
          </button>
        </div>
      </div>
    </div>
  );
}