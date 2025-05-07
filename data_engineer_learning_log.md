
# 📈 1000万円データエンジニアを目指す学習ロードマップ進捗記録

## 🎯 目標
- 半年以内に年収1000万円相当のスキル・実績を持つデータエンジニアになる

---

## ✅ 達成済みステージ一覧

### Week 1–4: Python, Pandas, SQL 基礎
- Python文法習得・関数・リスト内包表記
- Pandasによるデータフレーム操作・groupby、merge、pivot
- SQL基礎（SELECT, JOIN, GROUP BY, WINDOW関数）

### Week 5–6: データ可視化とEDA
- matplotlib, seabornによる単変量・多変量分析
- カテゴリ別分布・ヒートマップ・相関分析

### Week 7–8: Streamlit ダッシュボード開発
- 日次売上ダッシュボード（カテゴリ別、支店別）
- ページ切り替え機能と月別絞り込みUI
- SQLAlchemy + try-except + logging による安定化

### Week 9–10: AWSとRedshift連携
- AWSアカウント再確認・VPC構成理解
- Redshift Serverless + COPYコマンド動作検証
- ECS + Fargate + S3 + Python ETLバッチ起動まで完了

---

## 🚧 現在のステージ（Week 11–12）

### AWS Fargate + TerraformによるIaC化
- ECSクラスタ定義（手動 → `.tf` 管理へ移行予定）
- Task定義・VPC/SG/サブネット・S3 IAMロール自動化
- Redshift用 Secrets Manager 利用検討

---

## 🧠 引き継ぎメモ・再開ポイント（次のステップ）

- [ ] Redshift Serverless ↔ Fargate ネットワーク通信の安定化
    - サブネット/VPCエンドポイント設定精査
    - DNS解決とセキュリティグループのアウトバウンド開放
- [ ] Terraform `main.tf` のリファクタリングとコメント整備
- [ ] ECSバッチのスケジューリング（EventBridge連携）
- [ ] Airflow もしくは Step Functions への移行検討
- [ ] GitHubへの進捗記録、READMEに構成図と技術選定理由を反映

---

## 📂 関連ファイル

- `ecs_redshift_troubleshooting.md`: ETLトラブル対応まとめ
- `streamlit_dashboard.py`: ダッシュボード可視化コード
- `terraform-s3-demo/`: IaC 構成テンプレート
- `scripts/etl_copy_redshift.py`: Redshiftバッチ起動スクリプト
