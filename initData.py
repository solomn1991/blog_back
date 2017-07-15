from db import engine,Base
from db.models import User
from db.Session import Session

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


session = Session()

users = [
    {"name":"wangwang","password":"miaomiao"},
]

for user in users:
    session.add(User(username=user.get("name"),password=user.get("password")))


session.commit()




