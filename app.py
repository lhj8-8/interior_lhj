from sprout import create_app, db
from sprout.models import User, CartItem

# sprout 패키지의 create_app() 사용
app = create_app()


# 더미 데이터 생성 함수 (필요시 사용)
def create_dummy_data():
    with app.app_context():
        db.create_all()
        # User 테이블과 CartItem 테이블만 생성
        # 제품 데이터는 data/products.json에서
        print('데이터베이스 테이블 생성 완료!')


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