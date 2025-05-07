import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
from config.settings import DB_CONFIG  # ← 追加

def load_query(filepath):
    with open(filepath, "r") as f:
        return f.read()

def extract_data():
    """DBからデータを抽出"""
    query = load_query("query/sales_daily.sql")  # ← SQLファイルを外部化
    conn = psycopg2.connect(**DB_CONFIG)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def transform_and_save(df):
    """加工してCSVとグラフ保存"""
    df.to_csv('output/sales_pipeline_summary.csv', index=False)  # ← 出力先をoutput/に

    # グラフ保存（複合グラフ）
    fig, ax1 = plt.subplots(figsize=(14, 6))
    ax1.bar(df['sale_date'], df['total_daily_sales'], color='skyblue', label='Total Sales')
    ax1.set_xlabel('Sale Date')
    ax1.set_ylabel('Total Sales', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    plt.xticks(rotation=45)

    ax2 = ax1.twinx()
    ax2.plot(df['sale_date'], df['sales_count'], color='red', marker='o', label='Sales Count')
    ax2.set_ylabel('Sales Count', color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    plt.title('Daily Sales Amount and Sales Count')
    fig.tight_layout()
    plt.savefig('output/sales_pipeline_graph.png')

def main():
    print("データ抽出開始...")
    df = extract_data()
    print("データ抽出完了。件数:", len(df))
    
    print("データ加工＆保存開始...")
    transform_and_save(df)
    print("パイプライン処理完了！🎉")

if __name__ == "__main__":
    main()
