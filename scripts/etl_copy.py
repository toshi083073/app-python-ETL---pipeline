#etl_copy.py
from sqlalchemy import create_engine, text
from config.settings import DATABASE_URL, IAM_ROLE, S3_PATH

def main():
    print("🟡 Starting COPY process...")
    if not IAM_ROLE or not S3_PATH:
        print("❌ IAM_ROLE or S3_PATH is not set. Skipping COPY.")
        return

    copy_sql = f"""
    COPY sales
    FROM '{S3_PATH}'
    IAM_ROLE '{IAM_ROLE}'
    FORMAT AS CSV
    IGNOREHEADER 1;
    """
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            conn.execute(text(copy_sql))
            print("✅ COPY succeeded.")
    except Exception as e:
        print("❌ COPY failed:", e)

if __name__ == "__main__":
    main()
