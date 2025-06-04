import argparse
import json

from mjc.model.entity import argue, assignment, common, course, folder, page, user, widget
from mjc.crud.user import create_user, get_user
from mjc.model.schema.user import UserCreate
from mjc.utils.database import get_session_sync

parser = argparse.ArgumentParser()
parser.add_argument('data')


if __name__ == '__main__':
    args = parser.parse_args()
    with open(args.data, 'r', encoding='utf-8') as f:
        data = json.load(f)
    db = get_session_sync()

    for user in data:
        try:
            create_user(db, UserCreate.model_validate(user))
        except Exception as e:
            print(e)
    # import admin
    try:
        create_user(db, UserCreate(
            username='admin',
            password='admin',
            email='admin@sustech.edu.cn',
            department='计算机科学与工程系',
            name='管理员'
        ))
    except Exception as e:
        print(e)
    user = get_user(db, 'admin')
    if user:
        user.is_admin = True
        db.commit()