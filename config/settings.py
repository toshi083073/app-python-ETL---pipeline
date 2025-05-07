# config/settings.py

from sqlalchemy.engine import URL
from dotenv import load_dotenv
import os

load_dotenv()

# 接続先の切り替え（local / redshift）
db_target = os.getenv("DB_TARGET", "local").lower()

if db_target == "redshift":
    DATABASE_URL = URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv("REDSHIFT_USER"),
        password=os.getenv("REDSHIFT_PASSWORD"),
        host=os.getenv("REDSHIFT_HOST"),
        port=int(os.getenv("REDSHIFT_PORT", 5439)),
        database=os.getenv("REDSHIFT_DB")
    )
    IAM_ROLE = os.getenv("REDSHIFT_IAM_ROLE_ARN")
    S3_PATH = os.getenv("S3_SOURCE_PATH")

else:  # local
    DATABASE_URL = URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv("LOCAL_DB_USER"),
        password=os.getenv("LOCAL_DB_PASSWORD"),
        host=os.getenv("LOCAL_DB_HOST"),
        port=int(os.getenv("LOCAL_DB_PORT", 5432)),
        database=os.getenv("LOCAL_DB_NAME")
    )
    IAM_ROLE = None
    S3_PATH = None
