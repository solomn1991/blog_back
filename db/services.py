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


class PassageService(BaseService):
    def add_passage(self,user_id,title,content):
        try:
            user = self.session.query(User).filter(User.id==user_id).scalar()
            passage = Passage()
            passage.title=title
            passage.content = content
            passage.user = user.id
            self.session.add(passage)

            self.session.commit()

        except Exception as e:
            self.session.rollback()
            raise e


    def get_passage(self,passage_id):
        passage = self.session.query(Passage).filter(Passage.id==passage_id).scalar()
        return passage


    def get_passage_list(self,user_id):
        passages = self.session.query(Passage).filter(Passage.user==user_id).all()

        return db_formatter.format_result_set(passages)

    def update_passage(self,passage_id,title,content):
        passage = self.session.query(Passage).filter(Passage.id==passage_id).scalar()

        passage.content = content
        passage.title = title
        self.session.commit()


