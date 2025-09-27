/* 비교 슬라이더 초기 설정 */
document.addEventListener('DOMContentLoaded', () => {
  const wrap = document.getElementById('sliderWrapper');
  if(!wrap) return;
  const afterImg   = document.getElementById('afterImage');
  const divider    = document.getElementById('sliderDivider');
  const handle     = document.getElementById('sliderHandle');
  let drag = false;

/* 슬라이더 위치 설정 함수 */
  function setPct(p){
    p = Math.max(0, Math.min(100, p));
    afterImg.style.clipPath = `inset(0 ${100-p}% 0 0)`; //슬라이더 보이는 값 0-100
    divider.style.left = handle.style.left = p + '%';
  }

 /* 슬라이더 위치 계산 함수 */
  function pctFromEvent(e){
    const r = wrap.getBoundingClientRect();
    const x = (e.touches ? e.touches[0].clientX : e.clientX) - r.left;
    return x / r.width * 100;
  }

 /* 슬라이더 드래그 설정 */

 /* 드래그 시작 */
  ['mousedown','touchstart'].forEach(ev => wrap.addEventListener
  (ev, e => { drag = true; setPct(pctFromEvent(e)); e.preventDefault(); }));
 /* 드래그 중 */
  ['mousemove','touchmove'].forEach(ev => document.addEventListener
  (ev, e => { if(drag) { setPct(pctFromEvent(e)); e.preventDefault(); } }));
 /* 드래그 종료 */
  ['mouseup','touchend','touchcancel','mouseleave'].forEach
  (ev => document.addEventListener(ev, () => drag = false));


 /* 초기 슬라이더 위치 */
  setPct(50);
});
