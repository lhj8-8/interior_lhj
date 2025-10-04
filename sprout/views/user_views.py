from flask import Blueprint, render_template, request, g, session, redirect, url_for
from sprout.models import CartItem
import json
import math
import os

bp = Blueprint('user', __name__, url_prefix='/')


# 로그인 데코레이터
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


class PaginatedItems:
    def __init__(self, items, page, per_page, total):
        self.items = items
        self.page = page
        self.per_page = per_page
        self.total = total
        self.pages = math.ceil(total / per_page) if total > 0 else 1

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    @property
    def prev_num(self):
        return self.page - 1 if self.has_prev else None

    @property
    def next_num(self):
        return self.page + 1 if self.has_next else None

    def iter_pages(self, left_edge=1, right_edge=1, left_current=2, right_current=2):
        last = 0
        for num in range(1, self.pages + 1):
            if (num <= left_edge or
                    (num > self.page - left_current - 1 and num < self.page + right_current) or
                    num > self.pages - right_edge):
                if last + 1 != num:
                    yield None
                yield num
                last = num


@bp.route('/mypage')
@login_required
def mypage():
    page = request.args.get('page', 1, type=int)
    per_page = 3  # 페이지당 3개씩 표시

    print(f"\n{'=' * 60}")
    print(f"마이페이지 장바구니 조회")
    print(f"{'=' * 60}")
    print(f"사용자: {g.user.username} (ID: {g.user.id})")
    print(f"페이지: {page}")

    # DB에서 장바구니 아이템 조회
    cart_items_db = CartItem.query.filter_by(user_id=g.user.id).order_by(CartItem.created_date.desc()).all()
    print(f"DB 장바구니 아이템: {len(cart_items_db)}개")

    if not cart_items_db:
        print("장바구니가 비어있습니다")
        print(f"{'=' * 60}\n")
        return render_template('mypage.html', cart_items=None)

    # JSON 파일에서 제품 데이터 로드
    json_path = os.path.join('data', 'products.json')

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            all_products = data.get('products', [])
            print(f"JSON 제품: {len(all_products)}개 로드")
    except Exception as e:
        print(f"ERROR: {e}")
        return render_template('mypage.html', cart_items=None)

    if not all_products:
        print("ERROR: 제품 데이터가 비어있습니다")
        return render_template('mypage.html', cart_items=None)

    # 제품 ID로 딕셔너리 생성
    products_dict = {product['id']: product for product in all_products}

    # 장바구니 아이템과 제품 정보 매칭 (사용자 기반)
    items_with_info = []

    for cart_item in cart_items_db:
        product_id = cart_item.product_id

        if product_id in products_dict:
            product = products_dict[product_id].copy()
            product['id'] = product_id
            items_with_info.append(product)
            print(f"  매칭: {product['name']}")
        else:
            print(f"  매칭 실패: Product ID {product_id}")

    print(f"최종 매칭: {len(items_with_info)}개")

    if not items_with_info:
        return render_template('mypage.html', cart_items=None)

    # 3개의 이미지 이상 페이지네이션
    total = len(items_with_info)
    start = (page - 1) * per_page
    end = start + per_page
    current_items = items_with_info[start:end]

    print(f"현재 페이지: {page}/{math.ceil(total / per_page)}")
    print(f"표시 아이템: {len(current_items)}개")
    print(f"{'=' * 60}\n")

    cart_items = PaginatedItems(current_items, page, per_page, total)

    return render_template('mypage.html', cart_items=cart_items)