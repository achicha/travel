from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# db_connector
class DataAccessLayer:
    """ access to DB fabric"""

    def __init__(self, conn_string, base, echo=False):
        self.engine = None
        self.session = None
        self.conn = None
        self.conn_string = conn_string
        self.echo = echo
        self.Base = base

    def connect(self):
        self.engine = create_engine(self.conn_string, echo=self.echo)
        self.Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
