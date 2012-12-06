# Copyright (c) 2007-2012 Christoph Haas <email@christoph-haas.de>
# See the file LICENSE for copying permission.

"""Enhances the paginate.Page class to work with SQLAlchemy objects"""

import sys
from nose.tools import eq_, raises
import unittest
import sqlalchemy
import sqlalchemy.orm
import paginate_sqlalchemy

class TestSqlalchemyPage(unittest.TestCase):
    def setUp(self):
        engine = sqlalchemy.create_engine('sqlite:///:memory:', echo=False)
        from sqlalchemy.ext.declarative import declarative_base
        Base = declarative_base()
        from sqlalchemy import Column, Integer, String
        
        class User(Base):
            __tablename__ = 'users'
            id = Column(Integer, primary_key=True)
            name = Column(String)
            
        Base.metadata.create_all(engine)
        
        Session = sqlalchemy.orm.sessionmaker(bind=engine)
        session = Session()
        
        for i in range(1000):
            user = User()
            user.name = i
            session.add(user)
            
        session.commit()

        self.session = session
        self.User = User

    def test_orm(self):
        orm_query = self.session.query(self.User)
        page = paginate_sqlalchemy.SqlalchemyOrmPage(orm_query, page=8)
        eq_(orm_query.count(), 1000)
        eq_(page.first_item, 141)
        eq_(page.last_item, 160)
        eq_(page.page_count, 50)

    @raises(TypeError)
    def test_ormpage_from_wrong_object_type(self):
        # ORM-mapped objects are not supported directly. Only queries on such objects.
        page = paginate_sqlalchemy.SqlalchemyOrmPage(self.User, page=8)

