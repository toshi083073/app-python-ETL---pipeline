FROM python:3.11-slim

# 必須パッケージのインストール
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    fonts-noto-cjk

# Pythonライブラリのインストール（dotenv追加）
RUN pip install \
    pandas \
    matplotlib \
    psycopg2 \
    jupyterlab \
    seaborn \
    streamlit \
    sqlalchemy \
    python-dotenv

# 作業ディレクトリ
WORKDIR /app

# プロジェクト全体をコピー
COPY . /app

# デフォルトでは何も起動せず（docker-composeで制御）
CMD ["tail", "-f", "/dev/null"]
