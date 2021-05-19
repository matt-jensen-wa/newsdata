drop function if exists news.fn_svd;
create function news.fn_svd()
returns table (
    outlet text
    ,total integer
    ,label integer
    ,first numeric
    ,second numeric
    ,third numeric
)
as $body$

import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn.feature_extraction.text import TfidfTransformer, HashingVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans

def model(df):
    hasher = HashingVectorizer(n_features=100, analyzer='word', stop_words='english', alternate_sign=False, norm=None)
    vectorizer = make_pipeline(hasher, TfidfTransformer(use_idf=False))
    X = vectorizer.fit_transform(df['links'])
    normalizer = Normalizer(copy=False)
    svd = TruncatedSVD(n_components=12)
    lsa = make_pipeline(svd, normalizer)
    Y = lsa.fit_transform(X)
    km = KMeans(n_clusters=30, init='k-means++', max_iter=1000, n_init=1)
    km.fit(Y)
    plpy.notice(df)
    for i, (idx, row) in enumerate(df.iterrows()):
        plpy.notice(row.index)
        yield [
                row.index
                ,row['total'] # total links
                ,km.labels_[i] # cluster label
                ,Y[i][1] # svd 1
                ,Y[i][2] # svd 2
                ,Y[i][3] # svd 3
            ]

query = """
with news as (
    select distinct 
        base_url as outlet
        ,case when parent_url is null then url else parent_url end as link
    from news
    where parent_url is not null
    and (parent_url is not null or url is not null)
    and base_url is not null
    and published_at between '2016-01-01'::date and '2017-01-01'::date
)
select
    outlet
    ,string_agg(link, '\n') as links
    ,count(1) as total
from news
group by outlet
"""

result = plpy.execute(query)
df = pd.DataFrame.from_records(result, columns=['outlet', 'links', 'total'], index=['outlet'])
return model(df)

$body$ language plpython3u;

drop table if exists news.outlet_svd;
create table news.outlet_svd as
select * from news.fn_svd();
alter table news.outlet_svd owner to news_user;
