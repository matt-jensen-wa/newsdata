from flask import (
    Flask, send_file, request, redirect, url_for
)
from sqlalchemy import create_engine, text
from sqlalchemy.engine.url import URL
import numpy as np
import pandas as pd
from numpy import int64, int32, float64
from scraper import settings
from io import BytesIO
from PIL import Image, ImagePalette
import matplotlib.pyplot as plt
from app.model import svd
from app.config import database
from psycopg2.extensions import register_adapter, AsIs
import psycopg2
import json
import os


app = Flask(
    __name__,
    static_folder = 'resources'
)

def resource_path(filename):
    import os
    absolutepath = os.path.abspath(__file__)
    fileDirectory = os.path.dirname(absolutepath)
    return fileDirectory + '/resources/' + filename

@app.route("/")
def index():
    return """
        <html>
            <head>
                <title>{{ title }} - image</title>
            </head>
            <body>
                <img src='/image/plot?x=first&y=second&static=true&cache=false' alt='Image Placeholder' height='100'>
                <img src='/image/plot?x=first&y=third&static=true&cache=false' alt='Image Placeholder' height='100'>
                <img src='/image/plot?x=second&y=third&static=true&cache=false' alt='Image Placeholder' height='100'>
                <div>
                    <a href='/svd/refresh'>Refresh Outlet SVD Transformation</a>
                </div>
            </body>
        </html>
    """


@app.route("/svd/refresh")
def refresh():
    engine = create_engine(URL.create(**database.default))
    data = svd.model(svd.data())
    with engine.connect() as conn:
        data.to_sql('outlet_svd', conn, schema='news', if_exists='replace', index=False)
    return redirect(url_for('index'))

@app.route("/image/plot")
def plot():
    x = request.args.get('x', 'first')
    y = request.args.get('y', 'second')
    static = request.args.get('static')
    cache = request.args.get('cache', True, type=json.loads)
    filename = 'plot_{}_{}.png'.format(x, y)

    if not cache or not os.path.exists(resource_path(filename)):
        label = request.args.get('label', 'outlet')
        database_settings = settings.DB_SETTINGS
        engine = create_engine(URL.create(**database_settings))
        query = text("""
            select
                outlet
                ,labels
                ,case :x 
                    when 'first' 
                    then first 
                    when 'second' 
                    then second 
                    else third 
                end as x
                ,case :y 
                    when 'first' 
                    then first 
                    when 'second' 
                    then second 
                    else third 
                end as y
                ,total as total
            from news.outlet_svd
            where outlet is not null
        """)
        with engine.connect() as conn:
            params={'x': x, 'y':y}
            df = pd.read_sql_query(query, conn, params=params)

        #df.set_index('label')
        fig, ax = plt.subplots()
        ax.scatter(x=df['x'], y=df['y'], s=df['total'], c=df['labels'], cmap=plt.cm.RdBu)
        df['range'] = np.abs((df['y'] - np.mean(df['y']))/np.std(df['y']))
        labels = df[df.range > 2.]
        for i, row in labels.iterrows():
            ax.text(x=row.loc['x']+0.3
                        ,y=row.loc['y']+0.3
                        ,s=row.loc['outlet']
                        ,fontdict=dict(color='red',size=10)
                    )

        ax.set(xlabel=x, ylabel=y,
                        title='plot of {0} vs {1} component of svd'.format(x, y))
        ax.grid()
        fig.savefig(resource_path(filename), format='png')

    return app.send_static_file(filename)
