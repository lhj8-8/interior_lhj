// 메인 페이지 로드 시 초기화
document.addEventListener('DOMContentLoaded', () => {
  // 비교 슬라이더 초기화
  const wrap = document.getElementById('sliderWrapper');
  if(wrap) {
    const afterImg = document.getElementById('afterImage');
    const divider = document.getElementById('sliderDivider');
    const handle = document.getElementById('sliderHandle');
    let drag = false;

    /* 슬라이더 위치 설정 함수 */
    function setPct(p){
      p = Math.max(0, Math.min(100, p));
      afterImg.style.clipPath = `inset(0 ${100-p}% 0 0)`;
      divider.style.left = handle.style.left = p + '%';
    }

    /* 슬라이더 위치 계산 함수 */
    function pctFromEvent(e){
      const r = wrap.getBoundingClientRect();
      const x = (e.touches ? e.touches[0].clientX : e.clientX) - r.left;
      return x / r.width * 100;
    }

    /* 슬라이더 드래그 설정 */
    ['mousedown','touchstart'].forEach(ev => wrap.addEventListener
    (ev, e => { drag = true; setPct(pctFromEvent(e)); e.preventDefault(); }));

    ['mousemove','touchmove'].forEach(ev => document.addEventListener
    (ev, e => { if(drag) { setPct(pctFromEvent(e)); e.preventDefault(); } }));

    ['mouseup','touchend','touchcancel','mouseleave'].forEach
    (ev => document.addEventListener(ev, () => drag = false));

    /* 초기 슬라이더 위치 */
    setPct(50);
  }

  // section_3 video
  const video = document.querySelector('.section_3 video');
  if (video) {
    // 비디오가 자동 재생되도록 재생
    video.play().catch(err => console.log('Video autoplay failed:', err));

    // 마우스를 올렸을 때 소리 켜기
    video.addEventListener('mouseenter', function() {
      video.muted = false;
      video.play(); // 재생 확인
    });

    // 마우스를 뗐을 때 다시 음소거
    video.addEventListener('mouseleave', function() {
      video.muted = true;
    });
  }
});

// 메인 스크롤 이벤트 리스너
window.addEventListener('scroll', () => {
  const scrolled = window.pageYOffset;

  // 각 행마다 다른 속도와 방향으로 이동
  const row1 = document.getElementById('row1');
  const row2 = document.getElementById('row2');
  const row3 = document.getElementById('row3');

  if(row1) row1.style.transform = `translateX(-${scrolled * 0.3}px)`;
  if(row2) row2.style.transform = `translateX(${scrolled * 0.05}px)`;
  if(row3) row3.style.transform = `translateX(-${scrolled * 0.35}px)`;
});

// 페이지 로드 시 초기 위치 설정
window.addEventListener('load', () => {
  const row1 = document.getElementById('row1');
  const row2 = document.getElementById('row2');
  const row3 = document.getElementById('row3');

  if(row1) row1.style.transform = 'translateX(0px)';
  if(row2) row2.style.transform = 'translateX(0px)';
  if(row3) row3.style.transform = 'translateX(0px)';
});

/* 헤더 스크롤 효과 */
window.addEventListener('scroll', function() {
  const header = document.querySelector('.header');
  if (header) {
    if (window.scrollY > 50) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  }
});