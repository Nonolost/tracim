from tracim.model import DeclarativeBase
from sqlalchemy import Column, UnicodeText, Unicode, Float, ForeignKey, DateTime
from sqlalchemy.ext.hybrid import hybrid_property
from time import mktime
from datetime import datetime

class Lock(DeclarativeBase):
    __tablename__ = 'locks'

    token = Column(Unicode(1024), primary_key=True, unique=False, nullable=False) # id identifying lock
    depth = Column(Unicode(8), unique=False, nullable=False, default='infinity') # 0, 1, infinity
    user_mail = Column(Unicode(255), ForeignKey('users.email', ondelete='CASCADE', onupdate='CASCADE'), unique=True, nullable=False)
    xml_owner = Column(UnicodeText, unique=False, nullable=False) # string identifying an owner
    # "<?xml version=\'1.0\' encoding=\'UTF-8\'?>\\n<owner xmlns="DAV:">litmus test suite</owner>\\n"

    url_resource = Column(UnicodeText, unique=False, nullable=False) # url of resource
    type = Column(Unicode(32), unique=False, nullable=False, default='write') # write / read
    timeout = Column(Float, unique=False, nullable=False) # seconds until timeout

    expire = Column(DateTime, unique=False, nullable=False) # = time() + timeout
    scope = Column(Unicode(32), unique=False, nullable=False, default='exclusive') # shared / exclusive

    @hybrid_property
    def token(self) -> str:
        return self.token

    @token.setter
    def token(self, value: str):
        self.token = value

    @hybrid_property
    def depth(self) -> str:
        return self.depth

    @depth.setter
    def depth(self, value: str):
        self.depth = value

    @hybrid_property
    def principal(self) -> str:
        return self.user_mail

    @principal.setter
    def principal(self, value: str):
        self.user_mail = value

    @hybrid_property
    def owner(self):
        return self.xml_owner

    @owner.setter
    def owner(self, value: str):
        self.xml_owner = value

    @hybrid_property
    def root(self):
        return self.url_resource

    @root.setter
    def root(self, value: str):
        self.url_resource = value

    @hybrid_property
    def type(self):
        return self.type

    @type.setter
    def type(self, value: str):
        self.type = value

    @hybrid_property
    def timeout(self):
        return self.timeout

    @timeout.setter
    def timeout(self, value: float):
        self.timeout = value

    @hybrid_property
    def scope(self):
        return self.scope

    @scope.setter
    def scope(self, value: str):
        self.scope = value

    @hybrid_property
    def expire(self):
        return mktime(self.expire)

    @expire.setter
    def expire(self, value: float):
        self.expire = datetime.fromtimestamp(value)



class Url2Token(DeclarativeBase):
    __tablename__ = 'url2token'

    token = Column(Unicode(1024), primary_key=True, unique=False, nullable=False, default='')
    path = Column(Unicode(1024), unique=False, nullable=False, default='')

    def get_token(self):
        return self.token

    def get_path(self):
        return self.path
