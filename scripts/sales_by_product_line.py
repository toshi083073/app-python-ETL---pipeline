import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
from config.settings import DB_CONFIG

# --- SQL読み込み ---
def load_query(filepath):
    with open(filepath, "r") as f:
        return f.read()

def main():
    print("SQL読み込み中...")
    query = load_query("query/sales_by_product_line.sql")  # 外部SQLから読み込み

    print("DB接続中...")
    conn = psycopg2.connect(**DB_CONFIG)

    print("クエリ実行中...")
    df = pd.read_sql_query(query, conn)
    conn.close()

    print("出力中...")

    # --- CSV保存 ---
    df.to_csv("output/sales_by_product_line.csv", index=False)

    # --- グラフ化（改善版）---
    # 売上高順（昇順）で並べ替え
    df_sorted = df.sort_values('total_sales', ascending=True)

    plt.figure(figsize=(12, 6))
    bars = plt.barh(df_sorted['product_line'], df_sorted['total_sales'], color='skyblue')

    # 金額ラベルを横に表示
    for bar in bars:
        plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, 
                 f'${bar.get_width():,.0f}', va='center', ha='left', fontsize=9)
        

    plt.xlabel('Sales Total (USD)')  # ← 単位を追加
    plt.title('Sales by Product Line (Sorted)')
    plt.tight_layout()

    plt.savefig('output/sales_by_product_line_better.png')
    # plt.show()  # Docker内なのでコメントアウト

    print("完了！🎉")

if __name__ == "__main__":
    main()
