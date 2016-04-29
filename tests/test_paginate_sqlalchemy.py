# Copyright (c) 2007-2012 Christoph Haas <email@christoph-haas.de>
# See the file LICENSE for copying permission.

"""Enhances the paginate.Page class to work with SQLAlchemy objects"""

import pytest
import sqlalchemy as sa
import sqlalchemy.orm
import paginate_sqlalchemy

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)


@pytest.fixture(scope='function')
def db_engine():
    engine = sa.create_engine('sqlite:///:memory:', echo=True)
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture(scope='function')
def db_session(db_engine):
    return sqlalchemy.orm.sessionmaker(bind=db_engine)()


@pytest.fixture(scope='function')
def base_data(db_session):
    users = []
    for i in range(1000):
        users.append({'id': i, 'name': 'user_{}'.format(i)})
    db_session.execute(User.__table__.insert(), users)
    db_session.commit()


@pytest.mark.usefixtures("base_data")
class TestSqlalchemyPage(object):
    def test_orm(self, db_session):
        orm_query = db_session.query(User)
        page = paginate_sqlalchemy.SqlalchemyOrmPage(
            orm_query, page=8, db_session=db_session)
        assert page.item_count == 1000
        assert page.first_item == 141
        assert page.last_item == 160
        assert page.page_count == 50

    def test_select(self, db_session):
        users_table = User.__table__
        select_query = sqlalchemy.sql.select([users_table])
        page = paginate_sqlalchemy.SqlalchemySelectPage(
            db_session, select_query, page=8)
        assert page.item_count == 1000
        assert page.first_item == 141
        assert page.last_item == 160
        assert page.page_count == 50
