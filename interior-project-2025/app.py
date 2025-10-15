from sprout import create_app, db
from sprout.models import User, CartItem
from flask import render_template, request
import os, json

# sprout 패키지의 create_app() 사용
app = create_app()


# 더미 데이터 생성 함수 (필요시 사용)
def create_dummy_data():
    with app.app_context():
        db.create_all()
        print('데이터베이스 테이블 생성 완료!')


# 상세 페이지 라우트
@app.route("/product_detail")
def product_detail():
    product_id = request.args.get("product_id")

    # product_id가 없거나 정수가 아닐 때 처리
    try:
        product_id = int(product_id)
    except (TypeError, ValueError):
        return " 잘못된 product_id 형식입니다.", 400

    # JSON 파일 경로
    json_path = os.path.join(os.getcwd(), "data", "products.json")

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            products = data.get("products", [])
    except FileNotFoundError:
        return " products.json 파일을 찾을 수 없습니다.", 404
    except json.JSONDecodeError as e:
        return f" JSON 형식 오류: {e}", 400

    # id 일치하는 상품 찾기
    product = next((p for p in products if p.get("id") == product_id), None)

    if not product:
        return f" id={product_id}에 해당하는 상품을 찾을 수 없습니다.", 404

    return render_template("product_detail.html", product=product)


# 등록된 라우트 확인
with app.app_context():
    print("\n" + "=" * 70)
    print("📋 등록된 라우트 목록")
    print("=" * 70)
    for rule in app.url_map.iter_rules():
        methods = ','.join(sorted(rule.methods - {'HEAD', 'OPTIONS'}))
        print(f"{rule.endpoint:35s} {methods:15s} {rule.rule}")
    print("=" * 70 + "\n")


if __name__ == '__main__':
    # 데이터베이스 테이블 생성
    create_dummy_data()

    # Flask 서버 실행
    app.run(debug=True)
