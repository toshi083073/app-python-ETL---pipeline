import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
from config.settings import DB_CONFIG

# SQL読み込み
def load_query(filepath):
    with open(filepath, "r") as f:
        return f.read()

# データ抽出
def extract_data():
    conn = psycopg2.connect(**DB_CONFIG)
    query = load_query("query/supermarket_sales_pipeline.sql")
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# データ加工＆保存
def transform_and_save(df):
    df.to_csv("output/supermarket_sales_summary.csv", index=False)

    plt.figure(figsize=(12, 6))
    plt.plot(df["sale_date"], df["daily_sales"], marker='o', color='green')
    plt.title("Daily Sales Trend")
    plt.xlabel("Sale Date")
    plt.ylabel("Total Sales")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("output/supermarket_sales_graph.png")

# メイン処理
def main():
    print("データ抽出開始...")
    df = extract_data()
    print("抽出完了！件数:", len(df))

    print("加工・保存中...")
    transform_and_save(df)
    print("完了！🎉")

if __name__ == "__main__":
    main()
