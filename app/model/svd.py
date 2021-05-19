import pandas as pd
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn.feature_extraction.text import TfidfTransformer, HashingVectorizer, CountVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans
from nltk.tokenize import RegexpTokenizer
import matplotlib.pyplot as plt
from io import BytesIO

def data():
    from sqlalchemy import create_engine, text
    from sqlalchemy.engine.url import URL
    from scraper import settings
    from app.config import database

    #database_settings = settings.DB_SETTINGS
    #engine = create_engine(URL.create(**database_settings))
    engine = create_engine(URL.create(**database.default))
    query = text("""
        with news as (
            select distinct 
                base_url as outlet
                ,parent_url as link
            from news
            where published_at between '2016-01-01'::date and '2017-01-01'::date
            and parent_url is not null
        )
        select
            outlet
            ,string_agg(link, ' ') as links
            ,count(1) as total
        from news
        where link is not null
        group by outlet
        order by total desc
    """)
    with engine.connect() as conn:
        df = pd.read_sql_query(query, conn)
    return df

def model(df):
    #hasher = HashingVectorizer(n_features=100, analyzer='word', stop_words='english', alternate_sign=False, norm=None)
    hasher = CountVectorizer(analyzer='word', stop_words='english')
    vectorizer = make_pipeline(hasher, TfidfTransformer(use_idf=False))
    X = vectorizer.fit_transform(df['links'])
    print(hasher.get_params())
    normalizer = Normalizer(copy=False)
    svd = TruncatedSVD(n_components=12)
    lsa = make_pipeline(svd, normalizer)
    Y = lsa.fit_transform(X)
    km = KMeans(n_clusters=4, init='k-means++', max_iter=1000, n_init=1)
    Z = km.fit_predict(Y)
    df['labels'] = Z
    df['first'] = Y[:,0]
    df['second'] = Y[:,1]
    df['third'] = Y[:,2]
    
    result = df[['outlet', 'total', 'labels', 'first', 'second', 'third']]
    return result

    # for i, (idx, row) in enumerate(df.iterrows()):
    #     yield [str(idx) # outlet
    #             ,row['total'] # total links
    #             ,km.labels_[i] # cluster label
    #             ,Y[i][1] # svd 1
    #             ,Y[i][2] # svd 2
    #             ,Y[i][3] # svd 3
    #         ]
