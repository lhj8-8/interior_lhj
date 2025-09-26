
        // 드롭다운 아이콘 회전 효과
        document.addEventListener('shown.bs.dropdown', function (event) {
            const icon = event.target.querySelector('.bi-chevron-down');
            if (icon) {
                icon.style.transform = 'rotate(180deg)';
            }
        });

        document.addEventListener('hidden.bs.dropdown', function (event) {
            const icon = event.target.querySelector('.bi-chevron-down');
            if (icon) {
                icon.style.transform = 'rotate(0deg)';
            }
        });

        // 필터 함수들
        function resetStyleFilters() {
            document.querySelectorAll('input[name="style"]').forEach(input => input.checked = false);
        }

        function applyStyleFilters() {
            console.log('스타일 필터 적용');
        }

        function resetColorFilters() {
            document.querySelectorAll('input[name="color"]').forEach(input => input.checked = false);
        }

        function applyColorFilters() {
            console.log('색상 필터 적용');
        }

        function resetBrandFilters() {
            document.querySelectorAll('input[name="brand"]').forEach(input => input.checked = false);
        }

        function applyBrandFilters() {
            console.log('브랜드 필터 적용');
        }
