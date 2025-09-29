// 필터 상태 저장용 객체
        let selectedFilters = {
            style: [],
            color: [],
            brand: []
        };

        // 드롭다운 화살표 방향 제어
        document.addEventListener('DOMContentLoaded', function() {
            const dropdowns = document.querySelectorAll('.dropdown');
            
            dropdowns.forEach(dropdown => {
                const dropdownToggle = dropdown.querySelector('.dropdown-toggle');
                const chevronIcon = dropdownToggle.querySelector('.bi-chevron-down, .bi-chevron-up');
                
                if (dropdownToggle && chevronIcon) {
                    dropdown.addEventListener('show.bs.dropdown', function () {
                        chevronIcon.classList.remove('bi-chevron-down');
                        chevronIcon.classList.add('bi-chevron-up');
                    });
                    
                    dropdown.addEventListener('hide.bs.dropdown', function () {
                        chevronIcon.classList.remove('bi-chevron-up');
                        chevronIcon.classList.add('bi-chevron-down');
                    });
                }
            });
        });

        // 스타일 필터 함수들
        function applyStyleFilters() {
            selectedFilters.style = [];
            const checkboxes = document.querySelectorAll('input[name="style"]:checked');
            checkboxes.forEach(cb => selectedFilters.style.push(cb.value));
            console.log('선택된 스타일:', selectedFilters.style);
            updateFilterDisplay('style');
            // 드롭다운 닫기
            bootstrap.Dropdown.getInstance(document.getElementById('styleDropdown')).hide();
        }

        function resetStyleFilters() {
            document.querySelectorAll('input[name="style"]').forEach(cb => cb.checked = false);
            selectedFilters.style = [];
            updateFilterDisplay('style');
            // 드롭다운 닫기
            bootstrap.Dropdown.getInstance(document.getElementById('styleDropdown')).hide();
        }

        // 색상 필터 함수들
        function applyColorFilters() {
            selectedFilters.color = [];
            const checkboxes = document.querySelectorAll('input[name="color"]:checked');
            checkboxes.forEach(cb => selectedFilters.color.push(cb.value));
            console.log('선택된 색상:', selectedFilters.color);
            updateFilterDisplay('color');
            // 드롭다운 닫기
            bootstrap.Dropdown.getInstance(document.getElementById('colorDropdown')).hide();
        }

        function resetColorFilters() {
            document.querySelectorAll('input[name="color"]').forEach(cb => cb.checked = false);
            selectedFilters.color = [];
            updateFilterDisplay('color');
            // 드롭다운 닫기
            bootstrap.Dropdown.getInstance(document.getElementById('colorDropdown')).hide();
        }

        // 브랜드 필터 함수들
        function applyBrandFilters() {
            selectedFilters.brand = [];
            const checkboxes = document.querySelectorAll('input[name="brand"]:checked');
            checkboxes.forEach(cb => selectedFilters.brand.push(cb.value));
            console.log('선택된 브랜드:', selectedFilters.brand);
            updateFilterDisplay('brand');
            // 드롭다운 닫기
            bootstrap.Dropdown.getInstance(document.getElementById('brandDropdown')).hide();
        }

        function resetBrandFilters() {
            document.querySelectorAll('input[name="brand"]').forEach(cb => cb.checked = false);
            selectedFilters.brand = [];
            updateFilterDisplay('brand');
            // 드롭다운 닫기
            bootstrap.Dropdown.getInstance(document.getElementById('brandDropdown')).hide();
        }

        // 필터 버튼 텍스트 업데이트
        function updateFilterDisplay(filterType) {
            const button = document.getElementById(filterType + 'Dropdown');
            const count = selectedFilters[filterType].length;
            let originalText = '';
            
            switch(filterType) {
                case 'style': originalText = '스타일'; break;
                case 'color': originalText = '색상'; break;
                case 'brand': originalText = '브랜드'; break;
            }
            
            const chevronIcon = button.querySelector('.bi-chevron-down, .bi-chevron-up');
            const iconClass = chevronIcon ? chevronIcon.classList.contains('bi-chevron-up') ? 'bi-chevron-up' : 'bi-chevron-down' : 'bi-chevron-down';
            
            if (count > 0) {
                button.innerHTML = `${originalText} (${count}) <i class="bi ${iconClass} ms-1"></i>`;
                button.classList.add('fw-bold');
            } else {
                button.innerHTML = `${originalText} <i class="bi ${iconClass} ms-1"></i>`;
                button.classList.remove('fw-bold');
            }
        }

        console.log('필터 시스템이 준비되었습니다.');