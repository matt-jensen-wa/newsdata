drop table if exists public.news;
create table if not exists public.news (
    url text
    ,title text
    ,description text
    ,author text
    ,outlet text
    ,outlet_url text
    ,parent_url text
    ,published_at timestamp
    ,type text
    ,scraped_at timestamp
    ,scraped_url text
)
