# ditis.social

Persoonlijke pitchpagina's van ditisABC. Elke map is een pagina: ditis.social/<map>/

## Standaard bij elke video: afspeelknop als ditisABC-pixel

Elke video op een pitchpagina krijgt een overlay met een afspeelknop in de vorm van de pixel uit het
ditisABC-logo (oranje #FF7141, pulserend), een label "Video · <duur>" en een korte titel met ondertitel.
Zonder overlay lijkt een video een plaatje. Gebruik een poster zonder ondertitel in beeld.

- Staande video (9:16): `<div class="vwrap" style="--vr:26px">`
- Kleine staande video: voeg `klein` toe
- Liggende video (16:9) met tekst in het midden van de poster: voeg `wide` toe (knop linksonder)
- De `<video>` krijgt geen `controls`; die komen erbij zodra hij speelt. Ook `video.play()` vanuit
  eigen code (bijvoorbeeld hoofdstukknoppen) verbergt de overlay.
- Duur in het label exact uit het bestand halen (ffprobe), niet afronden naar een mooi getal.

Voorbeelden in gebruik: kadoburo, ditisdressing, chelsea.

HTML per video:

```html
<div class="vwrap" style="--vr:26px"><video playsinline preload="metadata" poster="media/poster.jpg" src="media/VIDEO.mp4"></video><span class="vtag"><i></i>Video · 1:18</span><button class="vplay" type="button" aria-label="Speel de video af"><span class="pb"><svg viewBox="84.4 -0.2 30.6 30.6" aria-hidden="true"><path class="halo" d="M113.134 7.98374H111.275C110.803 7.98374 110.418 7.59782 110.418 7.12346V5.25817C110.418 4.78381 110.034 4.39789 109.561 4.39789H107.702C107.229 4.39789 106.845 4.01197 106.845 3.53761V1.67232C106.845 1.19796 106.46 0.812042 105.988 0.812042H93.4007C92.928 0.812042 92.5435 1.19796 92.5435 1.67232V3.53761C92.5435 4.01197 92.1589 4.39789 91.6862 4.39789H89.8274C89.3547 4.39789 88.9701 4.78381 88.9701 5.25817V7.12346C88.9701 7.59782 88.5856 7.98374 88.1129 7.98374H86.2541C85.7814 7.98374 85.3968 8.36966 85.3968 8.84402V21.4749C85.3968 21.9493 85.7814 22.3352 86.2541 22.3352H88.1129C88.5856 22.3352 88.9701 22.7211 88.9701 23.1955V25.0607C88.9701 25.5351 89.3547 25.921 89.8274 25.921H91.6862C92.1589 25.921 92.5435 26.3069 92.5435 26.7813V28.6466C92.5435 29.121 92.928 29.5069 93.4007 29.5069H105.988C106.46 29.5069 106.845 29.121 106.845 28.6466V26.7813C106.845 26.3069 107.229 25.921 107.702 25.921H109.561C110.034 25.921 110.418 25.5351 110.418 25.0607V23.1955C110.418 22.7211 110.803 22.3352 111.275 22.3352H113.134C113.607 22.3352 113.992 21.9493 113.992 21.4749V8.84402C113.992 8.36966 113.607 7.98374 113.134 7.98374Z"/><path class="body" d="M113.134 7.98374H111.275C110.803 7.98374 110.418 7.59782 110.418 7.12346V5.25817C110.418 4.78381 110.034 4.39789 109.561 4.39789H107.702C107.229 4.39789 106.845 4.01197 106.845 3.53761V1.67232C106.845 1.19796 106.46 0.812042 105.988 0.812042H93.4007C92.928 0.812042 92.5435 1.19796 92.5435 1.67232V3.53761C92.5435 4.01197 92.1589 4.39789 91.6862 4.39789H89.8274C89.3547 4.39789 88.9701 4.78381 88.9701 5.25817V7.12346C88.9701 7.59782 88.5856 7.98374 88.1129 7.98374H86.2541C85.7814 7.98374 85.3968 8.36966 85.3968 8.84402V21.4749C85.3968 21.9493 85.7814 22.3352 86.2541 22.3352H88.1129C88.5856 22.3352 88.9701 22.7211 88.9701 23.1955V25.0607C88.9701 25.5351 89.3547 25.921 89.8274 25.921H91.6862C92.1589 25.921 92.5435 26.3069 92.5435 26.7813V28.6466C92.5435 29.121 92.928 29.5069 93.4007 29.5069H105.988C106.46 29.5069 106.845 29.121 106.845 28.6466V26.7813C106.845 26.3069 107.229 25.921 107.702 25.921H109.561C110.034 25.921 110.418 25.5351 110.418 25.0607V23.1955C110.418 22.7211 110.803 22.3352 111.275 22.3352H113.134C113.607 22.3352 113.992 21.9493 113.992 21.4749V8.84402C113.992 8.36966 113.607 7.98374 113.134 7.98374Z"/><g fill="#fff"><rect x="94.90" y="9.16" width="3.03" height="12.00"/><rect x="97.90" y="10.66" width="3.03" height="9.00"/><rect x="100.90" y="12.16" width="3.03" height="6.00"/><rect x="103.90" y="13.66" width="3.03" height="3.00"/></g></svg></span><span class="vl">Bekijk de video<small>Korte ondertitel</small></span></button></div>
```

Eenmalig onderaan de pagina:

```html
<script>document.querySelectorAll(".vwrap").forEach(function(w){var v=w.querySelector("video");function go(){w.classList.add("speelt");v.controls=true}w.querySelector(".vplay").addEventListener("click",function(){go();var p=v.play();if(p&&p.catch)p.catch(function(){})});v.addEventListener("play",go)});</script>
```

CSS (eenmalig):

```css
/* ditisABC: afspeelknop als pixel (standaard bij elke video) */
.vwrap{position:relative;overflow:hidden;border-radius:var(--vr,0)}
.vwrap video{display:block}
.vplay{position:absolute;inset:0;border:0;padding:0;margin:0;cursor:pointer;background:linear-gradient(180deg,rgba(0,19,46,0) 45%,rgba(0,19,46,.78) 100%);display:flex;align-items:center;justify-content:center;color:#fff;font:inherit;-webkit-appearance:none;appearance:none}
.vplay .pb{width:104px;height:104px;display:block;transition:transform .2s}
.vplay:hover .pb,.vplay:focus-visible .pb{transform:scale(1.08)}
.vplay .pb svg{width:100%;height:100%;overflow:visible}
.vplay .pb .body,.vplay .pb .halo{fill:#FF7141}
.vplay .pb .halo{transform-box:fill-box;transform-origin:center;animation:pixpuls 2s infinite}
@keyframes pixpuls{0%{transform:scale(1);opacity:.55}70%{transform:scale(1.45);opacity:0}100%{transform:scale(1.45);opacity:0}}
@media (prefers-reduced-motion:reduce){.vplay .pb .halo{animation:none;opacity:0}}
.vplay .vl{position:absolute;left:0;right:0;bottom:22px;text-align:center;font-weight:800;font-size:22px;line-height:1.15}
.vplay .vl small{display:block;font-weight:500;font-size:14px;opacity:.9;margin-top:4px}
.vtag{position:absolute;top:14px;left:14px;z-index:2;background:rgba(0,19,46,.78);color:#fff;font-weight:600;font-size:13px;line-height:1;border-radius:999px;padding:6px 11px;display:flex;align-items:center;gap:6px;pointer-events:none}
.vtag i{width:8px;height:8px;border-radius:1px;background:#FF7141}
.vwrap.wide .vplay{justify-content:flex-start;align-items:flex-end;padding:0 0 24px 26px;background:linear-gradient(180deg,rgba(0,19,46,0) 55%,rgba(0,19,46,.72) 100%)}
.vwrap.wide .vplay .pb{width:80px;height:80px;flex:0 0 auto}
.vwrap.wide .vplay .vl{position:static;text-align:left;margin:0 0 14px 18px}
.vwrap.klein .vplay .pb{width:84px;height:84px}
.vwrap.klein .vplay .vl{font-size:19px;bottom:16px}
.vwrap.speelt .vplay,.vwrap.speelt .vtag{display:none}
@media (max-width:640px){.vwrap.wide .vplay{padding:0 0 12px 12px}.vwrap.wide .vplay .pb{width:48px;height:48px}.vwrap.wide .vplay .vl{font-size:15px;margin:0 0 6px 10px}.vwrap.wide .vplay .vl small{font-size:12px;margin-top:2px}.vwrap.wide .vtag{top:10px;left:10px;font-size:11px;padding:4px 8px}}
```
