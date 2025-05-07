# 必要なモジュールをインポート
from airflow import DAG  # DAG本体
from airflow.operators.python import PythonOperator  # Python関数をAirflowタスクに使うためのオペレーター
from datetime import datetime, timedelta  # スケジュールとリトライ設定に使用
import psycopg2  # PostgreSQLへの接続用
import csv  # CSVファイル書き出し用

# デフォルトの引数（再試行回数など）
default_args = {
    'owner': 'airflow',
    'retries': 1,  # 失敗した場合1回だけ再試行
    'retry_delay': timedelta(minutes=1),  # 再試行までの待機時間
}

# 実際のデータ出力処理を行う関数（PythonOperatorで実行される）
def export_sales_to_csv():
    # PostgreSQLへ接続
    conn = psycopg2.connect(
        host='postgres',        # コンテナ名（docker-composeのservice名と一致）
        dbname='mydb',          # データベース名
        user='myuser',          # ユーザー名
        password='mypassword',  # パスワード
        port=5432               # ポート番号
    )
    cur = conn.cursor()
    
    # sales テーブルを全件取得
    cur.execute("SELECT * FROM sales")
    rows = cur.fetchall()  # 結果を全件取得
    column_names = [desc[0] for desc in cur.description]  # カラム名を取得
    
    # /tmp に CSV ファイルを書き出し
    with open('/tmp/output/sales_export.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(column_names)  # ヘッダーを書き出す
        writer.writerows(rows)        # データ本体を書き出す
    
    # 接続を閉じる
    cur.close()
    conn.close()

# DAG（ワークフロー）本体
with DAG(
    dag_id='export_sales_to_csv_py',  # DAGのID（Airflow UIに表示される名前）
    default_args=default_args,        # 上で定義した引数を適用
    description='Export sales table to CSV using PythonOperator',
    schedule_interval=None,           # 自動では実行せず、手動トリガーで動く
    start_date=datetime(2025, 5, 1),  # 開始日（過去日付でもOK）
    catchup=False,                    # 過去分のバックフィルを行わない
    tags=['export'],                  # タグ付け（UIでの整理に便利）
) as dag:

    # PythonOperator に処理関数を登録
    export_task = PythonOperator(
        task_id='export_sales_python',        # タスク名
        python_callable=export_sales_to_csv   # 実行する関数
    )
