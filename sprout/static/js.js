// 메인 a/b 비교 슬라이더 로직

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

       // 메인 스크롤 이벤트 리스너
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;

            // 각 행마다 다른 속도와 방향으로 이동
            const row1 = document.getElementById('row1');
            const row2 = document.getElementById('row2');
            const row3 = document.getElementById('row3');

            // 첫 번째 행: 왼쪽으로 이동 (음수)
            row1.style.transform = `translateX(-${scrolled * 0.3}px)`;

            // 두 번째 행: 오른쪽으로 이동 (양수)
            row2.style.transform = `translateX(${scrolled * 0.25}px)`;

            // 세 번째 행: 왼쪽으로 이동 (음수, 더 빠르게)
            row3.style.transform = `translateX(-${scrolled * 0.35}px)`;
        });

        // 페이지 로드 시 초기 위치 설정
        window.addEventListener('load', () => {
            document.getElementById('row1').style.transform = 'translateX(0px)';
            document.getElementById('row2').style.transform = 'translateX(0px)';
            document.getElementById('row3').style.transform = 'translateX(0px)';
        });