const products = {
    chair_black: {
        brand: "콜드 포그",
        name: "CHAIR_ 블랙 스트라이프",
        price: 405000,
        originalPrice: 450000,
        discount: "10%",
        cardBenefit: "75,000원 (6개월 할부시)",
        deliveryPeriod: "주문 제작 약 3주 이내",
        deliveryMethod: "브랜드사 배송",
        shippingFee: "10,000원",
        jejuFee: "제주 및 도서산간 배송비 개당 40,000원",
        image: "chair_black.png"
    },
    chair_white: {
        brand: "콜드 포그",
        name: "CHAIR_ 화이트 스트라이프",
        price: 385000,
        originalPrice: 430000,
        discount: "10%",
        cardBenefit: "70,000원 (6개월 할부시)",
        deliveryPeriod: "주문 제작 약 2~3주 이내",
        deliveryMethod: "브랜드사 배송",
        shippingFee: "10,000원",
        jejuFee: "제주 및 도서산간 배송비 개당 40,000원",
        image: "chair_white.png"
    }
};

function formatPrice(price) {
    return price.toLocaleString() + "원";
}

function showDetails(key) {
    const product = products[key];
    const html = `
        <img src="${product.image}" alt="${product.name}">
        <div>
          <h4>${product.brand}</h4>
          <h2>${product.name}</h2>
          <div>
            <span class="original-price">${formatPrice(product.originalPrice)}</span>
            <span style="color: red;">${product.discount}</span>
            <div class="price">${formatPrice(product.price)}</div>
          </div>
          <ul>
            <li><strong>카드혜택:</strong> ${product.cardBenefit}</li>
            <li><strong>배송기간:</strong> ${product.deliveryPeriod}</li>
            <li><strong>배송방법:</strong> ${product.deliveryMethod}</li>
            <li><strong>배송비:</strong> ${product.shippingFee}</li>
            <li><strong>배송안내:</strong> ${product.jejuFee}</li>
          </ul>
          <div class="button-group">
            <button>문의하기</button>
            <button>장바구니 담기</button>
            <button style="background: black; color: white;">구매하기</button>
          </div>
        </div>
      `;
    document.getElementById('productDetails').innerHTML = html;
}

// 페이지 로드 시 기본 제품 보여주기
window.onload = () => showDetails('chair_black');
