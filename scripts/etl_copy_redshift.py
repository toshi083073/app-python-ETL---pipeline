import psycopg2
import os
from dotenv import load_dotenv
from urllib.parse import urlparse


load_dotenv()  # .envファイルから環境変数を読み込む

# [TROUBLESHOOT] Redshift Serverless への COPY 実行時にタイムアウト
# - IAM Role OK、S3 OK でも接続不可になるケースあり
# - 原因: VPC/SG のアクセス許可不足（TCP:5439）

# Redshift endpoint:
# default-workgroup.802190220015.ap-northeast-1.redshift-serverless.amazonaws.com:5439


# Redshift 接続情報をパース
url = urlparse(os.getenv("REDSHIFT_DATABASE_URL", ""))

DATABASE_URL = url
IAM_ROLE = os.getenv("REDSHIFT_IAM_ROLE_ARN")
S3_PATH = os.getenv("S3_SOURCE_PATH")

print("🚀 Script started")

def main():
    print("🟡 Starting COPY process...")
    if not IAM_ROLE or not S3_PATH:
        print("❌ IAM_ROLE or S3_PATH is not set. Skipping COPY.")
        return

    print("IAM_ROLE =", IAM_ROLE)
    print("S3_PATH =", S3_PATH)

    # psycopg2で直接接続するため、DATABASE_URL を分解
    try:

        conn = psycopg2.connect(
            host=url.hostname,
            port=url.port,
            dbname=url.path.lstrip("/"),
            user=url.username,
            password=url.password,
        )

        cur = conn.cursor()

        copy_sql = f"""
        COPY sales
        FROM '{S3_PATH}'
        IAM_ROLE '{IAM_ROLE}'
        FORMAT AS CSV
        IGNOREHEADER 1;
        """

        cur.execute(copy_sql)
        conn.commit()
        print("✅ COPY succeeded.")
    except Exception as e:
        print("❌ COPY failed:", e)
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main()
