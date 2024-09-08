from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

class UnitOfWork:
    def __init__(self, session_factory: sessionmaker):
        self.session_factory = session_factory
        self.session = None

    def __enter__(self):
        self.session = self.session_factory()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()

    @contextmanager
    def get_session(self):
        session = self.session_factory()
        try:
            yield session
        except:
            session.rollback()
            raise
        finally:
            session.close()
