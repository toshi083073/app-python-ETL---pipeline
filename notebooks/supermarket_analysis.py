#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import psycopg2

# 接続設定
conn = psycopg2.connect(
    host="postgres",
    port=5432,
    dbname="mydb",
    user="myuser",
    password="mypassword"
)

# データ読み込み
df = pd.read_sql_query("SELECT * FROM supermarket_sales", conn)
conn.close()

# 確認
df.head()


# In[3]:


import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import seaborn as sns

conn = psycopg2.connect(
    host="postgres",
    port=5432,
    dbname="mydb",
    user="myuser",
    password="mypassword"
)
df = pd.read_sql_query("SELECT * FROM supermarket_sales", conn)
conn.close()
df.head()


# In[4]:


df.isnull().sum()


# In[5]:


df[df['quantity'] <= 0]
df[df['unit_price'] <= 0]
df[df['sales_total'] <= 0]


# In[6]:


df.describe()


# In[7]:


df['sales_total'].sum()


# In[8]:


df.groupby('product_line')['sales_total'].sum().sort_values(ascending=False)


# In[11]:


import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.family'] = 'Noto Sans CJK JP'  # ← 日本語フォントを指定

plt.figure(figsize=(10, 6))
sns.barplot(data=df, x='sales_total', y='product_line', estimator=sum, ci=None)
plt.title('売上高 by Product Line')
plt.xlabel('Sales Total')
plt.ylabel('Product Line')
plt.tight_layout()
plt.show()


# In[12]:


import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# 日本語フォント指定（DockerでNoto Sansを入れている前提）
plt.rcParams['font.family'] = 'Noto Sans CJK JP'

# 日付をdatetime型に変換
df['date'] = pd.to_datetime(df['date'])

# 日別売上集計
daily = df.groupby('date')['sales_total'].sum().reset_index()

# 折れ線グラフの描画
plt.figure(figsize=(12, 6))
sns.lineplot(data=daily, x='date', y='sales_total')
plt.title('日別売上推移')
plt.xlabel('日付')
plt.ylabel('売上高')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# In[ ]:




