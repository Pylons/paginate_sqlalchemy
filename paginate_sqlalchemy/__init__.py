# Copyright (c) 2007-2012 Christoph Haas <email@christoph-haas.de>
# See the file LICENSE for copying permission.

"""Enhances the paginate.Page class to work with SQLAlchemy objects"""

import sys
import paginate
import sqlalchemy

class SqlalchemyOrmWrapper(object):
    """Wrapper class to access elements of a collection."""
    def __init__(self, obj):
        if type(obj) is not sqlalchemy.orm.query.Query:
            raise TypeError("Only sqlalchemy.orm.query.Query type objects are supported. "
                            "Yours is of type {0}".format(type(obj)))

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
        super(SqlalchemyOrmPage, self).__init__(*args, wrapper_class=SqlalchemyOrmWrapper, **kwargs)

