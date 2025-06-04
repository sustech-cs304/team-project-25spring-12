from mjc.model.schema.user import UserCreate
from mjc.utils.database import get_session_sync
from mjc.service.user import register

if __name__ == "__main__":
    db = get_session_sync()
    register(db, UserCreate(
        username='admin',
        password='admin',
        name='admin',
        email='admin@sustech.edu.cn',
        department='cse'
    ))
    db.close()