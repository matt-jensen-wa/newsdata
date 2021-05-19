begin;

create table news.outlets (
    id biginteger primary key
    ,name text
    ,url text
);
create table news.articles (
    id biginteger primary key
    ,outlet_id biginteger references news.outlets(id)
    ,title text
    ,description text
    ,published_at timestamp
);

create table news.article_references (
    source_id biginteger references news.articles(id)
    destination_id biginteger references news.articles(id)
);

insert into news.references
select *
from insert_articles
