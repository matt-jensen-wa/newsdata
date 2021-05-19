begin;
create schema if not exists news;

create table news.outlets (
    base_url text
    ,article_links integer
    ,first_published_at timestamp
    ,last_published_at timestamp
);
insert into news.outlets (
    base_url
    ,article_links
    ,first_published_at
    ,last_published_at
)
select
    base_url
    ,count(distinct parent_url) as article_links
    ,min(published_at) as first_published_at
    ,max(published_at) as last_published_at
from news
group by
    base_url
;
create unique index if not exists outlets_base_url_uniq_idx on news.outlets (base_url);
alter table news add foreign key (base_url) references news.outlets;
select
*
from news.outlets
order by article_links desc
limit 50;
rollback;
