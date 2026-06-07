import { useState, useEffect, useRef } from "react";
import { ArrowRight, Zap, ChevronRight } from "lucide-react";

/* ─── tiny animated grid background ─── */
function GridBg() {
  return (
    <div style={g.grid} aria-hidden>
      <svg width="100%" height="100%" style={{ position: "absolute", inset: 0 }}>
        <defs>
          <pattern id="grid" width="60" height="60" patternUnits="userSpaceOnUse">
            <path d="M 60 0 L 0 0 0 60" fill="none" stroke="rgba(0,212,255,0.045)" strokeWidth="1" />
          </pattern>
          <radialGradient id="vignette" cx="50%" cy="40%" r="60%">
            <stop offset="0%" stopColor="transparent" />
            <stop offset="100%" stopColor="#0D0F12" />
          </radialGradient>
        </defs>
        <rect width="100%" height="100%" fill="url(#grid)" />
        <rect width="100%" height="100%" fill="url(#vignette)" />
      </svg>
      {/* Floating accent orbs */}
      <div style={g.orb1} />
      <div style={g.orb2} />
    </div>
  );
}

const g = {
  grid: { position: "absolute", inset: 0, overflow: "hidden", pointerEvents: "none" },
  orb1: {
    position: "absolute", top: "18%", left: "8%",
    width: 520, height: 520, borderRadius: "50%",
    background: "radial-gradient(circle, rgba(0,212,255,0.07) 0%, transparent 70%)",
    filter: "blur(1px)",
  },
  orb2: {
    position: "absolute", bottom: "10%", right: "6%",
    width: 380, height: 380, borderRadius: "50%",
    background: "radial-gradient(circle, rgba(0,212,255,0.05) 0%, transparent 70%)",
  },
};

/* ─── Stat counter ─── */
function Stat({ value, label, delay = 0 }) {
  return (
    <div style={{ ...s.statBlock, animationDelay: `${delay}ms` }} className="reveal-up">
      <span style={s.statValue}>{value}</span>
      <span style={s.statLabel}>{label}</span>
    </div>
  );
}

/* ─── Product card ─── */
function ProductCard({ icon, name, tagline, range, speed, weight, accent, delay }) {
  const [hovered, setHovered] = useState(false);
  return (
    <div
      style={{
        ...s.productCard,
        borderColor: hovered ? accent : "rgba(255,255,255,0.06)",
        transform: hovered ? "translateY(-6px)" : "translateY(0)",
        boxShadow: hovered ? `0 24px 48px rgba(0,0,0,0.5), 0 0 0 1px ${accent}22` : "0 4px 24px rgba(0,0,0,0.3)",
        animationDelay: `${delay}ms`,
      }}
      className="reveal-up"
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
    >
      <div style={{ ...s.productIcon, background: `${accent}14`, borderColor: `${accent}30` }}>
        <span style={{ fontSize: 32 }}>{icon}</span>
      </div>
      <h3 style={s.productName}>{name}</h3>
      <p style={s.productTagline}>{tagline}</p>
      <div style={s.productSpecs}>
        <div style={s.spec}>
          <span style={s.specLabel}>Range</span>
          <span style={{ ...s.specValue, color: accent }}>{range}</span>
        </div>
        <div style={s.spec}>
          <span style={s.specLabel}>Top Speed</span>
          <span style={{ ...s.specValue, color: accent }}>{speed}</span>
        </div>
        <div style={s.spec}>
          <span style={s.specLabel}>Category</span>
          <span style={{ ...s.specValue, color: accent }}>{weight}</span>
        </div>
      </div>
    </div>
  );
}

/* ─── Feature row ─── */
function Feature({ icon, title, body, delay }) {
  return (
    <div style={{ ...s.featureRow, animationDelay: `${delay}ms` }} className="reveal-up">
      <div style={s.featureIcon}>{icon}</div>
      <div>
        <h4 style={s.featureTitle}>{title}</h4>
        <p style={s.featureBody}>{body}</p>
      </div>
    </div>
  );
}

/* ─── Main component ─── */
export default function LandingPage({ onNavigateToChat }) {
  const [query, setQuery] = useState("");
  const [inputFocused, setInputFocused] = useState(false);
  const [placeholder, setPlaceholder] = useState(0);
  const inputRef = useRef(null);

  const placeholders = [
    "Compare EV-9 truck vs the Titan X range...",
    "What's the battery life on the Glide Pro hoverboard?",
    "Show me the Q2 manufacturing report...",
    "Which bike handles best in monsoon conditions?",
    "Ask DAI anything about Dhaya Electric...",
  ];

  // Cycle placeholder text
  useEffect(() => {
    const t = setInterval(() => setPlaceholder(p => (p + 1) % placeholders.length), 3200);
    return () => clearInterval(t);
  }, []);

  // Scroll reveal
  useEffect(() => {
    const els = document.querySelectorAll(".reveal-up");
    const obs = new IntersectionObserver(
      (entries) => entries.forEach(e => { if (e.isIntersecting) e.target.classList.add("visible"); }),
      { threshold: 0.12 }
    );
    els.forEach(el => obs.observe(el));
    return () => obs.disconnect();
  }, []);

  const handleSubmit = (e) => {
    e?.preventDefault();
    if (query.trim()) onNavigateToChat(query.trim());
  };

  const handleKey = (e) => {
    if (e.key === "Enter") handleSubmit();
  };

  const products = [
    { icon: "⚡", name: "Dhaya Volt", tagline: "Urban commuter e-bicycle with adaptive torque sensing", range: "120 km", speed: "45 km/h", weight: "E-Bicycle", accent: "#00D4FF", delay: 100 },
    { icon: "🛹", name: "Glide Pro X", tagline: "Self-balancing hoverboard for the next generation", range: "35 km", speed: "28 km/h", weight: "Hoverboard", accent: "#A78BFA", delay: 200 },
    { icon: "🚛", name: "EV-9 Titan", tagline: "Heavy-duty electric cargo truck, zero emissions", range: "480 km", speed: "120 km/h", weight: "E-Truck", accent: "#34D399", delay: 300 },
    { icon: "🛵", name: "Sprint S2", tagline: "Electric scooter designed for dense city grids", range: "90 km", speed: "60 km/h", weight: "E-Scooter", accent: "#FB923C", delay: 400 },
    { icon: "🚗", name: "Dhaya Aero", tagline: "Lightweight electric city car with panoramic solar roof", range: "340 km", speed: "160 km/h", weight: "E-Car", accent: "#F472B6", delay: 500 },
    { icon: "🏍️", name: "RapidR Moto", tagline: "Performance electric motorcycle for highways", range: "260 km", speed: "210 km/h", weight: "E-Moto", accent: "#FBBF24", delay: 600 },
  ];

  return (
    <div style={s.page}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&family=JetBrains+Mono:wght@400;500&display=swap');
        * { box-sizing: border-box; margin: 0; padding: 0; }
        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #1E2530; border-radius: 99px; }
        .reveal-up { opacity: 0; transform: translateY(28px); transition: opacity 0.65s ease, transform 0.65s ease; }
        .reveal-up.visible { opacity: 1; transform: translateY(0); }
        @keyframes heroFade { from { opacity:0; transform:translateY(20px); } to { opacity:1; transform:translateY(0); } }
        @keyframes placeholderFade { 0%,90% { opacity:1; } 95%,100% { opacity:0; } }
        @keyframes pulse2 { 0%,100% { box-shadow:0 0 0 0 rgba(0,212,255,0.35); } 50% { box-shadow:0 0 0 8px rgba(0,212,255,0); } }
        @keyframes borderGlow { 0%,100% { box-shadow:0 0 0 1px rgba(0,212,255,0.4), 0 8px 40px rgba(0,0,0,0.6); } 50% { box-shadow:0 0 0 1px rgba(0,212,255,0.7), 0 8px 48px rgba(0,212,255,0.12); } }
        @keyframes marquee { from { transform:translateX(0); } to { transform:translateX(-50%); } }
        @keyframes logoIn { from { opacity:0; transform:translateY(-12px); } to { opacity:1; transform:translateY(0); } }
        .hero-title { animation: heroFade 0.9s ease 0.1s both; }
        .hero-sub { animation: heroFade 0.9s ease 0.28s both; }
        .hero-input { animation: heroFade 0.9s ease 0.45s both; }
        .hero-stats { animation: heroFade 0.9s ease 0.62s both; }
        .nav-in { animation: logoIn 0.6s ease both; }
        textarea:focus { outline: none; }
      `}</style>

      {/* ── NAV ── */}
      <nav style={s.nav} className="nav-in">
        <div style={s.navInner}>
          <div style={s.navLogo}>
            <div style={s.logoMark}>
              <Zap size={15} color="#00D4FF" fill="#00D4FF" />
            </div>
            <span style={s.logoName}>Dhaya Electric</span>
          </div>
          <div style={s.navLinks}>
            {["Vehicles", "Technology", "Sustainability", "About"].map(l => (
              <a key={l} href="#" style={s.navLink} onMouseEnter={e => e.target.style.color = "#00D4FF"} onMouseLeave={e => e.target.style.color = "#8B91A0"}>{l}</a>
            ))}
          </div>
          <button
            style={s.navCta}
            onClick={() => onNavigateToChat("")}
            onMouseEnter={e => { e.target.style.background = "#00D4FF"; e.target.style.color = "#000"; }}
            onMouseLeave={e => { e.target.style.background = "transparent"; e.target.style.color = "#00D4FF"; }}
          >
            Open DAI <ArrowRight size={13} style={{ display: "inline", marginLeft: 4 }} />
          </button>
        </div>
      </nav>

      {/* ── HERO ── */}
      <section style={s.hero}>
        <GridBg />
        <div style={s.heroInner}>
          <div style={s.badge} className="hero-title">
            <span style={s.badgeDot} />
            <span style={s.badgeText}>Now shipping the EV-9 Titan — India's first electric heavy truck</span>
          </div>

          <h1 style={s.heroTitle} className="hero-title">
            Move the world<br />
            <span style={s.heroAccent}>without burning it.</span>
          </h1>

          <p style={s.heroSub} className="hero-sub">
            Dhaya Electric designs zero-emission vehicles for every road — from city sidewalks to national highways. Engineered in India. Built for tomorrow.
          </p>

          {/* ── BIG INPUT BAR ── */}
          <div style={s.heroInputWrap} className="hero-input">
            <div style={{
              ...s.inputOuter,
              borderColor: inputFocused ? "rgba(0,212,255,0.6)" : "rgba(0,212,255,0.18)",
              boxShadow: inputFocused
                ? "0 0 0 4px rgba(0,212,255,0.1), 0 16px 60px rgba(0,0,0,0.6)"
                : "0 8px 40px rgba(0,0,0,0.5)",
              animation: inputFocused ? "borderGlow 2s ease infinite" : "none",
            }}>
              <div style={s.inputIconLeft}>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#00D4FF" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" opacity="0.7">
                  <rect x="3" y="11" width="18" height="11" rx="2" /><path d="M7 11V7a5 5 0 0 1 10 0v4" />
                </svg>
              </div>
              <input
                ref={inputRef}
                type="text"
                value={query}
                onChange={e => setQuery(e.target.value)}
                onKeyDown={handleKey}
                onFocus={() => setInputFocused(true)}
                onBlur={() => setInputFocused(false)}
                placeholder={placeholders[placeholder]}
                style={s.heroInput}
              />
              <button
                style={{
                  ...s.heroSendBtn,
                  background: query.trim() ? "#00D4FF" : "rgba(0,212,255,0.1)",
                  color: query.trim() ? "#000" : "rgba(0,212,255,0.4)",
                  transform: query.trim() ? "scale(1)" : "scale(0.96)",
                  boxShadow: query.trim() ? "0 0 20px rgba(0,212,255,0.4)" : "none",
                }}
                onClick={handleSubmit}
              >
                <span style={{ fontFamily: "'DM Sans', sans-serif", fontWeight: 500, fontSize: 14, marginRight: 6 }}>Ask DAI</span>
                <ArrowRight size={15} />
              </button>
            </div>
            <p style={s.inputHint}>Ask anything about our vehicles, specs, reports, or manufacturing data</p>
          </div>

          {/* ── STATS ── */}
          <div style={s.statsRow} className="hero-stats">
            <Stat value="6+" label="Vehicle Lines" delay={0} />
            <div style={s.statDivider} />
            <Stat value="48K+" label="Units Delivered" delay={100} />
            <div style={s.statDivider} />
            <Stat value="12" label="States Covered" delay={200} />
            <div style={s.statDivider} />
            <Stat value="0" label="Emissions" delay={300} />
          </div>
        </div>
      </section>

      {/* ── MARQUEE STRIP ── */}
      <div style={s.marqueeWrap} aria-hidden>
        <div style={s.marqueeTrack}>
          {[...Array(2)].map((_, gi) => (
            <div key={gi} style={s.marqueeInner}>
              {["E-Bicycle", "Hoverboard", "E-Truck", "E-Scooter", "E-Motorcycle", "Solar Roof Car", "Zero Emissions", "Made in India", "Smart Battery", "DAI Powered"].map((t, i) => (
                <span key={i} style={s.marqueeItem}>
                  <span style={s.marqueeDot}>⚡</span> {t}
                </span>
              ))}
            </div>
          ))}
        </div>
      </div>

      {/* ── PRODUCTS ── */}
      <section style={s.section}>
        <div style={s.sectionInner}>
          <div style={s.sectionLabel} className="reveal-up">Our Fleet</div>
          <h2 style={s.sectionTitle} className="reveal-up">Every vehicle. Every road.</h2>
          <p style={s.sectionSub} className="reveal-up">From the last-mile delivery hoverboard to the long-haul electric truck — Dhaya Electric covers the full spectrum of sustainable mobility.</p>
          <div style={s.productGrid}>
            {products.map((p) => <ProductCard key={p.name} {...p} />)}
          </div>
        </div>
      </section>

      {/* ── DAI FEATURE SECTION ── */}
      <section style={{ ...s.section, background: "#13161B", borderTop: "1px solid #1E2530", borderBottom: "1px solid #1E2530" }}>
        <div style={s.sectionInner}>
          <div style={s.daiFeatureGrid}>
            <div style={s.daiLeft}>
              <div style={s.sectionLabel} className="reveal-up">Meet DAI</div>
              <h2 style={{ ...s.sectionTitle, marginBottom: 16 }} className="reveal-up">Your internal AI, built for Dhaya.</h2>
              <p style={{ ...s.sectionSub, marginBottom: 40 }} className="reveal-up">
                DAI (Dhaya AI) connects every employee to real-time vehicle data, manufacturing reports, and production analytics — in plain language, instantly.
              </p>
              <div style={s.featureList}>
                <Feature icon="🔍" title="Vehicle Intelligence" body="Instant specs, comparisons, and technical data for every model in our fleet." delay={100} />
                <Feature icon="📊" title="Manufacturing Reports" body="Live production metrics, defect rates, cycle times, and shift summaries." delay={200} />
                <Feature icon="🛠️" title="MCP Trace Visibility" body="Every step DAI takes is logged and visible — full transparency into AI reasoning." delay={300} />
                <Feature icon="⚡" title="Real-Time Queries" body="Ask in natural language. Get structured answers with markdown, tables, and code." delay={400} />
              </div>
            </div>
            <div style={s.daiRight} className="reveal-up">
              {/* Mini chat preview */}
              <div style={s.chatPreview}>
                <div style={s.cpHeader}>
                  <div style={s.cpDot} />
                  <span style={s.cpTitle}>DAI — Dhaya AI</span>
                  <span style={s.cpOnline}>● Online</span>
                </div>
                <div style={s.cpBody}>
                  {[
                    { role: "user", text: "What's the range of the EV-9 Titan?" },
                    { role: "ai", text: "The EV-9 Titan delivers **480 km** on a single charge under standard load. With regenerative braking active, real-world range extends to ~510 km." },
                    { role: "user", text: "Compare it to the Sprint S2" },
                    { role: "ai", text: "The Sprint S2 is optimized for urban use with a **90 km** range at 60 km/h top speed. The Titan is a long-haul cargo vehicle. Very different use cases." },
                  ].map((m, i) => (
                    <div key={i} style={{ display: "flex", justifyContent: m.role === "user" ? "flex-end" : "flex-start", marginBottom: 10 }}>
                      <div style={{
                        maxWidth: "82%", padding: "9px 13px", fontSize: 12, lineHeight: 1.6, borderRadius: m.role === "user" ? "14px 14px 3px 14px" : "14px 14px 14px 3px",
                        background: m.role === "user" ? "#00D4FF" : "#1C2028",
                        color: m.role === "user" ? "#000" : "#E8EAF0",
                        border: m.role === "ai" ? "1px solid #1E2530" : "none",
                        fontFamily: "'DM Sans', sans-serif",
                      }}
                        dangerouslySetInnerHTML={{ __html: m.text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') }}
                      />
                    </div>
                  ))}
                </div>
                <button
                  style={s.cpCta}
                  onClick={() => onNavigateToChat("")}
                  onMouseEnter={e => e.currentTarget.style.background = "#00D4FF22"}
                  onMouseLeave={e => e.currentTarget.style.background = "transparent"}
                >
                  Open full DAI interface <ChevronRight size={13} style={{ display: "inline", marginLeft: 4 }} />
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── SUSTAINABILITY ── */}
      <section style={s.section}>
        <div style={s.sectionInner}>
          <div style={s.sectionLabel} className="reveal-up">Sustainability</div>
          <h2 style={s.sectionTitle} className="reveal-up">Numbers that matter.</h2>
          <div style={s.sustainGrid}>
            {[
              { val: "184K", unit: "tonnes", label: "CO₂ avoided in 2024", color: "#34D399" },
              { val: "100%", unit: "", label: "Renewable factory energy", color: "#00D4FF" },
              { val: "92%", unit: "", label: "Recyclable battery components", color: "#A78BFA" },
              { val: "₹0", unit: "", label: "Fuel cost for our customers", color: "#FBBF24" },
            ].map((item, i) => (
              <div key={i} style={{ ...s.sustainCard, animationDelay: `${i * 100}ms`, borderColor: `${item.color}22` }} className="reveal-up">
                <span style={{ ...s.sustainVal, color: item.color }}>{item.val}<span style={s.sustainUnit}>{item.unit}</span></span>
                <span style={s.sustainLabel}>{item.label}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── FOOTER CTA ── */}
      <section style={s.footerCta}>
        <GridBg />
        <div style={{ position: "relative", zIndex: 1, textAlign: "center", maxWidth: 620, margin: "0 auto", padding: "0 24px" }}>
          <h2 style={{ ...s.heroTitle, fontSize: "clamp(28px, 4vw, 48px)", marginBottom: 16 }} className="reveal-up">
            Ready to talk to <span style={s.heroAccent}>DAI?</span>
          </h2>
          <p style={{ ...s.heroSub, marginBottom: 36 }} className="reveal-up">
            Your internal AI assistant is live. Ask about any vehicle, report, or manufacturing metric.
          </p>
          <button
            style={s.bigCta}
            onClick={() => onNavigateToChat("")}
            className="reveal-up"
            onMouseEnter={e => { e.currentTarget.style.transform = "translateY(-3px)"; e.currentTarget.style.boxShadow = "0 12px 40px rgba(0,212,255,0.4)"; }}
            onMouseLeave={e => { e.currentTarget.style.transform = "translateY(0)"; e.currentTarget.style.boxShadow = "0 4px 24px rgba(0,212,255,0.25)"; }}
          >
            <Zap size={17} fill="#000" /> &nbsp; Launch DAI
          </button>
        </div>
      </section>

      {/* ── FOOTER ── */}
      <footer style={s.footer}>
        <div style={s.footerInner}>
          <div style={s.footerLogo}>
            <div style={s.logoMark}>
              <Zap size={13} color="#00D4FF" fill="#00D4FF" />
            </div>
            <span style={{ ...s.logoName, fontSize: 14 }}>Dhaya Electric</span>
          </div>
          <p style={s.footerCopy}>© 2026 Dhaya Electric Pvt. Ltd. · Made in India · Zero Emissions</p>
          <div style={s.footerLinks}>
            {["Privacy", "Terms", "Careers", "Contact"].map(l => (
              <a key={l} href="#" style={s.footerLink}>{l}</a>
            ))}
          </div>
        </div>
      </footer>
    </div>
  );
}

/* ─── STYLES ─── */
const s = {
  page: { minHeight: "100vh", background: "#0D0F12", fontFamily: "'DM Sans', sans-serif", color: "#E8EAF0", overflowX: "hidden" },

  /* Nav */
  nav: { position: "fixed", top: 0, left: 0, right: 0, zIndex: 100, background: "rgba(13,15,18,0.85)", backdropFilter: "blur(16px)", borderBottom: "1px solid rgba(255,255,255,0.05)" },
  navInner: { maxWidth: 1200, margin: "0 auto", padding: "0 32px", height: 64, display: "flex", alignItems: "center", justifyContent: "space-between" },
  navLogo: { display: "flex", alignItems: "center", gap: 10 },
  logoMark: { width: 30, height: 30, borderRadius: 8, background: "#0A3D4D", border: "1px solid rgba(0,212,255,0.3)", display: "flex", alignItems: "center", justifyContent: "center" },
  logoName: { fontFamily: "'Syne', sans-serif", fontWeight: 700, fontSize: 16, letterSpacing: "0.02em" },
  navLinks: { display: "flex", gap: 32 },
  navLink: { color: "#8B91A0", textDecoration: "none", fontSize: 14, fontWeight: 400, transition: "color 0.2s" },
  navCta: { padding: "8px 18px", borderRadius: 8, border: "1px solid rgba(0,212,255,0.4)", background: "transparent", color: "#00D4FF", fontFamily: "'DM Sans', sans-serif", fontSize: 13, fontWeight: 500, cursor: "pointer", transition: "all 0.2s", display: "flex", alignItems: "center", gap: 4 },

  /* Hero */
  hero: { position: "relative", minHeight: "100vh", display: "flex", alignItems: "center", paddingTop: 64 },
  heroInner: { position: "relative", zIndex: 1, maxWidth: 860, margin: "0 auto", padding: "80px 32px 100px", textAlign: "center" },
  badge: { display: "inline-flex", alignItems: "center", gap: 8, padding: "6px 14px", borderRadius: 99, border: "1px solid rgba(0,212,255,0.2)", background: "rgba(0,212,255,0.05)", marginBottom: 32 },
  badgeDot: { width: 6, height: 6, borderRadius: "50%", background: "#00D4FF", display: "inline-block", animation: "pulse2 2s infinite" },
  badgeText: { fontSize: 12, color: "#8B91A0", fontFamily: "'JetBrains Mono', monospace" },
  heroTitle: { fontFamily: "'Syne', sans-serif", fontWeight: 800, fontSize: "clamp(38px, 6vw, 72px)", lineHeight: 1.08, letterSpacing: "-0.03em", marginBottom: 22, color: "#E8EAF0" },
  heroAccent: { color: "#00D4FF" },
  heroSub: { fontSize: 17, color: "#8B91A0", lineHeight: 1.7, maxWidth: 560, margin: "0 auto 44px", fontWeight: 300 },

  /* Input bar */
  heroInputWrap: { marginBottom: 52 },
  inputOuter: { display: "flex", alignItems: "center", gap: 12, background: "#13161B", border: "1px solid", borderRadius: 16, padding: "10px 10px 10px 20px", maxWidth: 720, margin: "0 auto", transition: "border-color 0.25s, box-shadow 0.35s" },
  inputIconLeft: { flexShrink: 0 },
  heroInput: { flex: 1, background: "transparent", border: "none", outline: "none", color: "#E8EAF0", fontSize: 16, fontFamily: "'DM Sans', sans-serif", lineHeight: 1.5, padding: "4px 0" },
  heroSendBtn: { display: "flex", alignItems: "center", padding: "10px 18px", borderRadius: 10, border: "none", cursor: "pointer", fontFamily: "'DM Sans', sans-serif", fontWeight: 600, fontSize: 14, transition: "all 0.22s", flexShrink: 0, whiteSpace: "nowrap" },
  inputHint: { fontSize: 12, color: "#4A5060", marginTop: 12, fontFamily: "'JetBrains Mono', monospace" },

  /* Stats */
  statsRow: { display: "flex", alignItems: "center", justifyContent: "center", gap: 0 },
  statBlock: { display: "flex", flexDirection: "column", gap: 3, padding: "0 28px" },
  statValue: { fontFamily: "'Syne', sans-serif", fontWeight: 700, fontSize: 28, color: "#E8EAF0", letterSpacing: "-0.02em" },
  statLabel: { fontSize: 12, color: "#4A5060", fontFamily: "'JetBrains Mono', monospace", letterSpacing: "0.04em" },
  statDivider: { width: 1, height: 36, background: "#1E2530" },

  /* Marquee */
  marqueeWrap: { overflow: "hidden", borderTop: "1px solid #1E2530", borderBottom: "1px solid #1E2530", background: "#13161B", padding: "14px 0" },
  marqueeTrack: { display: "flex", animation: "marquee 28s linear infinite" },
  marqueeInner: { display: "flex", alignItems: "center", gap: 0, flexShrink: 0 },
  marqueeItem: { display: "inline-flex", alignItems: "center", gap: 6, padding: "0 28px", fontSize: 12, color: "#8B91A0", fontFamily: "'JetBrains Mono', monospace", letterSpacing: "0.06em", whiteSpace: "nowrap" },
  marqueeDot: { color: "#00D4FF", fontSize: 10 },

  /* Sections */
  section: { padding: "100px 32px" },
  sectionInner: { maxWidth: 1200, margin: "0 auto" },
  sectionLabel: { fontFamily: "'JetBrains Mono', monospace", fontSize: 11, color: "#00D4FF", letterSpacing: "0.14em", textTransform: "uppercase", marginBottom: 14 },
  sectionTitle: { fontFamily: "'Syne', sans-serif", fontWeight: 700, fontSize: "clamp(26px, 4vw, 42px)", lineHeight: 1.15, letterSpacing: "-0.02em", marginBottom: 16, color: "#E8EAF0" },
  sectionSub: { fontSize: 16, color: "#8B91A0", lineHeight: 1.7, maxWidth: 580, marginBottom: 56, fontWeight: 300 },

  /* Products */
  productGrid: { display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))", gap: 20 },
  productCard: { background: "#13161B", border: "1px solid", borderRadius: 16, padding: "28px 24px", transition: "all 0.3s ease", cursor: "default" },
  productIcon: { width: 56, height: 56, borderRadius: 14, border: "1px solid", display: "flex", alignItems: "center", justifyContent: "center", marginBottom: 18 },
  productName: { fontFamily: "'Syne', sans-serif", fontWeight: 700, fontSize: 18, marginBottom: 8, color: "#E8EAF0" },
  productTagline: { fontSize: 13, color: "#8B91A0", lineHeight: 1.6, marginBottom: 22, fontWeight: 300 },
  productSpecs: { display: "flex", flexDirection: "column", gap: 8, borderTop: "1px solid #1E2530", paddingTop: 18 },
  spec: { display: "flex", justifyContent: "space-between", alignItems: "center" },
  specLabel: { fontSize: 12, color: "#4A5060", fontFamily: "'JetBrains Mono', monospace" },
  specValue: { fontSize: 13, fontFamily: "'JetBrains Mono', monospace", fontWeight: 500 },

  /* DAI section */
  daiFeatureGrid: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 72, alignItems: "center" },
  daiLeft: {},
  daiRight: {},
  featureList: { display: "flex", flexDirection: "column", gap: 24 },
  featureRow: { display: "flex", gap: 16, alignItems: "flex-start" },
  featureIcon: { fontSize: 22, flexShrink: 0, marginTop: 2 },
  featureTitle: { fontFamily: "'Syne', sans-serif", fontWeight: 600, fontSize: 15, marginBottom: 4, color: "#E8EAF0" },
  featureBody: { fontSize: 13, color: "#8B91A0", lineHeight: 1.65, fontWeight: 300 },

  /* Chat preview */
  chatPreview: { background: "#0D0F12", border: "1px solid #1E2530", borderRadius: 16, overflow: "hidden" },
  cpHeader: { display: "flex", alignItems: "center", gap: 8, padding: "14px 18px", borderBottom: "1px solid #1E2530", background: "#13161B" },
  cpDot: { width: 8, height: 8, borderRadius: "50%", background: "#22C55E" },
  cpTitle: { fontFamily: "'Syne', sans-serif", fontSize: 13, fontWeight: 600, flex: 1 },
  cpOnline: { fontSize: 11, color: "#22C55E", fontFamily: "'JetBrains Mono', monospace" },
  cpBody: { padding: "20px 18px" },
  cpCta: { width: "100%", padding: "12px 18px", background: "transparent", border: "none", borderTop: "1px solid #1E2530", color: "#00D4FF", fontFamily: "'DM Sans', sans-serif", fontSize: 13, fontWeight: 500, cursor: "pointer", transition: "background 0.2s", textAlign: "left" },

  /* Sustainability */
  sustainGrid: { display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 20 },
  sustainCard: { background: "#13161B", border: "1px solid", borderRadius: 14, padding: "28px 22px", display: "flex", flexDirection: "column", gap: 10 },
  sustainVal: { fontFamily: "'Syne', sans-serif", fontWeight: 800, fontSize: 38, letterSpacing: "-0.02em", lineHeight: 1 },
  sustainUnit: { fontSize: 18, fontWeight: 600, marginLeft: 3 },
  sustainLabel: { fontSize: 13, color: "#8B91A0", lineHeight: 1.5, fontWeight: 300 },

  /* Footer CTA */
  footerCta: { position: "relative", padding: "120px 32px", borderTop: "1px solid #1E2530", overflow: "hidden" },
  bigCta: { display: "inline-flex", alignItems: "center", padding: "14px 36px", background: "#00D4FF", color: "#000", fontFamily: "'Syne', sans-serif", fontWeight: 700, fontSize: 16, border: "none", borderRadius: 12, cursor: "pointer", boxShadow: "0 4px 24px rgba(0,212,255,0.25)", transition: "all 0.25s", letterSpacing: "0.01em" },

  /* Footer */
  footer: { borderTop: "1px solid #1E2530", padding: "28px 32px" },
  footerInner: { maxWidth: 1200, margin: "0 auto", display: "flex", alignItems: "center", justifyContent: "space-between", flexWrap: "wrap", gap: 16 },
  footerLogo: { display: "flex", alignItems: "center", gap: 8 },
  footerCopy: { fontSize: 12, color: "#4A5060", fontFamily: "'JetBrains Mono', monospace" },
  footerLinks: { display: "flex", gap: 20 },
  footerLink: { fontSize: 12, color: "#8B91A0", textDecoration: "none", fontFamily: "'JetBrains Mono', monospace" },
};
