    // 카테고리 토글 버튼 화살표 회전 기능
    document.addEventListener('DOMContentLoaded', function() {
        // 모든 카테고리 토글 버튼 선택
        const categoryToggles = document.querySelectorAll('.category-toggle');

        categoryToggles.forEach(function(toggle) {
            // 연결된 collapse 요소 찾기
            const targetId = toggle.getAttribute('data-bs-target');
            const targetElement = document.querySelector(targetId);

            if (targetElement) {
                // collapse가 보일 때 이벤트
                targetElement.addEventListener('show.bs.collapse', function() {
                    toggle.setAttribute('aria-expanded', 'true');
                });

                // collapse가 숨겨질 때 이벤트
                targetElement.addEventListener('hide.bs.collapse', function() {
                    toggle.setAttribute('aria-expanded', 'false');
                });
            }
        });
    });