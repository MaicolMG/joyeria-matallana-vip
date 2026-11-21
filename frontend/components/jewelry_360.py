from urllib.parse import urlparse

import streamlit as st


_VIEWER = st.components.v2.component(
    "matallana_jewelry_viewer",
    html="""
<section class="viewer">
  <div class="stage">
    <img class="piece" alt="Joya Matallana VIP">
    <div class="light"></div>
    <div class="empty" hidden>No hay imágenes adicionales para esta pieza.</div>
  </div>
  <div class="controls">
    <span class="hint">Arrastra para explorar</span>
    <button class="rotate" type="button" aria-pressed="false">Rotación automática</button>
    <span class="frame" aria-live="polite"></span>
  </div>
</section>
""",
    css="""
.viewer { color: #c8bfa8; font: 12px Montserrat, sans-serif; }
.stage { position: relative; display: grid; place-items: center; height: 420px; overflow: hidden; background: radial-gradient(ellipse at 50% 42%, #1c1a14, #080808 70%); touch-action: pan-y; cursor: grab; }
.stage:active { cursor: grabbing; }
.piece { max-width: 90%; max-height: 90%; object-fit: contain; user-select: none; -webkit-user-drag: none; transition: transform .18s ease, filter .3s ease; }
.stage.inspect .piece { transform: scale(1.6); }
.light { position: absolute; inset: 0; pointer-events: none; background: linear-gradient(115deg, transparent 34%, rgba(212,175,55,.16) 49%, transparent 64%); background-size: 220% 100%; animation: gem-light 4s ease-in-out infinite; mix-blend-mode: screen; }
.empty { position: absolute; color: #c8bfa8; letter-spacing: .12em; text-transform: uppercase; }
.controls { display: flex; align-items: center; justify-content: space-between; gap: 12px; padding-top: 12px; }
.hint, .frame { color: #9a9080; letter-spacing: .1em; }
.rotate { padding: 9px 14px; color: #d4af37; background: transparent; border: 1px solid rgba(212,175,55,.45); font: inherit; letter-spacing: .12em; cursor: pointer; }
.rotate:hover, .rotate[aria-pressed="true"] { color: #080808; background: #d4af37; }
@keyframes gem-light { 0%, 12% { background-position: 100% 0; } 55%, 100% { background-position: -100% 0; } }
@media (prefers-reduced-motion: reduce) { .light { animation: none; } }
""",
    js="""
export default function (component) {
  const { data, parentElement } = component
  const stage = parentElement.querySelector(".stage")
  const image = parentElement.querySelector(".piece")
  const empty = parentElement.querySelector(".empty")
  const button = parentElement.querySelector(".rotate")
  const frame = parentElement.querySelector(".frame")
  const images = Array.isArray(data?.images) ? data.images : []
  const label = String(data?.label || "Joya Matallana VIP")
  let index = 0
  let startX = null
  let lastX = null
  let timer = null

  image.alt = label
  if (!images.length) {
    image.hidden = true
    empty.hidden = false
    button.disabled = true
  } else {
    image.src = images[0]
    frame.textContent = images.length > 1 ? `1 / ${images.length}` : "Vista de inspección"
    if (images.length < 2) {
      button.disabled = true
      button.textContent = "Inspección con una imagen"
    }
  }

  const showFrame = (next) => {
    index = (next + images.length) % images.length
    image.src = images[index]
    frame.textContent = images.length > 1 ? `${index + 1} / ${images.length}` : "Vista de inspección"
  }
  const stop = () => {
    if (timer) window.clearInterval(timer)
    timer = null
    button.setAttribute("aria-pressed", "false")
  }

  stage.addEventListener("pointerdown", (event) => {
    startX = event.clientX
    lastX = event.clientX
    stage.setPointerCapture(event.pointerId)
  })
  stage.addEventListener("pointermove", (event) => {
    if (startX === null) return
    const delta = event.clientX - lastX
    if (images.length > 1 && Math.abs(event.clientX - startX) >= 28) {
      showFrame(index + (delta < 0 ? 1 : -1))
      startX = event.clientX
    } else if (images.length === 1) {
      const bounds = stage.getBoundingClientRect()
      image.style.transformOrigin = `${Math.max(0, Math.min(100, (event.clientX - bounds.left) / bounds.width * 100))}% ${Math.max(0, Math.min(100, (event.clientY - bounds.top) / bounds.height * 100))}%`
    }
    lastX = event.clientX
  })
  stage.addEventListener("pointerup", () => { startX = null })
  stage.addEventListener("pointercancel", () => { startX = null })
  stage.addEventListener("pointerenter", () => {
    if (images.length === 1) stage.classList.add("inspect")
  })
  stage.addEventListener("pointerleave", () => {
    stage.classList.remove("inspect")
    image.style.transformOrigin = "center"
  })
  button.addEventListener("click", () => {
    if (timer) {
      stop()
      return
    }
    button.setAttribute("aria-pressed", "true")
    timer = window.setInterval(() => showFrame(index + 1), 650)
  })
  parentElement.addEventListener("DOMNodeRemoved", stop, { once: true })
}
""",
)


def jewelry_360(product, *, key):
    image_urls = product.get("imagenes_360") or []
    if not isinstance(image_urls, list):
        image_urls = []
    if not image_urls and product.get("imagen"):
        image_urls = [product["imagen"]]

    safe_urls = []
    for image_url in image_urls[:36]:
        if not isinstance(image_url, str):
            continue
        parsed = urlparse(image_url.strip())
        if parsed.scheme in {"http", "https"} and parsed.netloc:
            safe_urls.append(image_url.strip())

    return _VIEWER(
        data={
            "images": safe_urls,
            "label": str(product.get("nombre", "Joya Matallana VIP"))[:120],
        },
        key=key,
        width="stretch",
        height=470,
    )
