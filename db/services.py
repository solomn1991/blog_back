from .Session import Session
from .models import User,Passage

from utils import db_formatter


class BaseService(object):
    def __init__(self):
        self.session = Session()




class UserService(BaseService):
    def find_user(self,username):
        record = self.session.query(User).filter(User.username==username).scalar()
        return record

    def add_user(self,username,password,email):
        assert username and password and email

        if self.session.query(User).filter(User.username==username).scalar():
            res = {"register_success":False,"message":"用户名存在"}
            return res

        user = User(username=username, password=password, email=email)
        self.session.add(user)
        self.session.commit()


        res = {"register_success":True,"message":"","user":{"id":user.id,"username":user.username}}
        return res



class PassageService(BaseService):
    def add_passage(self,user_id,title,content):
        try:
            user = self.session.query(User).filter(User.id==user_id).scalar()
            passage = Passage()
            passage.title=title
            passage.content = content
            passage.user = user
            self.session.add(passage)

            self.session.commit()
            return db_formatter.format_row(passage)

        except Exception as e:
            self.session.rollback()
            raise e


    def get_passage(self,passage_id):
        passage = self.session.query(Passage).filter(Passage.id==passage_id).scalar()
        return passage


    def get_passage_list(self,user_id):
        passages = self.session.query(Passage).filter(Passage.user_id==user_id).all()

        return db_formatter.format_result_set(passages)

    def update_passage(self,passage_id,title,content,is_publish):
        assert passage_id is not None
        assert (title!=None and content!=None) or is_publish!=None

        passage = self.session.query(Passage).filter(Passage.id==passage_id).scalar()

        if (title!=None and content!=None):
            passage.content = content
            passage.title = title
            passage.is_publish = is_publish
        else:
            passage.is_publish = is_publish


        self.session.commit()


    def delete_passage(self,id):

        passage = self.session.query(Passage).filter(Passage.id == id).scalar()

        self.session.delete(passage)

        self.session.commit()

    def get_published_passages(self):
        passages = db_formatter.format_result_set(self.session.query(Passage).filter(Passage.is_publish==True).all())
        user_ids = set([passage["user_id"] for passage in passages])
        user_rows = self.session.query(User,User.id,User.username).filter(User.id.in_(user_ids)).all()
        user_map = {}
        for row in user_rows:
            user_map.update({row.id:row.username})

        for passage in passages:
            user_id = passage.get("user_id")
            username = user_map.get(user_id)
            user_info = {"user":{"username":username}}
            passage.update(user_info)








        return passages



