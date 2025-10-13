/* mypage 장바구니 찜 목록 삭제 로직 */

function removeFromCart(event, productId) {
    event.preventDefault();

    if (confirm('장바구니에서 삭제하시겠습니까?')) {
        fetch('/cart/remove', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ product_id: productId })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert('삭제에 실패했습니다.');
            }
        })
        .catch(error => {
            console.error('오류:', error);
            alert('오류가 발생했습니다.');
        });
    }
}