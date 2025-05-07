#!/bin/bash

echo "🔽 すべてのコンテナを停止・削除します..."
docker compose down

echo "🚀 本番モードでコンテナを起動します..."
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

echo "📋 起動中コンテナを確認します..."
docker ps

echo "✅ これでPostgres＋Pythonだけが稼働しているはずです！"
echo ""
echo "（pgAdminが表示されなければ成功です！）"
