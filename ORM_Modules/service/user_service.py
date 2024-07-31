from models.database import Session
from models.user import User

def add_user(username: str, email: str):
    session = Session()  # 세션 생성
    try:
        new_user = User(username=username, email=email)
        session.add(new_user)
        session.commit()
        print(f'User added: {username}')
    except Exception as e:
        session.rollback()
        print(f'Error adding user: {e}')
    finally:
        session.close()

def get_all_users():
    session = Session()  # 세션 생성
    try:
        users = session.query(User).all()
        for user in users:
            print(f'ID: {user.id}, Username: {user.username}, Email: {user.email}')
    except Exception as e:
        print(f'Error retrieving users: {e}')
    finally:
        session.close()
