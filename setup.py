from setuptools import setup, find_packages

import sys, os

setup(
    name='paginate_sqlalchemy',
    version='0.3.0',
    description="Extension to paginate.Page that supports SQLAlchemy queries",
    long_description="""
        This module helps divide up large result sets into pages or chunks.
        The user gets displayed one page at a time and can navigate to other pages.
        It is especially useful when developing web interfaces and showing the
        users only a selection of information at a time.

        This module uses and extends the functionality of the paginate module to
        support SQLAlchemy queries.
        """,

    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    keywords='pagination paginate sqlalchemy',
    author='Christoph Haas',
    author_email='email@christoph-haas.de',
    maintainer='Luke Crooks',
    maintainer_email='luke@pumalo.org',
    install_requires=[
        "sqlalchemy>=0.8.3",
        "paginate>=0.4"
        ],
    url='https://github.com/Pylons/paginate_sqlalchemy',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points=""" """,
)
