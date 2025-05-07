#app/scripts/streamlit_dashboard.py
import streamlit as st
import pandas as pd
import calendar
from config.settings import DATABASE_URL
from sqlalchemy import create_engine, text
import logging
from datetime import datetime
import os

# ログディレクトリ作成（なければ）
os.makedirs("logs", exist_ok=True)
log_filename = f"logs/app_{datetime.now().strftime('%Y%m%d')}.log"

# ログ設定（重複ハンドラを防止）
logger = logging.getLogger()
if not logger.hasHandlers():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )

# SQLAlchemyエンジン作成（グローバルに1回だけ）
engine = create_engine(DATABASE_URL)

# --- ページ設定 ---
st.set_page_config(page_title="📊 Supermarket Dashboard", layout="wide")

# --- ページ選択 ---
page = st.sidebar.selectbox("📄 ページを選択", [
    "Sales Summary", "Daily Sales Trend", "Monthly Sales Trend", "Daily Sales Summary"
])


# --- データ取得関数（サマリー） ---
@st.cache_data
def load_summary_data():
    try:
        query = open("query/sales_summary.sql", "r").read()
        df = pd.read_sql_query(query, engine)
        logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ load_summary_data 成功")
        return df
    except Exception as e:
        logging.error(f"[load_summary_data] SQL実行失敗: {e}")
        st.error("データの読み込みに失敗しました。再度お試しください。")
        return pd.DataFrame()

# --- データ取得関数（日別） ---
@st.cache_data
def load_daily_summary():
    try:
        query = open("query/daily_sales_summary.sql", "r").read()
        df = pd.read_sql_query(query, engine)
        df["sale_date"] = pd.to_datetime(df["sale_date"])
        logging.info("✅ 日次サマリーデータ読み込み成功")
        return df
    except Exception as e:
        logging.error(f"❌ 日次サマリーデータ読み込み失敗: {e}")
        st.error("日次サマリーデータの取得に失敗しました。")
        return pd.DataFrame()

@st.cache_data
def load_daily_data():
    try:
        with open("query/sales_by_date.sql", "r") as f:
            query = text(f.read())
        df = pd.read_sql_query(query, engine)
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ load_summary_data 成功")
        return df
    except Exception as e:
        logging.error(f"❌ load_daily_data エラー: {e}")
        return pd.DataFrame()

# --- データ取得関数（月別） ---
@st.cache_data
def load_monthly_data():
    try:
        with open("query/sales_by_month.sql", "r") as f:
            query = text(f.read())
        df = pd.read_sql_query(query, engine)
        df["month"] = pd.to_datetime(df["month"], errors="coerce")
        df_grouped = df.groupby("month", as_index=False).agg({"total_sales": "sum"})
        logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ load_summary_data 成功")
        return df_grouped
    except Exception as e:
        logging.error(f"❌ load_monthly_data エラー: {e}")
        return pd.DataFrame()

# --- Sales Summaryページ ---
if page == "Sales Summary":
    st.title("📊 Supermarket Sales Summary")
    df = load_summary_data()

    # --- サイドバーのフィルター ---
    st.sidebar.header("🔍 フィルター")
    item_options = df["item_name"].dropna().unique()
    selected_items = st.sidebar.multiselect("商品名", item_options, default=item_options)

    min_rank = int(df["sales_rank"].min())
    max_rank = int(df["sales_rank"].max())
    rank_range = st.sidebar.slider("売上ランク", min_rank, max_rank, (min_rank, max_rank))

    # --- フィルター処理 ---
    filtered_df = df[
        (df["item_name"].isin(selected_items)) &
        (df["sales_rank"] >= rank_range[0]) &
        (df["sales_rank"] <= rank_range[1])
    ]

    # --- テーブル表示 ---
    st.subheader("💰 売上サマリー（USD）")
    st.dataframe(
        filtered_df.style.format({
            "total_sales": "${:,.2f}",
            "first_half_sales": "${:,.2f}",
            "second_half_sales": "${:,.2f}",
            "diff": "${:,.2f}"
        }),
        use_container_width=True
    )

    # --- 棒グラフ表示 ---
    st.subheader("📦 商品別の売上")
    bar_data = filtered_df.set_index("item_name")["total_sales"]
    st.bar_chart(bar_data)

# --- Daily Sales Trendページ ---
elif page == "Daily Sales Trend":
    st.title("📈 Daily Sales Trend")
    df_daily = load_daily_data()
    df_daily["month"] = df_daily["date"].dt.month
    months = sorted(df_daily["month"].dropna().unique())
    selected_month = st.selectbox("📅 月を選択", months, format_func=lambda x: calendar.month_name[x])

    filtered_daily = df_daily[df_daily["month"] == selected_month]
    sales_by_date = filtered_daily.groupby("date")["total_sales"].sum()

    st.line_chart(sales_by_date)

# --- Monthly Sales Trendページ ---
elif page == "Monthly Sales Trend":
    st.title("📆 Monthly Sales Trend")
    df_monthly = load_monthly_data()
    df_monthly.set_index("month", inplace=True)
    st.line_chart(df_monthly["total_sales"])

# --- Daily Sales Summaryページ ---
elif page == "Daily Sales Summary":
    st.title("📋 Daily Sales Summary (Last 30 Days)")
    df_summary = load_daily_summary()

    if df_summary.empty:
        st.warning("データが見つかりませんでした。")
    else:
        st.dataframe(
            df_summary.style.format({
                "total_sales": "${:,.2f}"
            }),
            use_container_width=True
        )

