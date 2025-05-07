import pandas as pd
import psycopg2
import matplotlib.pyplot as plt

# PostgreSQL接続設定
conn = psycopg2.connect(
    host="postgres",
    port=5432,
    dbname="mydb",
    user="myuser",
    password="mypassword"
)

# 📋 売上推移用クエリ（NEW）
query = """
SELECT
  sale_date,
  SUM(price * quantity) AS total_daily_sales
FROM
  sales
GROUP BY
  sale_date
ORDER BY
  sale_date;
"""

# データ取得
df = pd.read_sql_query(query, conn)

# コネクションを閉じる
conn.close()

# データ確認
print(df.head())

# ================= グラフ作成 =================
plt.figure(figsize=(14, 6))
plt.plot(df['sale_date'], df['total_daily_sales'], marker='o')
plt.title('Daily Sales Trend')
plt.xlabel('Sale Date')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig('sales_trend_graph.png')  # ← グラフを画像保存
# plt.show()  # ← ローカル環境なら表示、Dockerなら画像ファイルで確認
# =============================================
