from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
from config.settings import DATABASE_URL
import pandas as pd
import logging

# --- ログ設定 ---
today_str = datetime.now().strftime("%Y%m%d")  # ← 修正: datetime.date → datetime
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(f"logs/daily_batch_{today_str}.log"),
        logging.StreamHandler()
    ]
)

# --- 接続設定 ---
engine = create_engine(DATABASE_URL)
yesterday = datetime.now().date() - timedelta(days=1)  # ← datetime.date型


# SQL（キャストなしに）
query = text("""
    SELECT
        :yesterday AS sale_date,
        item_name,
        SUM(price * quantity) AS total_sales
    FROM sales
    WHERE sale_date = :yesterday
    GROUP BY item_name
""")

insert_sql = text("""
    INSERT INTO daily_sales_summary (sale_date, item_name, total_sales)
    VALUES (:sale_date, :item_name, :total_sales)
""")

delete_sql = text("""
    DELETE FROM daily_sales_summary WHERE sale_date = :yesterday
""")

# --- 処理実行 ---
try:
    with engine.begin() as conn:
        # 削除（既存データをクリア）
        conn.execute(delete_sql, {"yesterday": yesterday})
        logging.info(f"🧹 {yesterday} の既存データを削除しました")

        # データ抽出
        df = pd.read_sql(query, engine, params={"yesterday": yesterday})
        logging.info("✅ 日次売上集計に成功しました")
        logging.info(f"\n{df}")

        # データ挿入
        for _, row in df.iterrows():
            conn.execute(insert_sql, {
                "sale_date": row["sale_date"],
                "item_name": row["item_name"],
                "total_sales": row["total_sales"]
            })
        logging.info(f"📥 {len(df)} 件のデータを保存しました")

except Exception as e:
    logging.error(f"❌ 日次集計に失敗しました: {e}")
