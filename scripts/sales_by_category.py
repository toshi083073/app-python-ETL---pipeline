import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
from config.settings import DB_CONFIG

def main():
    print("SQL読み込み中...")
    with open("query/sales_by_category.sql", "r") as f:
        query = f.read()

    print("DB接続中...")
    conn = psycopg2.connect(**DB_CONFIG)

    print("クエリ実行中...")
    df = pd.read_sql_query(query, conn)
    conn.close()

    print("CSV出力...")
    df.to_csv("output/sales_by_category.csv", index=False)

    print("グラフ生成中...")
    plt.figure(figsize=(12, 6))
    plt.bar(df['product_line'], df['total_sales'], color='orange')
    plt.title("Sales by Product Line")
    plt.xlabel("Product Line")
    plt.ylabel("Total Sales")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("output/sales_by_category_graph.png")

    print("完了！🎉")

if __name__ == "__main__":
    main()
