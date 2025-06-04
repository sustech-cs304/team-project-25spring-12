import json
import random

from faker import Faker
from mjc.model.schema.user import UserCreate

fake = Faker(locale='zh_CN')
student_num = 110
sid_start = 12110000
teacher_num = 10
tid_start = 12120000

departments = ['计算机科学与工程系', '数学系', '物理系']

if __name__ == '__main__':
    result = []
    for i in range(student_num):
        user = UserCreate(
            username=str(sid_start + i),
            password=str(sid_start + i),
            name=fake.name(),
            email=fake.email(domain="mail.sustech.edu.cn"),
            department=random.choice(departments)
        )
        result.append(user.model_dump())

    for i in range(teacher_num):
        user = UserCreate(
            username=str(tid_start + i),
            password=str(tid_start + i),
            name=fake.name(),
            email=fake.email(domain="mail.sustech.edu.cn"),
            department=random.choice(departments)
        )
        result.append(user.model_dump())
    with open('mock_users.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)