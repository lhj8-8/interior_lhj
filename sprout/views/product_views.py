from flask import Blueprint, render_template, request, jsonify, g, session
from sprout import db
from sprout.models import CartItem
import json
import math

bp = Blueprint('product', __name__, url_prefix='/')


# ㅡㅡㅡㅡㅡㅡㅡㅡ 페이지네이션 클래스 ㅡㅡㅡㅡㅡㅡㅡㅡㅡ
class ProductPagination:
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

    def iter_pages(self, left_edge=1, right_edge=1, left_current=3, right_current=3):
        last = 0
        for num in range(1, self.pages + 1):
            if (num <= left_edge or
                    num > self.pages - right_edge or
                    (num >= self.page - left_current and num <= self.page + right_current)):
                if last + 1 != num:
                    yield None
                yield num
                last = num


# ㅡㅡㅡㅡㅡㅡㅡㅡ JSON 데이터 로드 ㅡㅡㅡㅡㅡㅡㅡㅡ
def load_products():
    try:
        with open('data/products.json', 'r', encoding='utf-8') as f:
            return json.load(f).get('products', [])
    except FileNotFoundError:
        print("❌ ERROR: data/products.json 파일을 찾을 수 없습니다!")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ JSON 파싱 오류: {e}")
        return []


# ㅡㅡㅡㅡㅡㅡㅡㅡ sub 페이지 (검색 + 필터 + 페이지네이션) ㅡㅡㅡㅡㅡㅡㅡㅡ
@bp.route('/sub')
def sub():
    products = load_products()

    # 검색어 & 스타일 파라미터 가져오기
    search_query = request.args.get('search', '').strip().lower()
    selected_style = request.args.get('style', '').strip()

    # 검색 필터링
    if search_query:
        products = [p for p in products if search_query in p.get('name', '').lower()]

    # 스타일 필터링
    if selected_style:
        products = [p for p in products if p.get('style', '').strip() == selected_style]

    # 페이지네이션 처리
    page = request.args.get('page', 1, type=int)
    per_page = 25
    total = len(products)
    start = (page - 1) * per_page
    end = start + per_page
    current_products = products[start:end]

    product_list = ProductPagination(current_products, page, per_page, total)

    # sub.html로 전달
    return render_template(
        'sub.html',
        product_list=product_list,
        selected_style=selected_style,
        search_query=search_query
    )


# ㅡㅡㅡㅡㅡㅡㅡㅡ 장바구니 기능 ㅡㅡㅡㅡㅡㅡㅡㅡ
@bp.route('/cart/add', methods=['POST'])
def cart_add():
    if not session.get('user_id'):
        return jsonify({'success': False, 'message': 'Login required', 'redirect': True}), 401

    data = request.get_json()
    product_id = data.get('product_id')

    print(f"\n장바구니 추가 요청:")
    print(f"  - 사용자: {g.user.username} (ID: {g.user.id})")
    print(f"  - Product ID: {product_id}")

    if not product_id:
        return jsonify({'success': False, 'message': 'Product ID is required'}), 400

    existing = CartItem.query.filter_by(user_id=g.user.id, product_id=product_id).first()

    if existing:
        print(f"  이미 장바구니에 존재함")
        return jsonify({'success': True, 'message': 'Already in cart'})

    new_item = CartItem(user_id=g.user.id, product_id=product_id)
    db.session.add(new_item)
    db.session.commit()

    print(f"  장바구니에 추가 완료 (CartItem ID: {new_item.id})")

    return jsonify({'success': True, 'message': 'Added to cart'})


@bp.route('/cart/remove', methods=['POST'])
def cart_remove():
    if not session.get('user_id'):
        return jsonify({'success': False, 'message': 'Login required', 'redirect': True}), 401

    data = request.get_json()
    product_id = data.get('product_id')

    print(f"\n장바구니 삭제 요청:")
    print(f"  - 사용자: {g.user.username} (ID: {g.user.id})")
    print(f"  - Product ID: {product_id}")

    if not product_id:
        return jsonify({'success': False, 'message': 'Product ID is required'}), 400

    item = CartItem.query.filter_by(user_id=g.user.id, product_id=product_id).first()

    if item:
        db.session.delete(item)
        db.session.commit()
        print(f"  장바구니에서 삭제 완료")
        return jsonify({'success': True, 'message': 'Removed from cart'})

    print(f"  삭제할 아이템을 찾을 수 없음")
    return jsonify({'success': False, 'message': 'Item not found'}), 404


@bp.route('/cart/check')
def cart_check():
    if not session.get('user_id'):
        return jsonify({'cart_items': [], 'logged_in': False})

    cart_items = CartItem.query.filter_by(user_id=g.user.id).all()
    cart_item_ids = [item.product_id for item in cart_items]

    return jsonify({'cart_items': cart_item_ids, 'logged_in': True})
