import { useState, useEffect } from 'react';
import { supabase } from './supabaseClient';
import Auth from './components/Auth';
import Dashboard from './components/Dashboard';
import Room from './components/Room';
import Landing from './components/Landing';

export default function App() {
  const [user, setUser] = useState(null);
  const [activeRoomId, setActiveRoomId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showLanding, setShowLanding] = useState(true);

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null);
      if (session?.user) setShowLanding(false);
      setLoading(false);
    });

    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null);
      if (session?.user) setShowLanding(false);
    });

    return () => subscription.unsubscribe();
  }, []);

  if (loading) return (
    <div style={{
      minHeight: '100vh', background: '#0a0f1e',
      display: 'flex', alignItems: 'center', justifyContent: 'center',
    }}>
      <div style={{
        width: 36, height: 36, borderRadius: '50%',
        border: '3px solid rgba(16,185,129,0.2)',
        borderTop: '3px solid #10b981',
        animation: 'spin 0.8s linear infinite',
      }} />
      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
    </div>
  );

  if (showLanding && !user) return <Landing onGetStarted={() => setShowLanding(false)} />;
  if (!user) return <Auth />;
  if (activeRoomId) return <Room roomId={activeRoomId} user={user} onExit={() => setActiveRoomId(null)} />;
  return <Dashboard user={user} onEnterRoom={setActiveRoomId} />;
}
