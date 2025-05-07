import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
from config.settings import DB_CONFIG  # ← 追加

# SQL読み込み関数
def load_query(filepath):
    with open(filepath, "r") as f:
        return f.read()

def main():
    print("SQL読み込み中...")
    query = load_query("query/sales_summary.sql")  # ← 外部SQLファイル

    print("DB接続中...")
    conn = psycopg2.connect(**DB_CONFIG)

    print("クエリ実行中...")
    df = pd.read_sql_query(query, conn)
    conn.close()

    print("出力中...")
    df.to_csv("output/sales_summary.csv", index=False)

    # グラフ化
    plt.figure(figsize=(12, 6))
    plt.bar(df['item_name'], df['total_sales'], color='skyblue')
    plt.title('Top 10 Items by Total Sales')
    plt.xlabel('Item Name')
    plt.ylabel('Total Sales')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('output/sales_summary_graph.png')

    print("完了！🎉")

if __name__ == "__main__":
    main()
