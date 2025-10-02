// 카테고리 토글 버튼
document.addEventListener('DOMContentLoaded', function () {
  const categoryToggles = document.querySelectorAll('.category-toggle');

  categoryToggles.forEach(function (toggle) {
    const targetId = toggle.getAttribute('data-bs-target');
    const targetElement = document.querySelector(targetId);

    if (targetElement) {
      targetElement.addEventListener('show.bs.collapse', function () {
        toggle.setAttribute('aria-expanded', 'true');
      });

      targetElement.addEventListener('hide.bs.collapse', function () {
        toggle.setAttribute('aria-expanded', 'false');
      });
    }
  });
});

// 찜 목록 토글 함수
function toggleWishlist(event, productId) {
    event.preventDefault();
    event.stopPropagation();

    const btn = event.currentTarget;
    const icon = btn.querySelector('i');

    // 하트 상태 토글
    if (icon.classList.contains('bi-heart')) {
        // 빈 하트 -> 채워진 하트
        icon.classList.remove('bi-heart');
        icon.classList.add('bi-heart-fill');
        icon.style.color = '#dc3545'; // 빨간색

        // 찜 목록에 추가
        addToWishlist(productId);
    } else {
        // 채워진 하트 -> 빈 하트
        icon.classList.remove('bi-heart-fill');
        icon.classList.add('bi-heart');
        icon.style.color = '#333';

        // 찜 목록에서 제거
        removeFromWishlist(productId);
    }
}

// 찜 목록에 추가
function addToWishlist(productId) {
    // 로컬 스토리지에서 찜 목록 가져오기
    let wishlist = JSON.parse(localStorage.getItem('wishlist') || '[]');

    // 중복 체크 후 추가
    if (!wishlist.includes(productId)) {
        wishlist.push(productId);
        localStorage.setItem('wishlist', JSON.stringify(wishlist));
        console.log('찜 목록에 추가:', productId);
    }
}

// 찜 목록에서 제거
function removeFromWishlist(productId) {
    let wishlist = JSON.parse(localStorage.getItem('wishlist') || '[]');
    wishlist = wishlist.filter(id => id !== productId);
    localStorage.setItem('wishlist', JSON.stringify(wishlist));
    console.log('찜 목록에서 제거:', productId);
}

// 페이지 로드 시 찜 목록 상태 복원
document.addEventListener('DOMContentLoaded', function() {
    const wishlist = JSON.parse(localStorage.getItem('wishlist') || '[]');

    wishlist.forEach(productId => {
        const btn = document.querySelector(`[data-product-id="${productId}"]`);
        if (btn) {
            const icon = btn.querySelector('i');
            icon.classList.remove('bi-heart');
            icon.classList.add('bi-heart-fill');
            icon.style.color = '#dc3545';
        }
    });
});