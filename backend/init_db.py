import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from backend.db.db_config import host, port, db_name_backend, user, password

print("host", host, "port", port, "db-name", db_name_backend)
con = psycopg2.connect(
    dbname="postgres", user=user, host=host, port=port, password=password
)

con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

cur = con.cursor()
try:
    cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name_backend)))
except Exception as ex:
    print(ex)
