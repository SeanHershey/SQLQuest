import os
import dotenv
from sqlalchemy import create_engine

def database_connection_url():
    dotenv.load_dotenv()
    # TODO: PASSWORD!
    return os.environ.get("postgres://postgres.gnutkhzhvufdmnveqcgc:[YOUR-PASSWORD]@aws-0-us-west-1.pooler.supabase.com:5432/postgres")

engine = create_engine(database_connection_url(), pool_pre_ping=True)