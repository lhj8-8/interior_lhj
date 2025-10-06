// sub 제품 찜 로직 (서버 API 연동)

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

  // 페이지 로드 시 장바구니 상태 동기화
  fetch('/cart/check')
    .then(response => response.json())
    .then(data => {
      if (data && data.cart_items && Array.isArray(data.cart_items)) {
        data.cart_items.forEach(productId => {
          const heartBtn = document.querySelector(`button[data-product-id="${productId}"]`);
          if (heartBtn) {
            const heartIcon = heartBtn.querySelector('i');
            heartIcon.classList.remove('bi-heart');
            heartIcon.classList.add('bi-heart-fill');
            heartIcon.style.color = '#dc3545';
          }
        });
      }
    })
    .catch(error => {
      console.error('장바구니 확인 오류:', error);
    });
});

// 장바구니 토글 함수
function toggleWishlist(event, productId) {
    event.preventDefault();
    event.stopPropagation();

    const button = event.currentTarget;
    const heartIcon = button.querySelector('i');
    const isFilled = heartIcon.classList.contains('bi-heart-fill');

    if (isFilled) {
        // 장바구니에서 제거
        fetch('/cart/remove', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ product_id: productId })
        })
        .then(response => {
            if (response.status === 401) {
                alert('로그인이 필요합니다.');
                window.location.href = '/login/?next=' + encodeURIComponent(window.location.pathname);
                return null;
            }
            return response.json();
        })
        .then(data => {
            if (data && data.success) {
                heartIcon.classList.remove('bi-heart-fill');
                heartIcon.classList.add('bi-heart');
                heartIcon.style.color = '#333';
            } else if (data && data.redirect) {
                alert('로그인이 필요합니다.');
                window.location.href = '/login/?next=' + encodeURIComponent(window.location.pathname);
            } else if (data) {
                alert('삭제에 실패했습니다.');
            }
        })
        .catch(error => {
            console.error('오류:', error);
            alert('오류가 발생했습니다.');
        });
    } else {
        // 장바구니에 추가
        fetch('/cart/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ product_id: productId })
        })
        .then(response => {
            if (response.status === 401) {
                alert('로그인이 필요합니다.');
                window.location.href = '/login/?next=' + encodeURIComponent(window.location.pathname);
                return null;
            }
            return response.json();
        })
        .then(data => {
            if (data && data.success) {
                heartIcon.classList.remove('bi-heart');
                heartIcon.classList.add('bi-heart-fill');
                heartIcon.style.color = '#dc3545';

                // 알림 메시지
                const toast = document.createElement('div');
                toast.className = 'position-fixed bottom-0 end-0 p-3';
                toast.style.zIndex = '9999';
                toast.innerHTML = `
                    <div class="toast show" role="alert">
                        <div class="toast-body bg-dark text-white rounded">
                            장바구니에 추가되었습니다!
                        </div>
                    </div>
                `;
                document.body.appendChild(toast);
                setTimeout(() => toast.remove(), 2000);
            } else if (data && data.redirect) {
                alert('로그인이 필요합니다.');
                window.location.href = '/login/?next=' + encodeURIComponent(window.location.pathname);
            } else if (data) {
                alert('추가에 실패했습니다.');
            }
        })
        .catch(error => {
            console.error('오류:', error);
            alert('오류가 발생했습니다.');
        });
    }
}