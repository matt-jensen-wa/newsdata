from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction import DictVectorizer
from sklearn.decomposition import TruncatedSVD, SparsePCA
from sqlalchemy import create_engine, text
from sqlalchemy.engine.url import URL
from news import settings
import pandas as pd

database_settings = settings.DB_SETTINGS
engine = create_engine(URL.create(**database_settings))
query = text("""
with news as (
    select distinct 
        regexp_replace(regexp_replace(regexp_replace(outlet_url, '^https?\:\/\/', ''), '^www\.', ''), '\/$', '') as outlet
        ,case when parent_url is null then url else parent_url end as link
    from news
)
select
    outlet
    ,json_object_agg(link, 1) as links
    ,count(1) as total
from news
where link is not null
group by outlet
""")
with engine.connect() as conn:
    df = pd.read_sql_query(query, conn)

vec = DictVectorizer()
#vec = CountVectorizer()
X = vec.fit_transform(df['links'])
print(X)
decomp = TruncatedSVD(n_components=3)
#decomp = SparsePCA(n_components=3)
#decomp.fit_transform(X)
out = decomp.fit_transform(X)
df['first'] = [x[0] for x in out]
df['second'] = [x[1] for x in out]
df['third'] = [x[2] for x in out]
with engine.connect() as conn:
    df[['outlet', 'first', 'second', 'third', 'total']].to_sql(name='outlet_svd', con=conn, if_exists='replace', chunksize=1000)
