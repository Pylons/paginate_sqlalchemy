# Copyright (c) 2007-2012 Christoph Haas <email@christoph-haas.de>
# See the file LICENSE for copying permission.

"""Enhances the paginate.Page class to work with SQLAlchemy objects"""

import paginate


class SqlalchemyOrmWrapper(object):
    """Wrapper class to access elements of an SQLAlchemy ORM query result."""

    def __init__(self, obj):
        self.obj = obj

    def __getitem__(self, range):
        if not isinstance(range, slice):
            raise Exception("__getitem__ without slicing not supported")
        return self.obj[range]

    def __len__(self):
        return self.obj.count()


class SqlalchemyOrmPage(paginate.Page):
    """A pagination page that deals with SQLAlchemy ORM objects.
    
    See the documentation on paginate.Page for general information on how to work
    with instances of this class."""

    # This class just subclasses paginate.Page which contains all the functionality.
    # It just instantiates the class with a "wrapper_class" argument telling it how the
    # collection can be accessed.
    def __init__(self, *args, **kwargs):
        super(SqlalchemyOrmPage, self).__init__(
            *args, wrapper_class=SqlalchemyOrmWrapper, **kwargs)


def sql_wrapper_factory(db_session=None):
    class SqlalchemySelectWrapper(object):
        """Wrapper class to access elements of an SQLAlchemy SELECT query."""

        def __init__(self, obj):
            self.obj = obj
            self.db_session = db_session

        def __getitem__(self, range):
            if not isinstance(range, slice):
                raise Exception("__getitem__ without slicing not supported")
            # value for offset
            offset_v = range.start
            limit = range.stop - range.start
            select = self.obj.limit(limit).offset(offset_v)
            return self.db_session.execute(select).fetchall()

        def __len__(self):
            return self.db_session.execute(self.obj.alias().count()).scalar()

    return SqlalchemySelectWrapper


class SqlalchemySelectPage(paginate.Page):
    """A pagination page that deals with SQLAlchemy Select objects.
    
    See the documentation on paginate.Page for general information on how to work
    with instances of this class."""

    # This class just subclasses paginate.Page which contains all the functionality.
    # It just instantiates the class with a "wrapper_class" argument telling it how the
    # collection can be accessed.
    def __init__(self, db_session, *args, **kwargs):
        """sqlalchemy_connection: SQLAlchemy connection object"""
        wrapper = sql_wrapper_factory(db_session)
        super(SqlalchemySelectPage, self).__init__(
            *args, wrapper_class=wrapper, **kwargs)
