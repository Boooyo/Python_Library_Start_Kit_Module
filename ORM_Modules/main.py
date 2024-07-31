# main.py

from services.user_service import add_user, get_all_users

def main():
    # 사용자 추가
    add_user(username='testuser', email='test@example.com')

    # 모든 사용자 조회
    get_all_users()

if __name__ == "__main__":
    main()
