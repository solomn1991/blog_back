from sqlalchemy.orm import sessionmaker
from .engine import engine

Session = sessionmaker()
Session.configure(bind=engine)