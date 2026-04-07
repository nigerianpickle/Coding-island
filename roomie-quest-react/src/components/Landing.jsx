import { useEffect, useRef } from 'react';

const features = [
  {
    icon: '✓',
    title: 'Shared Task List',
    desc: 'Add tasks, check them off, and they disappear for everyone instantly. No more "did you do the dishes?" texts.',
  },
  {
    icon: '🛒',
    title: 'Shopping List',
    desc: 'Add items with prices, mark as purchased. Bought items sink to the bottom automatically.',
  },
  {
    icon: '⚡',
    title: 'Real-time Sync',
    desc: "Every change appears instantly on every roommate's screen. No refreshing, no lag.",
  },
  {
    icon: '🔒',
    title: 'Private Rooms',
    desc: 'Create a room with a password. Only people you share it with can join. Max 5 roommates.',
  },
  {
    icon: '🎲',
    title: 'Auto Room Names',
    desc: 'Rooms get fun generated names like "Chill Mango" or "Fuzzy Rocket" so you can tell them apart.',
  },
  {
    icon: '👥',
    title: 'See Who Did What',
    desc: "Every task and item shows who added it with a color-coded initial badge.",
  },
];

const steps = [
  {
    num: '01',
    title: 'Create a room',
    desc: 'Sign up, hit create, set a password. Your room gets a fun name automatically.',
  },
  {
    num: '02',
    title: 'Share the room ID',
    desc: 'Copy your room ID with one click and send it to your roommates.',
  },
  {
    num: '03',
    title: 'Stay organized together',
    desc: 'Add tasks, manage the shopping list. Everything updates live for everyone.',
  },
];

export default function Landing({ onGetStarted }) {
  const heroRef = useRef(null);

  useEffect(() => {
    const handleMouseMove = (e) => {
      if (!heroRef.current) return;
      const { clientX, clientY } = e;
      const { innerWidth, innerHeight } = window;
      const x = (clientX / innerWidth - 0.5) * 20;
      const y = (clientY / innerHeight - 0.5) * 20;
      heroRef.current.style.setProperty('--mouse-x', `${x}px`);
      heroRef.current.style.setProperty('--mouse-y', `${y}px`);
    };
    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  return (
    <div style={{ minHeight: '100vh', background: '#0a0f1e', color: '#f0f4ff', overflowX: 'hidden' }}>

      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

        * { box-sizing: border-box; margin: 0; padding: 0; }

        @keyframes fadeUp {
          from { opacity: 0; transform: translateY(24px); }
          to { opacity: 1; transform: translateY(0); }
        }
        @keyframes float {
          0%, 100% { transform: translateY(0px); }
          50% { transform: translateY(-10px); }
        }
        @keyframes pulse-glow {
          0%, 100% { box-shadow: 0 0 40px rgba(16,185,129,0.2); }
          50% { box-shadow: 0 0 80px rgba(16,185,129,0.4); }
        }
        @keyframes shimmer {
          0% { background-position: -200% center; }
          100% { background-position: 200% center; }
        }
        @keyframes spin-slow {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }

        .fade-up-1 { animation: fadeUp 0.6s ease forwards; }
        .fade-up-2 { animation: fadeUp 0.6s 0.1s ease both; }
        .fade-up-3 { animation: fadeUp 0.6s 0.2s ease both; }
        .fade-up-4 { animation: fadeUp 0.6s 0.3s ease both; }

        .feature-card {
          background: rgba(255,255,255,0.02);
          border: 1px solid rgba(255,255,255,0.07);
          border-radius: 20px;
          padding: 28px;
          transition: transform 0.3s ease, border-color 0.3s ease, background 0.3s ease;
        }
        .feature-card:hover {
          transform: translateY(-4px);
          border-color: rgba(16,185,129,0.3);
          background: rgba(16,185,129,0.03);
        }

        .cta-btn {
          background: linear-gradient(135deg, #10b981, #059669);
          border: none;
          border-radius: 14px;
          padding: 16px 36px;
          color: white;
          font-size: 16px;
          font-weight: 700;
          font-family: 'Syne', sans-serif;
          cursor: pointer;
          animation: pulse-glow 3s ease infinite;
          transition: transform 0.2s ease, opacity 0.2s ease;
          letter-spacing: 0.3px;
        }
        .cta-btn:hover {
          transform: scale(1.04);
          opacity: 0.92;
        }

        .nav-link {
          color: #64748b;
          font-size: 14px;
          cursor: pointer;
          transition: color 0.2s;
          background: none;
          border: none;
          font-family: 'DM Sans', sans-serif;
        }
        .nav-link:hover { color: #f0f4ff; }

        .grid-bg {
          position: absolute;
          inset: 0;
          background-image:
            linear-gradient(rgba(16,185,129,0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(16,185,129,0.03) 1px, transparent 1px);
          background-size: 60px 60px;
          pointer-events: none;
        }

        .glow-orb {
          position: absolute;
          border-radius: 50%;
          filter: blur(80px);
          pointer-events: none;
        }

        .step-num {
          font-family: 'Syne', sans-serif;
          font-size: 56px;
          font-weight: 800;
          background: linear-gradient(135deg, rgba(16,185,129,0.4), rgba(16,185,129,0.05));
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          line-height: 1;
          margin-bottom: 16px;
        }

        .tag {
          display: inline-flex;
          align-items: center;
          gap: 6px;
          background: rgba(16,185,129,0.1);
          border: 1px solid rgba(16,185,129,0.25);
          border-radius: 99px;
          padding: 6px 14px;
          font-size: 13px;
          color: #10b981;
          font-weight: 600;
          margin-bottom: 24px;
        }

        .hero-title {
          font-family: 'Syne', sans-serif;
          font-size: clamp(42px, 7vw, 80px);
          font-weight: 800;
          line-height: 1.05;
          letter-spacing: -2px;
          margin-bottom: 24px;
        }

        .accent {
          background: linear-gradient(135deg, #10b981, #34d399);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
        }

        .section-label {
          font-size: 12px;
          font-weight: 700;
          letter-spacing: 2px;
          text-transform: uppercase;
          color: #10b981;
          margin-bottom: 12px;
        }

        .section-title {
          font-family: 'Syne', sans-serif;
          font-size: clamp(28px, 4vw, 42px);
          font-weight: 800;
          letter-spacing: -1px;
          color: #f0f4ff;
          margin-bottom: 16px;
        }
      `}</style>

      {/* Nav */}
      <nav style={{
        position: 'fixed', top: 0, left: 0, right: 0, zIndex: 100,
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        padding: '0 40px', height: 64,
        background: 'rgba(10,15,30,0.8)',
        backdropFilter: 'blur(20px)',
        borderBottom: '1px solid rgba(255,255,255,0.05)',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <span style={{ fontSize: 22 }}>🏠</span>
          <span style={{ fontFamily: 'Syne, sans-serif', fontWeight: 800, fontSize: 18, color: '#f0f4ff' }}>
            RoomieQuest
          </span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 24 }}>
          <button className="nav-link" onClick={() => document.getElementById('features').scrollIntoView({ behavior: 'smooth' })}>
            Features
          </button>
          <button className="nav-link" onClick={() => document.getElementById('how-it-works').scrollIntoView({ behavior: 'smooth' })}>
            How it works
          </button>
          <button
            onClick={onGetStarted}
            style={{
              background: 'linear-gradient(135deg, #10b981, #059669)',
              border: 'none', borderRadius: 10, padding: '8px 20px',
              color: 'white', fontSize: 14, fontWeight: 700,
              fontFamily: 'Syne, sans-serif', cursor: 'pointer',
            }}
          >
            Get Started
          </button>
        </div>
      </nav>

      {/* Hero */}
      <section
        ref={heroRef}
        style={{
          position: 'relative', minHeight: '100vh',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          textAlign: 'center', padding: '120px 40px 80px',
          overflow: 'hidden',
        }}
      >
        <div className="grid-bg" />
        <div className="glow-orb" style={{
          width: 600, height: 600,
          background: 'radial-gradient(circle, rgba(16,185,129,0.12), transparent 70%)',
          top: '50%', left: '50%',
          transform: 'translate(-50%, -50%)',
        }} />
        <div className="glow-orb" style={{
          width: 300, height: 300,
          background: 'rgba(99,102,241,0.06)',
          top: '20%', right: '10%',
          animation: 'float 6s ease-in-out infinite',
        }} />
        <div className="glow-orb" style={{
          width: 200, height: 200,
          background: 'rgba(16,185,129,0.08)',
          bottom: '20%', left: '5%',
          animation: 'float 8s ease-in-out infinite reverse',
        }} />

        <div style={{ position: 'relative', maxWidth: 800 }}>
          <div className="fade-up-1 tag">
            <span>⚡</span> Real-time • Free • No BS
          </div>

          <h1 className="hero-title fade-up-2">
            Living together<br />
            <span className="accent">made simple</span>
          </h1>

          <p className="fade-up-3" style={{
            fontSize: 18, color: '#64748b', lineHeight: 1.7,
            maxWidth: 520, margin: '0 auto 40px',
            fontFamily: 'DM Sans, sans-serif',
          }}>
            Shared tasks, shopping lists, and real-time sync for everyone in your home.
            No more group chat chaos.
          </p>

          <div className="fade-up-4" style={{ display: 'flex', gap: 12, justifyContent: 'center', flexWrap: 'wrap' }}>
            <button className="cta-btn" onClick={onGetStarted}>
              Create your room →
            </button>
            <button
              onClick={() => document.getElementById('how-it-works').scrollIntoView({ behavior: 'smooth' })}
              style={{
                background: 'rgba(255,255,255,0.05)',
                border: '1px solid rgba(255,255,255,0.1)',
                borderRadius: 14, padding: '16px 28px',
                color: '#94a3b8', fontSize: 15, fontWeight: 500,
                fontFamily: 'DM Sans, sans-serif', cursor: 'pointer',
                transition: 'color 0.2s, border-color 0.2s',
              }}
              onMouseEnter={e => { e.target.style.color = '#f0f4ff'; e.target.style.borderColor = 'rgba(255,255,255,0.2)'; }}
              onMouseLeave={e => { e.target.style.color = '#94a3b8'; e.target.style.borderColor = 'rgba(255,255,255,0.1)'; }}
            >
              See how it works
            </button>
          </div>

          {/* Social proof */}
          <div style={{
            marginTop: 56, display: 'flex', alignItems: 'center',
            justifyContent: 'center', gap: 24, flexWrap: 'wrap',
          }}>
            {['Free forever', 'Up to 5 roommates', 'Instant sync'].map(label => (
              <div key={label} style={{
                display: 'flex', alignItems: 'center', gap: 7,
                color: '#475569', fontSize: 13,
              }}>
                <span style={{ color: '#10b981', fontSize: 15 }}>✓</span>
                {label}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section id="features" style={{ padding: '100px 40px', maxWidth: 1100, margin: '0 auto' }}>
        <div style={{ textAlign: 'center', marginBottom: 60 }}>
          <p className="section-label">Features</p>
          <h2 className="section-title">Everything your house needs</h2>
          <p style={{ color: '#475569', fontSize: 16, fontFamily: 'DM Sans, sans-serif', lineHeight: 1.7 }}>
            Built for the way roommates actually live — chaotic, busy, and rarely in the same room.
          </p>
        </div>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
          gap: 20,
        }}>
          {features.map((f, i) => (
            <div key={f.title} className="feature-card" style={{ animationDelay: `${i * 0.05}s` }}>
              <div style={{
                width: 44, height: 44, borderRadius: 12, marginBottom: 18,
                background: 'linear-gradient(135deg, #10b981, #059669)',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontSize: 20,
              }}>
                {f.icon}
              </div>
              <h3 style={{
                fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: 17,
                color: '#f0f4ff', marginBottom: 10,
              }}>
                {f.title}
              </h3>
              <p style={{ color: '#475569', fontSize: 14, lineHeight: 1.7, fontFamily: 'DM Sans, sans-serif' }}>
                {f.desc}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* How it works */}
      <section id="how-it-works" style={{
        padding: '100px 40px',
        background: 'rgba(255,255,255,0.01)',
        borderTop: '1px solid rgba(255,255,255,0.05)',
        borderBottom: '1px solid rgba(255,255,255,0.05)',
      }}>
        <div style={{ maxWidth: 1100, margin: '0 auto' }}>
          <div style={{ textAlign: 'center', marginBottom: 70 }}>
            <p className="section-label">How it works</p>
            <h2 className="section-title">Up and running in 60 seconds</h2>
          </div>

          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
            gap: 40,
          }}>
            {steps.map((s, i) => (
              <div key={s.num} style={{ position: 'relative' }}>
                {i < steps.length - 1 && (
                  <div style={{
                    position: 'absolute', top: 28, right: -20,
                    width: 40, height: 1,
                    background: 'linear-gradient(90deg, rgba(16,185,129,0.3), transparent)',
                    display: 'none',
                  }} />
                )}
                <div className="step-num">{s.num}</div>
                <h3 style={{
                  fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: 20,
                  color: '#f0f4ff', marginBottom: 10,
                }}>
                  {s.title}
                </h3>
                <p style={{ color: '#475569', fontSize: 15, lineHeight: 1.7, fontFamily: 'DM Sans, sans-serif' }}>
                  {s.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section style={{
        padding: '120px 40px', textAlign: 'center',
        position: 'relative', overflow: 'hidden',
      }}>
        <div className="glow-orb" style={{
          width: 500, height: 500,
          background: 'radial-gradient(circle, rgba(16,185,129,0.08), transparent 70%)',
          top: '50%', left: '50%',
          transform: 'translate(-50%, -50%)',
        }} />
        <div style={{ position: 'relative', maxWidth: 600, margin: '0 auto' }}>
          <h2 style={{
            fontFamily: 'Syne, sans-serif', fontSize: 'clamp(32px, 5vw, 52px)',
            fontWeight: 800, letterSpacing: '-1.5px', marginBottom: 20, color: '#f0f4ff',
          }}>
            Ready to stop the<br />
            <span className="accent">group chat chaos?</span>
          </h2>
          <p style={{
            color: '#475569', fontSize: 17, lineHeight: 1.7,
            fontFamily: 'DM Sans, sans-serif', marginBottom: 40,
          }}>
            Free to use. Takes 30 seconds to set up.
            Your roommates will actually thank you.
          </p>
          <button className="cta-btn" onClick={onGetStarted} style={{ fontSize: 17, padding: '18px 44px' }}>
            Create your room — it's free →
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer style={{
        borderTop: '1px solid rgba(255,255,255,0.05)',
        padding: '32px 40px',
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        flexWrap: 'wrap', gap: 12,
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <span style={{ fontSize: 18 }}>🏠</span>
          <span style={{ fontFamily: 'Syne, sans-serif', fontWeight: 700, color: '#f0f4ff' }}>RoomieQuest</span>
        </div>
        <p style={{ color: '#334155', fontSize: 13, fontFamily: 'DM Sans, sans-serif' }}>
          Built by Daniel · {new Date().getFullYear()}
        </p>
      </footer>

    </div>
  );
}
