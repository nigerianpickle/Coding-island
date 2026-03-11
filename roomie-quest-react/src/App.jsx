import { useState, useEffect } from 'react';
import { supabase } from './supabaseClient';
import Auth from './components/Auth';
import Dashboard from './components/Dashboard';
import Room from './components/Room';

export default function App() {
  const [user, setUser] = useState(null);
  const [activeRoomId, setActiveRoomId] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // check if user is already logged in
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null);
      setLoading(false);
    });

    // listen for login/logout events
    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null);
    });

    return () => subscription.unsubscribe();
  }, []);

  if (loading) return <div className="flex items-center justify-center min-h-screen">Loading...</div>;

  // This is your "routing" — pure React, no style.display hacks
  if (!user) return <Auth />;
  if (activeRoomId) return <Room roomId={activeRoomId} user={user} onExit={() => setActiveRoomId(null)} />;
  return <Dashboard user={user} onEnterRoom={setActiveRoomId} />;
}