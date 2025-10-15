
 # C:\SJM\flask\project\interior-project-2025\update_db.py

import json
import os
from datetime import datetime
from sqlalchemy import text, inspect
from sprout import create_app, db

app = create_app()


with app.app_context():
    # --- cart-item ---
    with db.engine.connect() as conn:
        try:
            conn.execute(text('ALTER TABLE cart_item ADD COLUMN brand VARCHAR(100)'))
            conn.execute(text('ALTER TABLE cart_item ADD COLUMN name VARCHAR(150)'))
            conn.execute(text('ALTER TABLE cart_item ADD COLUMN price INTEGER'))
            conn.execute(text('ALTER TABLE cart_item ADD COLUMN description TEXT'))
            conn.execute(text('ALTER TABLE cart_item ADD COLUMN image_url VARCHAR(255)'))
            conn.execute(text('ALTER TABLE cart_item ADD COLUMN style VARCHAR(50)'))
            conn.commit()
            print("cart_item 테이블에 상품 정보 컬럼 추가 완료")
        except Exception as e:
            print("이미 컬럼이 존재하거나 오류 발생:", e)

# Flask 앱 컨텍스트 시작
with app.app_context():
    print(" 데이터베이스 업데이트 중...")

    # --- 기존 user 테이블 컬럼 추가 ---
    try:
        with db.engine.connect() as conn:
            conn.execute(text('ALTER TABLE user ADD COLUMN phone VARCHAR(20)'))
            conn.commit()
        print(" phone 컬럼 추가 완료")
    except:
        print(" phone 컬럼은 이미 존재합니다")

    try:
        with db.engine.connect() as conn:
            conn.execute(text('ALTER TABLE user ADD COLUMN address VARCHAR(300)'))
            conn.commit()
        print(" address 컬럼 추가 완료")
    except:
        print(" address 컬럼은 이미 존재합니다")


    # --- product 테이블 + JSON 데이터 삽입 ---
    from sqlalchemy import Column, Integer, String, Text, DateTime

    class Product(db.Model):
        __tablename__ = 'product'
        id = Column(Integer, primary_key=True)
        brand = Column(String(100))
        name = Column(String(150), nullable=False)
        price = Column(Integer, nullable=False)
        description = Column(Text)
        image_url = Column(String(255))
        style = Column(String(50))
        created_date = Column(DateTime, default=datetime.now)

    inspector = inspect(db.engine)
    if 'product' not in inspector.get_table_names():
        print("'product' 테이블이 존재하지 않아 새로 생성합니다...")
        db.create_all()

    # JSON 경로 지정
    json_path = os.path.join('data', 'products.json')
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        products = data.get("products", data)
        print(f"🛒 JSON에서 {len(products)}개의 상품 데이터를 읽었습니다.")

        added = 0
        for item in products:
            if Product.query.get(item.get("id")):
                print(f" 이미 존재: {item.get('name')}")
                continue

            product = Product(
                id=item.get("id"),
                brand=item.get("brand"),
                name=item.get("name"),
                price=item.get("price"),
                description=item.get("description"),
                image_url=item.get("image_url"),
                style=item.get("style")
            )
            db.session.add(product)
            added += 1

        db.session.commit()
        print(f" 총 {added}개의 상품이 DB에 추가되었습니다.")
    else:
        print(f"{json_path} 파일을 찾을 수 없습니다. (상품 데이터 추가 생략)")

    print("\n 모든 DB 업데이트가 완료되었습니다! 이제 서버를 실행하세요: python app.py")
