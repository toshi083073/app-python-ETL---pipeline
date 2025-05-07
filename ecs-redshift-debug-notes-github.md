# ECS × Redshift Serverless ETL Task Debug Notes

## ✅ 概要
AWS Fargate を使用して、Redshift Serverless に対して Python スクリプトで S3 → COPY を行う ETL パイプラインの実行検証。

---

## 📌 目的（パイプライン全体の構成）
```text
[S3 Bucket: sales.csv]
      |
      ▼
[ECS Fargate タスク (python scripts/etl_copy_redshift.py)]
      |
      ▼
[Redshift Serverless (COPY from S3)]
```

---

## 📝 使用サービス・ツール一覧

| サービス/ツール         | 用途                                   |
|--------------------------|----------------------------------------|
| ECS Fargate              | ETL実行タスクのコンテナ実行基盤        |
| Redshift Serverless      | ETL後のデータ格納先                    |
| CloudWatch Logs          | ログ出力確認                           |
| Amazon S3                | CSVデータ格納                          |
| IAM Role (Redshift COPY) | COPY権限付き IAM ロール                 |
| Terraform                | 今後 IaC 管理予定（準備中）           |

---

## ⚠️ 現時点の問題点・注意点（ハマった内容まとめ）

### 1. ❌ COPY failed: Connection timed out
- 原因：ECSタスクとRedshift Serverlessが **同一VPC/Subnet** に存在していないか、**適切なセキュリティグループ設定がなされていない**
- 対応：Redshift Serverless 側の `vpcEndpoints -> subnetId` に ECS Fargate タスクと同じ subnet を指定
  - 今回の private IP: `172.31.21.102` / Subnet: `subnet-05c5b84561074d252`

### 2. ❓ enableExecuteCommand の指定場所に注意
- `task-definition` JSON には `enableExecuteCommand` は指定不可 → `aws ecs run-task` CLI 時に `--enable-execute-command` で明示
- 間違えて JSON に記述 → `Unknown parameter in input: "enableExecuteCommand"` エラー

### 3. 🔍 CloudWatch Logs に出力されない問題
- 原因候補：
  - `awslogs-group` の作成が事前にされていない
  - タスク定義内で `logConfiguration` が不足
  - ECS タスクの IAM ロールに `logs:PutLogEvents` 権限がない
- 解決策：
  - `aws logs create-log-group` で手動作成
  - `ecsTaskExecutionRole` に以下のポリシー確認：
    ```json
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "*"
    }
    ```

### 4. 🐳 Dockerfile のベースイメージと OS
- Redshift Serverless との互換性のため `python:3.11-slim` や `debian-slim` 系の **Linux/X86_64** を使用
- ECS/Fargate 上で動作するため、軽量で root 書き込みが可能な構成に

### 5. ⌛ タスクが途中終了する問題への一時対処
- `command` に `sleep 3600` を指定して **対話セッション中にタイムアウトしないように** している

---

## 🗂 コードコメントに残すべきメモ（例）

```jsonc
{
  // [MEMO] enableExecuteCommand フラグは aws ecs run-task 時に指定する必要あり。
  // JSON上では未対応（aws CLI v2以降でCLIオプションで指定）

  "family": "redshift-etl-task",
  "networkMode": "awsvpc",
  ...
}
```

---

## ✅ 今後の対応TODO

- [ ] Terraform による Redshift Serverless / S3 / ECS 定義の IaC 管理化
- [ ] CloudWatch Logs の安定確認（自動作成含む）
- [ ] taskRole に最低限の IAM ポリシー設計
- [ ] S3 → Redshift COPY 完了時のバリデーション出力の強化
- [ ] ECS タスク失敗時の通知（SNSなど）の仕組み
- [ ] Python スクリプトのログ出力整備（info, error）

---

*作成日: 2025-05-04*