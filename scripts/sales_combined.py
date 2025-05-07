import pandas as pd
import psycopg2
import matplotlib.pyplot as plt

# PostgreSQL接続
conn = psycopg2.connect(
    host="postgres",
    port=5432,
    dbname="mydb",
    user="myuser",
    password="mypassword"
)

# 📋 売上＋件数を取得するSQL
query = """
SELECT
  sale_date,
  SUM(price * quantity) AS total_daily_sales,
  COUNT(*) AS sales_count
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
fig, ax1 = plt.subplots(figsize=(14, 6))

# 売上金額（棒グラフ）
ax1.bar(df['sale_date'], df['total_daily_sales'], color='skyblue', label='Total Sales')
ax1.set_xlabel('Sale Date')
ax1.set_ylabel('Total Sales', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
plt.xticks(rotation=45)

# 件数（折れ線グラフ）右軸
ax2 = ax1.twinx()
ax2.plot(df['sale_date'], df['sales_count'], color='red', marker='o', label='Sales Count')
ax2.set_ylabel('Sales Count', color='red')
ax2.tick_params(axis='y', labelcolor='red')

# グラフタイトル
plt.title('Daily Sales Amount and Sales Count')

# レイアウト調整と保存
fig.tight_layout()
plt.savefig('sales_combined_graph.png')
# plt.show()  # Dockerなら画像保存して確認
# =============================================
