from setuptools import setup, find_packages

setup(
    name='newsdata',
    version='0.0.3',
    description='This is a working setup.py',
    url='http://news.abumni.com',
    author='Matt',
    author_email='matt@abumni.com',
    packages = ['app','scraper'],
    install_requires=[
        'psycopg2'
        ,'python-dotenv'
        ,'Scrapy'
        ,'SQLAlchemy'
        ,'Twisted'
        ,'pandas'
        ,'matplotlib'
        ,'sklearn'
        ,'numpy'
        ,'nltk'
        ,'Flask'
    ],
    zip_safe=False
)
