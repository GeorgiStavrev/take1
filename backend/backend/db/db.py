from sqlalchemy import create_engine
from backend.db.db_config import host, port, db_name, user, password

db_url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}"
engine = create_engine(db_url)
