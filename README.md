# AWS S3 操作指南

這份文件提供了一個簡單的 AWS S3 操作指南，包括 IAM 使用者權限設定、Access Keys 創建、上傳資料夾、生成 Presigned URL 等。
此外，本文件也包含了常見問題的說明，並根據個人經驗，針對可能較模糊得概念、常見錯誤進行說明

## 1. IAM 使用者權限設定

在 AWS 的 IAM 中，手動創建使用者並授予相應權限。你可以在 "Permission" 中查看所授予該使用者的權限。

## 2. 創建 Access Keys

前往 "Security Credentials" 頁面，創建 Access Keys 以取得一組公私鑰。之後，這組鑰匙可用於設定 CLI 或直接進行驗證。

# 使用 Boto3 創建 S3 客戶端
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
## 3. 實作 S3 相關功能

查看 [S3 API 參考文件](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html) 以了解 S3 相關功能。

## 4. 上傳資料夾

由於無法直接上傳整個資料夾，需要使用迴圈逐一上傳。詳細可參考 [upload_file API 文件](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/upload_file.html)。

## 5. 實作 Presigned URL

建立 Presigned URL，可設定限制條件如：
- 限制 IP
- URL 一小時後失效
- URL 只能使用一次

參考 [generate_presigned_url API 文件](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/generate_presigned_url.html)。
參考 [知乎教學 AWS S3 presigned URL 教程](https://zhuanlan.zhihu.com/p/473553899)

## 6. IP 白名單設定

建立 IP 白名單以限制存取。最好是利用s3進行ip設定，而非在presigned url中
可以在bucket中的policy區域（permission），利用json去設定，範例如下
```
{
    "Version": "2012-10-17",
    "Id": "PolicyId2",
    "Statement": [
        {
            "Sid": "AllowIPmix",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:*",
            "Resource": [
                "arn:aws:s3:::amypractice",
                "arn:aws:s3:::amypractice/*"
            ],
            "Condition": {
                "NotIpAddress": {
                    "aws:SourceIp": [
                        "203.0.113.0/24",
                        "2001:DB8:1234:5678:ABCD::/80",
                        "39.12.65.124"
                    ]
                },
                "IpAddress": {
                    "aws:SourceIp": "192.0.2.0/24"
                }
            }
        }
    ]
}
```

~~但這裡容易遇到一個問題：設定好policy後，明明限制了自己的ip，但仍然能存取s3 bucket
那可能是因為電腦緩存或是該帳號擁有很高的iam權限。因此，在ip被限制的情況仍可能會可以獲取bucket或是object
解方：新建一個帳戶賦予s3:GetObject 和 s3:PutObject權限，利用aws s3 ls s3://amypractice指令去檢查（也可以使用aws sdk）~~

新解方：
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::bucketname",
        "arn:aws:s3:::bucketname/*"
      ],
      "Condition": {
         "NotIpAddress": {
            "aws:SourceIp": "ip address should be allowed" 
         }
      }
    }
  ]
}
```

## 7. 處理 Signature Does Not Match & URL 包含 Access Key ID 問題

在程式執行中，若出現 "Signature Does Not Match" 加上ip限制時，會出現this error，建議使用bucket 設定policy 
參考[s3 policy 設定](https://repost.aws/questions/QUu2KDx_98TMGP3vTi7Lv0dA/limit-ipaddress-while-uploading-to-aws-s3-bucket-using-aws-post-policy)
URL 包含 Access Key ID 的問題

## 8. presigned url 設定 
 - 當產生一個預簽名URL（presigned URL）時，存取控制是在產生URL的時候進行的，而不是在使用URL的時候。這意味著，只要產生URL的請求符合策略條件，產生的URL可以在任何地方使用，無論使用者的IP位址是什麼。
   - 如果企業在被允許的IP範圍內產生了一個預簽名URL，然後user嘗試在被拒絕的IP位址使用這個URL，它仍然是有效的。

## 9. presigned url 中的機敏資料該如何隱藏