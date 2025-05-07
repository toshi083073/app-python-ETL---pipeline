import pandas as pd
import psycopg2
from config.settings import DB_CONFIG

def main():
    print("データ読み込み中...")
    conn = psycopg2.connect(**DB_CONFIG)
    df = pd.read_sql_query("SELECT * FROM supermarket_sales", conn)
    conn.close()

    print("\n📌 欠損値チェック:")
    print(df.isnull().sum())

    print("\n📌 異常値チェック（例: 負の金額や0以下の数量など）")
    print(df[df['quantity'] <= 0])
    print(df[df['unit_price'] < 0])
    print(df[df['sales_total'] < 0])

    print("\n📌 概要統計:")
    print(df.describe())

if __name__ == "__main__":
    main()
