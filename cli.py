# cli.py
import sys
import subprocess

def run_pipeline():
    print("パイプライン処理を実行します...")
    subprocess.run(["python", "scripts/sales_pipeline.py"])

def main():
    if len(sys.argv) < 2:
        print("コマンドを指定してください (例: pipeline)")
        sys.exit(1)

    command = sys.argv[1]

    if command == "pipeline":
        run_pipeline()
    else:
        print(f"不明なコマンド: {command}")

if __name__ == "__main__":
    main()
