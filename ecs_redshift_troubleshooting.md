
# ECS Fargate + Redshift Serverless Troubleshooting Log

## ✅ 現在のステータス

- ECS タスク起動と `execute-command` 接続は成功。
- `etl_copy_redshift.py` 実行ログ確認済（CloudWatch）。
- Redshift Serverless 側への接続失敗（タイムアウト）。

---

## ❗️未解決のネットワーク関連の問題

### 問題1: Redshift Serverless への接続タイムアウト

**エラーメッセージ**:
```
❌ COPY failed: connection to server at "default-workgroup.***.redshift-serverless.amazonaws.com", port 5439 failed: Connection timed out
Is the server running on that host and accepting TCP/IP connections?
```

**原因と解決策**:
- ✅ Redshift Serverless は VPC 内にある → Fargate タスクも同一 VPC に配置する必要あり（OK）
- 🔍 **Security Group のインバウンドルールに TCP 5439 が許可されていない可能性**
  - 対応: Redshift 側の ENI に関連づいた SG に **TCP 5439 の許可**を追加
- 🔍 **Redshift Serverless 側の VPC ルーティング設定不備**
  - 対応: `enhancedVpcRouting = false` のままで OK（確認済）

---

### 問題2: CloudWatch Logs が表示されない（場合がある）

**確認済ログ出力の例**:
```
2025-05-03T13:58:06.103Z Fargate task started
2025-05-03T14:00:17.580Z Fargate task finished
```

**原因と解決策**:
- ✅ `awslogs-group`, `awslogs-stream-prefix` は正しく設定済
- 🔍 ECS ロールに CloudWatch Logs への書き込み権限が不足していた場合、出力されない可能性
  - 対応: `AmazonECSTaskExecutionRolePolicy` アタッチ済みロール使用（OK）

---

## 📝 補足情報・注意点

- `task-definition.json` に `enableExecuteCommand` は **記述不可**
  - `aws ecs run-task` 実行時の `--enable-execute-command` で有効化する必要あり
- `command`: `["sh", "-c", "sleep 3600 && python scripts/etl_copy_redshift.py"]` のようにタスク強制終了防止のために `sleep` を先頭に追加
- `Dockerfile` ベースイメージは **`python:3.11-slim` (Linux/x86_64)** を使用
- Terraform にて S3, Redshift, IAM ロールの構成管理を行っている（`terraform-s3-demo/`）

---

## 🔄 再開ポイント（ToDo）

- [ ] Redshift ENI に関連付く SG に TCP:5439 を許可（Inbound）
- [ ] `.env.fargate` の `REDSHIFT_*` 接続情報を再確認
- [ ] `etl_copy_redshift.py` を ECS 上で再実行
- [ ] 成功ログを CloudWatch Logs にて確認
- [ ] Terraform に SG 修正を反映（必要に応じて）

---

## 🔧 システム構成（簡易図）

```txt
[S3 Bucket] ---> [Fargate Task] ---> [Redshift Serverless]
                    | exec
                    |-----> CloudWatch Logs
```

---

**作成日**: 2025-05-04  
**作成者**: ChatGPT (AWSログ収集支援)
