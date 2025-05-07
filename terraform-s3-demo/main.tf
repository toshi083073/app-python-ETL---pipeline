# main.tf

terraform {
  backend "s3" {
    bucket = "my-bucket-toshi-2025"               # 作成済みのS3バケット名
    key    = "terraform/terraform.tfstate"        # バケット内の保存パス
    region = "ap-northeast-1"                     # バケットのリージョン
  }
}

provider "aws" {
  region = "ap-northeast-1"
}

resource "aws_s3_bucket" "main_bucket" {
  bucket = "my-bucket-toshi-2025" # ※すでに存在する場合、上書きしないよう注意
}

resource "aws_s3_bucket_versioning" "main_bucket_versioning" {
  bucket = aws_s3_bucket.main_bucket.bucket

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "main_bucket_encryption" {
  bucket = aws_s3_bucket.main_bucket.bucket

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
