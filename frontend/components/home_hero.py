import streamlit as st


_HOME_HERO = st.components.v2.component(
    "matallana_luxury_home_hero",
    html="""
<section class="mvip-hero" aria-labelledby="mvip-hero-title">
  <div class="mvip-glow mvip-glow-one" aria-hidden="true"></div>
  <div class="mvip-glow mvip-glow-two" aria-hidden="true"></div>
  <svg class="mvip-back-gem" viewBox="0 0 520 520" aria-hidden="true">
    <defs>
      <linearGradient id="back-gem-fill" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" stop-color="#50C878"/>
        <stop offset=".48" stop-color="#0B8A42"/>
        <stop offset="1" stop-color="#046307"/>
      </linearGradient>
    </defs>
    <polygon points="260,22 420,82 498,240 420,420 260,498 100,420 22,240 100,82" fill="url(#back-gem-fill)"/>
    <path d="M260 22 260 498M100 82 420 420M420 82 100 420M22 240H498M100 82 260 150 420 82M22 240 180 260 100 420M498 240 340 260 420 420M180 260 260 150 340 260 260 498Z" fill="none" stroke="#B8F4CB" stroke-width="2"/>
  </svg>
  <div class="mvip-particles" aria-hidden="true">
    <span class="particle particle-gold"></span><span class="particle particle-green"></span>
    <span class="particle particle-green"></span><span class="particle particle-gold"></span>
    <span class="particle particle-gold"></span><span class="particle particle-green"></span>
    <span class="particle particle-green"></span><span class="particle particle-gold"></span>
    <span class="particle particle-green"></span><span class="particle particle-gold"></span>
    <span class="particle particle-green"></span><span class="particle particle-gold"></span>
  </div>
  <div class="mvip-hero-inner">
    <div class="mvip-copy">
      <p class="mvip-eyebrow"><span class="eyebrow-rule"></span>Joyería Matallana VIP · Bogotá desde 1998<span class="eyebrow-rule"></span></p>
      <h1 class="mvip-title" id="mvip-hero-title"><span>ESMERALDAS</span><span>COLOMBIANAS</span></h1>
      <p class="mvip-subtitle">Que cuentan historias</p>
      <div class="mvip-title-rule" aria-hidden="true"><span></span></div>
      <p class="mvip-description">La esencia de Boyacá, engastada para perdurar.</p>
      <div class="mvip-actions">
        <button class="mvip-button mvip-button-primary" type="button" data-action="catalog" aria-label="Explorar la colección de joyas">
          Explorar colección <span aria-hidden="true">↗</span>
        </button>
        <button class="mvip-button mvip-button-secondary" type="button" data-action="design">
          Diseñar una joya <span aria-hidden="true">↗</span>
        </button>
      </div>
      <p class="mvip-signature">ESMERALDAS DE BOYACÁ <span>·</span> ORO 18K <span>·</span> PLATA 925</p>
    </div>
    <div class="mvip-stage" aria-label="Anillo de oro blanco con esmeralda octagonal">
      <div class="mvip-orbit mvip-orbit-one" aria-hidden="true"></div>
      <div class="mvip-orbit mvip-orbit-two" aria-hidden="true"></div>
      <div class="mvip-ring-float">
        <div class="mvip-ring-parallax">
          <div class="mvip-ring-visual">
            <img class="mvip-ring-photo" src="/app/static/ring-emerald-luxury.webp" alt="Anillo de oro blanco con esmeralda colombiana corte esmeralda" width="1254" height="1254" fetchpriority="high" decoding="async">
            <span class="mvip-diamond-flare" aria-hidden="true"></span>
          </div>
        </div>
      </div>
      <div class="mvip-art-caption"><span class="caption-dot"></span>Una gema. Un origen. Una historia.</div>
    </div>
  </div>
  <div class="mvip-scroll" aria-hidden="true"><span></span>DESCUBRIR</div>
</section>
""",
    css="""
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500;600&family=Montserrat:wght@300;400;500;600&display=swap');
:host { display: block; width: 100%; }
.mvip-hero, .mvip-hero * { box-sizing: border-box; }
.mvip-hero {
  --forest: #07120D;
  --deep-green: #0B1D16;
  --emerald: #1B4332;
  --bright-emerald: #2D6A4F;
  --mint: #40916C;
  --gold: #D4AF37;
  --ivory: #F5E6C8;
  position: relative;
  isolation: isolate;
  display: grid;
  align-items: center;
  width: 100%;
  min-height: min(760px, calc(100svh - 92px));
  overflow: hidden;
  padding: clamp(42px, 6vw, 88px) clamp(24px, 7vw, 112px);
  color: var(--ivory);
  background:
    radial-gradient(ellipse at 76% 45%, rgba(45,106,79,.42), transparent 43%),
    radial-gradient(ellipse at 12% 10%, rgba(64,145,108,.18), transparent 40%),
    linear-gradient(118deg, var(--forest) 0%, var(--deep-green) 44%, #10291F 72%, #07120D 100%);
  font-family: 'Montserrat', Arial, sans-serif;
}
.mvip-hero::before, .mvip-hero::after {
  position: absolute;
  z-index: -1;
  content: "";
  pointer-events: none;
}
.mvip-hero::before {
  inset: 18px;
  border: 1px solid rgba(212,175,55,.16);
  background: linear-gradient(130deg, rgba(255,255,255,.025), transparent 36%, rgba(212,175,55,.025));
  backdrop-filter: blur(1px);
}
.mvip-hero::after {
  width: 50%;
  height: 1px;
  right: 0;
  top: 17%;
  background: linear-gradient(90deg, transparent, rgba(212,175,55,.35), transparent);
}
.mvip-glow { position: absolute; z-index: -2; border-radius: 50%; pointer-events: none; filter: blur(2px); }
.mvip-glow-one { width: 440px; height: 440px; top: 12%; right: 17%; background: radial-gradient(circle, rgba(64,145,108,.24), transparent 68%); }
.mvip-glow-two { width: 320px; height: 320px; bottom: -24%; left: 18%; background: radial-gradient(circle, rgba(212,175,55,.08), transparent 70%); }
.mvip-back-gem {
  position: absolute;
  z-index: -1;
  width: clamp(380px, 54vw, 720px);
  right: 1%;
  top: 48%;
  opacity: .075;
  filter: drop-shadow(0 0 40px rgba(80,200,120,.72));
  transform: translateY(-50%) rotate(-12deg);
  pointer-events: none;
}
.mvip-hero-inner {
  position: relative;
  display: grid;
  grid-template-columns: minmax(0, .96fr) minmax(380px, 1.04fr);
  align-items: center;
  gap: clamp(20px, 4vw, 64px);
  width: min(100%, 1380px);
  margin: 0 auto;
}
.mvip-copy { position: relative; z-index: 2; animation: mvip-enter .9s cubic-bezier(.2,.8,.2,1) both; }
.mvip-eyebrow { display: flex; align-items: center; gap: 12px; margin: 0 0 30px; color: rgba(245,230,200,.72); font-size: .62rem; font-weight: 400; letter-spacing: .24em; line-height: 1.8; text-transform: uppercase; }
.eyebrow-rule { width: 24px; height: 1px; flex: 0 0 24px; background: linear-gradient(90deg, transparent, var(--gold)); }
.eyebrow-rule:last-child { transform: rotate(180deg); }
.mvip-title { display: flex; flex-direction: column; margin: 0; color: #F8F3E9; font-family: 'Cormorant Garamond', Georgia, serif; font-size: clamp(3.2rem, 6.1vw, 6.35rem); font-weight: 300; letter-spacing: .045em; line-height: .91; }
.mvip-title span:last-child { color: #EAD9B8; }
.mvip-subtitle { margin: 22px 0 0; color: #D9C497; font-family: 'Cormorant Garamond', Georgia, serif; font-size: clamp(1.7rem, 2.8vw, 2.65rem); font-style: italic; font-weight: 300; letter-spacing: .025em; }
.mvip-title-rule { display: flex; align-items: center; width: 138px; height: 1px; margin: 24px 0 20px; background: linear-gradient(90deg, var(--gold), rgba(212,175,55,.08)); }
.mvip-title-rule span { width: 5px; height: 5px; border: 1px solid var(--gold); transform: rotate(45deg); }
.mvip-description { margin: 0; color: rgba(245,230,200,.68); font-size: .75rem; font-weight: 300; letter-spacing: .08em; line-height: 1.9; }
.mvip-actions { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 32px; }
.mvip-button { position: relative; display: inline-flex; align-items: center; justify-content: center; gap: 16px; min-height: 50px; padding: 0 22px; overflow: hidden; border: 1px solid rgba(212,175,55,.56); border-radius: 0; color: var(--ivory); background: rgba(255,255,255,.035); font: 500 .62rem 'Montserrat', Arial, sans-serif; letter-spacing: .14em; text-transform: uppercase; cursor: pointer; transition: transform .4s ease, box-shadow .4s ease, background .4s ease, border-color .4s ease; }
.mvip-button::before { position: absolute; inset: 0; content: ""; background: linear-gradient(110deg, transparent 20%, rgba(255,255,255,.24) 48%, transparent 72%); transform: translateX(-120%); transition: transform .75s ease; }
.mvip-button span, .mvip-button { isolation: isolate; }
.mvip-button span { color: var(--gold); font-size: .95rem; }
.mvip-button:hover { z-index: 1; transform: translateY(-3px); border-color: #F1D981; box-shadow: 0 10px 28px rgba(0,0,0,.24), 0 0 22px rgba(212,175,55,.13); }
.mvip-button:hover::before { transform: translateX(120%); }
.mvip-button-primary { border-color: var(--gold); color: #10180F; background: linear-gradient(115deg, #B89538, #E5CB75 48%, #C3A34A); }
.mvip-button-primary span { color: #102017; }
.mvip-button-primary:hover { background: linear-gradient(115deg, #D4AF37, #F5E6A8 48%, #D4AF37); }
.mvip-button-secondary:hover { color: #FFF8E8; background: rgba(212,175,55,.11); }
.mvip-button:focus-visible { outline: 2px solid #F5E6C8; outline-offset: 4px; }
.mvip-signature { margin: 29px 0 0; color: rgba(245,230,200,.48); font-size: .53rem; font-weight: 400; letter-spacing: .2em; }
.mvip-signature span { padding: 0 7px; color: var(--gold); }
.mvip-stage { position: relative; display: grid; min-height: 530px; place-items: center; perspective: 1100px; }
.mvip-orbit { position: absolute; width: min(95%, 520px); aspect-ratio: 1; border: 1px solid rgba(245,230,200,.075); border-radius: 50%; transform: rotateX(68deg) rotate(-12deg); }
.mvip-orbit-two { width: min(76%, 420px); border-color: rgba(212,175,55,.1); transform: rotateX(68deg) rotate(34deg); }
.mvip-ring-float { position: relative; display: grid; width: min(100%, 530px); place-items: center; animation: mvip-float 5s ease-in-out infinite; }
.mvip-ring-parallax { width: 100%; transform: translate3d(var(--parallax-x, 0px), var(--parallax-y, 0px), 0) rotate(-8deg); transition: transform .25s ease-out; }
.mvip-ring-visual { position: relative; width: 100%; filter: drop-shadow(0 28px 30px rgba(0,0,0,.38)); }
.mvip-ring-photo { display: block; width: 100%; height: auto; object-fit: contain; overflow: visible; filter: contrast(1.03) saturate(1.08) drop-shadow(0 28px 24px rgba(0,0,0,.34)); }
.mvip-ring-visual::before { position: absolute; z-index: 2; inset: 5% 8%; content: ""; background: linear-gradient(112deg, transparent 34%, rgba(255,255,255,.72) 49%, rgba(255,255,255,.08) 54%, transparent 68%); opacity: 0; transform: translateX(-78%) rotate(9deg); pointer-events: none; }
.mvip-ring-visual:hover::before { animation: mvip-diamond-sweep 1s ease-in-out; }
.mvip-ring-visual::after { position: absolute; z-index: 3; top: 17%; left: 49%; width: 3px; height: 3px; content: ""; background: #FFF8E8; box-shadow: 0 0 12px 4px rgba(245,230,200,.78); opacity: 0; transform: scale(.2); pointer-events: none; }
.mvip-ring-visual:hover::after { animation: mvip-sparkle .8s ease-out .12s; }
.mvip-ring-photo { transition: filter .4s ease, transform .4s ease; }
.mvip-ring-visual:hover .mvip-ring-photo { transform: scale(1.015); filter: contrast(1.06) saturate(1.12) drop-shadow(0 28px 24px rgba(0,0,0,.34)) drop-shadow(0 0 18px rgba(80,200,120,.26)); }
.mvip-hero.is-flashing .mvip-ring-visual::before { animation: mvip-diamond-sweep 1.15s ease-in-out; }
.mvip-hero.is-flashing .mvip-ring-visual::after { animation: mvip-sparkle 1s ease-out; }
.mvip-hero.is-flashing .mvip-ring-photo { animation: mvip-photo-flash 1.2s ease-out; }
.mvip-art-caption { position: absolute; right: 2%; bottom: 3%; display: flex; align-items: center; gap: 10px; padding: 11px 15px; border: 1px solid rgba(245,230,200,.12); color: rgba(245,230,200,.72); background: rgba(7,18,13,.4); backdrop-filter: blur(12px); font-family: 'Cormorant Garamond', Georgia, serif; font-size: 1.05rem; font-style: italic; letter-spacing: .025em; }
.caption-dot { width: 5px; height: 5px; border-radius: 50%; background: var(--gold); box-shadow: 0 0 9px rgba(212,175,55,.72); }
.mvip-scroll { position: absolute; bottom: 28px; left: 50%; display: flex; align-items: center; gap: 10px; color: rgba(245,230,200,.45); font-size: .5rem; letter-spacing: .25em; transform: translateX(-50%); }
.mvip-scroll span { display: block; width: 34px; height: 1px; background: linear-gradient(90deg, var(--gold), transparent); }
.mvip-particles { position: absolute; inset: 0; overflow: hidden; pointer-events: none; }
.particle { position: absolute; width: 3px; height: 3px; border-radius: 50%; opacity: .35; animation: mvip-particle-drift 8s ease-in-out infinite; }
.particle-gold { background: #D4AF37; box-shadow: 0 0 9px rgba(212,175,55,.56); }
.particle-green { background: #50C878; box-shadow: 0 0 10px rgba(80,200,120,.64); }
.particle:nth-child(1) { top: 19%; left: 9%; animation-delay: -1s; }
.particle:nth-child(2) { top: 72%; left: 7%; animation-delay: -5s; }
.particle:nth-child(3) { top: 34%; left: 44%; animation-delay: -2s; }
.particle:nth-child(4) { top: 81%; left: 32%; animation-delay: -6s; }
.particle:nth-child(5) { top: 12%; left: 67%; animation-delay: -3s; }
.particle:nth-child(6) { top: 23%; right: 9%; animation-delay: -7s; }
.particle:nth-child(7) { top: 66%; right: 8%; animation-delay: -4s; }
.particle:nth-child(8) { top: 88%; right: 24%; animation-delay: -2.5s; }
.particle:nth-child(9) { top: 49%; left: 3%; animation-delay: -5.5s; }
.particle:nth-child(10) { top: 8%; right: 37%; animation-delay: -1.5s; }
.particle:nth-child(11) { top: 54%; right: 4%; animation-delay: -6.5s; }
.particle:nth-child(12) { top: 91%; left: 53%; animation-delay: -3.5s; }
@keyframes mvip-float { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-15px); } }
@keyframes mvip-enter { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
@keyframes mvip-diamond-sweep { 0% { opacity: 0; transform: translateX(-78%) rotate(9deg); } 28% { opacity: .8; } 100% { opacity: 0; transform: translateX(78%) rotate(9deg); } }
@keyframes mvip-sparkle { 0% { opacity: 0; transform: scale(.2); } 45% { opacity: 1; transform: scale(1.2); } 100% { opacity: 0; transform: scale(.2); } }
@keyframes mvip-gem-flash { 0%,100% { filter: drop-shadow(0 0 0 rgba(80,200,120,0)); } 42% { filter: drop-shadow(0 0 22px rgba(80,200,120,.95)) brightness(1.2); } }
@keyframes mvip-photo-flash { 0%,100% { filter: contrast(1.03) saturate(1.08) drop-shadow(0 28px 24px rgba(0,0,0,.34)); } 42% { filter: contrast(1.09) saturate(1.2) brightness(1.08) drop-shadow(0 28px 24px rgba(0,0,0,.34)) drop-shadow(0 0 24px rgba(82,183,136,.5)); } }
@keyframes mvip-particle-drift { 0%,100% { transform: translate3d(0,0,0); opacity: .18; } 50% { transform: translate3d(8px,-16px,0); opacity: .62; } }
@media (max-width: 900px) {
  .mvip-hero { min-height: 690px; padding-inline: clamp(24px,5vw,56px); }
  .mvip-hero-inner { grid-template-columns: minmax(0,1fr) minmax(300px,.9fr); gap: 8px; }
  .mvip-title { font-size: clamp(3.2rem,7vw,5.2rem); }
  .mvip-stage { min-height: 420px; }
}
@media (max-width: 680px) {
  .mvip-hero { min-height: 850px; padding: 52px 25px 64px; }
  .mvip-hero::before { inset: 10px; }
  .mvip-hero-inner { grid-template-columns: 1fr; gap: 0; align-content: start; text-align: center; }
  .mvip-copy { display: flex; flex-direction: column; align-items: center; padding-top: 12px; }
  .mvip-eyebrow { justify-content: center; gap: 8px; margin-bottom: 23px; font-size: .52rem; letter-spacing: .14em; }
  .eyebrow-rule { width: 14px; flex-basis: 14px; }
  .mvip-title { font-size: clamp(3.05rem,12vw,4.7rem); line-height: .92; }
  .mvip-subtitle { margin-top: 17px; font-size: 1.85rem; }
  .mvip-title-rule { margin: 18px auto 15px; }
  .mvip-description { max-width: 290px; font-size: .68rem; }
  .mvip-actions { justify-content: center; gap: 9px; margin-top: 23px; }
  .mvip-button { min-height: 46px; gap: 9px; padding: 0 13px; font-size: .52rem; letter-spacing: .09em; }
  .mvip-signature { margin-top: 21px; font-size: .44rem; letter-spacing: .13em; }
  .mvip-signature span { padding: 0 3px; }
  .mvip-stage { min-height: 365px; margin-top: -1px; }
  .mvip-ring-float { width: min(100%, 400px); }
  .mvip-back-gem { width: 460px; max-width: none; right: -52%; top: 56%; }
  .mvip-glow-one { width: 290px; height: 290px; top: 43%; right: 4%; }
  .mvip-art-caption { right: 0; bottom: 0; padding: 8px 11px; font-size: .92rem; }
  .mvip-scroll { bottom: 18px; }
}
@media (prefers-reduced-motion: reduce) {
  .mvip-copy, .mvip-ring-float, .particle { animation: none !important; }
  .mvip-ring-parallax, .mvip-button { transition: none !important; }
  .mvip-ring-visual:hover::before, .mvip-ring-visual:hover::after { animation: none !important; }
}
""",
    js="""
export default function (component) {
  const { parentElement, setTriggerValue } = component
  const host = parentElement
  const cleanupKey = "__matallanaHeroCleanup"
  if (typeof host[cleanupKey] === "function") host[cleanupKey]()

  const hero = host.querySelector(".mvip-hero")
  if (!hero) return

  const cleanups = []
  hero.querySelectorAll("[data-action]").forEach((button) => {
    const handler = () => setTriggerValue(button.dataset.action, true)
    button.addEventListener("click", handler)
    cleanups.push(() => button.removeEventListener("click", handler))
  })

  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches
  const ring = hero.querySelector(".mvip-ring-parallax")
  let frame = 0
  let flashTimer = 0
  let flashResetTimer = 0

  if (!reducedMotion) {
    const onPointerMove = (event) => {
      if (event.pointerType !== "mouse" || frame) return
      frame = window.requestAnimationFrame(() => {
        const bounds = hero.getBoundingClientRect()
        const x = ((event.clientX - bounds.left) / bounds.width - .5) * 13
        const y = ((event.clientY - bounds.top) / bounds.height - .5) * 13
        ring.style.setProperty("--parallax-x", `${x.toFixed(1)}px`)
        ring.style.setProperty("--parallax-y", `${y.toFixed(1)}px`)
        frame = 0
      })
    }
    const onPointerLeave = () => {
      ring.style.setProperty("--parallax-x", "0px")
      ring.style.setProperty("--parallax-y", "0px")
    }
    hero.addEventListener("pointermove", onPointerMove, { passive: true })
    hero.addEventListener("pointerleave", onPointerLeave)
    cleanups.push(() => hero.removeEventListener("pointermove", onPointerMove))
    cleanups.push(() => hero.removeEventListener("pointerleave", onPointerLeave))

    flashTimer = window.setInterval(() => {
      hero.classList.remove("is-flashing")
      void hero.offsetWidth
      hero.classList.add("is-flashing")
      flashResetTimer = window.setTimeout(() => hero.classList.remove("is-flashing"), 1300)
    }, 5000)
  }

  host[cleanupKey] = () => {
    cleanups.forEach((cleanup) => cleanup())
    window.clearInterval(flashTimer)
    window.clearTimeout(flashResetTimer)
    if (frame) window.cancelAnimationFrame(frame)
  }
}
""",
)


def home_hero(ir_a):
    return _HOME_HERO(
        key="matallana-home-hero",
        width="stretch",
        height="content",
        on_catalog_change=lambda: ir_a("catalogo"),
        on_design_change=lambda: ir_a("a_medida"),
    )
