from sklearn.feature_extraction import DictVectorizer
from sqlalchemy import create_engine, text
from sqlalchemy.engine.url import URL
import settings

database_settings = settings.DB_SETTINGS
engine = create_engine(URL.create(**database_settings))
query = text("""SELECT
        distinct
        outlet
        from outlets
        """)
with engine.connect() as conn:
    conn.execute(query)
