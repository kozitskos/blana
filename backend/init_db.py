from app.database import engine, Base
from app.models import User, Note, Feedback, Summary

# This will create the tables based on the models if they don't already exist
def init_db():
    Base.metadata.create_all(bind=engine)


init_db()