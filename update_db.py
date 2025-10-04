# 프로젝트 루트에 생성 후 1회 실행

from sprout import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    print("데이터베이스 업데이트 중...")

    try:
        # phone 컬럼 추가
        with db.engine.connect() as conn:
            conn.execute(text('ALTER TABLE user ADD COLUMN phone VARCHAR(20)'))
            conn.commit()
        print("✅ phone 컬럼 추가 완료")
    except:
        print("⚠️ phone 컬럼은 이미 존재합니다")

    try:
        # address 컬럼 추가
        with db.engine.connect() as conn:
            conn.execute(text('ALTER TABLE user ADD COLUMN address VARCHAR(300)'))
            conn.commit()
        print("✅ address 컬럼 추가 완료")
    except:
        print("⚠️ address 컬럼은 이미 존재합니다")

    try:
        # cart_item 테이블 생성
        db.create_all()
        print("✅ cart_item 테이블 생성 완료")
    except:
        print("⚠️ cart_item 테이블은 이미 존재합니다")

    print("\n✅ 완료! 이제 서버를 실행하세요: python app.py")