from dotenv import dotenv_values
from pathlib import Path
path = Path(__file__)
dotfile = path.parent.joinpath('.env').absolute()
config = dotenv_values(dotfile)

default = {
    'drivername': config.get('DB_DRIVER', "postgresql"),
    'database': config.get('DB_DATABASE', "news"),
    'username': config.get('DB_USERNAME', 'news_user'),
    'password': config.get('DB_PASSWORD', 'password'),
    'host': config.get('DB_HOST', 'localhost'),
    'port': config.get('DB_PORT', '5432'),
}
