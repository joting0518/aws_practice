import pandas as pd
import boto3
import os
# use access key and still have error bc ip_restrict
df = pd.read_csv('s3test_accessKeys.csv')

aws_access_key_id = df['Access key ID'].iloc[0]
aws_secret_access_key = df['Secret access key'].iloc[0]

s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

def upload_folder_to_s3(local_folder_path, bucket_name, s3_folder_path=''):
    for file in os.listdir(local_folder_path):
        if file == '.DS_Store':
            continue

        local_file_path = os.path.join(local_folder_path, file)

        # 比較相對路徑 s3_key=.jpg, .png, .tiff
        s3_key = os.path.relpath(local_file_path, local_folder_path)

        # 如果 s3_folder_path 存在 ex: element，則加上
        if s3_folder_path:
            s3_key = os.path.join(s3_folder_path, s3_key)

        s3.upload_file(local_file_path, bucket_name, s3_key)
        print(f"Uploaded {local_file_path} to s3://{bucket_name}/{s3_key}")

def look_bucket(bucket_name):
    response = s3.list_objects(Bucket=bucket_name)

    if 'Contents' in response:
        for obj in response['Contents']:
            print(f"Object Key: {obj['Key']}, Last Modified: {obj['LastModified']}, Size: {obj['Size']} bytes")
    else:
        print("No objects found in the bucket.")

def generate_presigned_url(bucket_name, object_key, expiration=3600, allowed_ip=None):
    
    url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': object_key},
        ExpiresIn=expiration
    )

    if allowed_ip:
        url += f"&X-Amz-Expires={expiration}&X-Amz-AllowedIP={allowed_ip}"

    return url

upload_folder_to_s3('/Users/chenruoting/Desktop/test/aws_s3/element', 'amypractice', 'element')

#look_bucket('amypractice')

presigned_url = generate_presigned_url('amypractice', 'element/example_JPG.jpg', expiration=3600)
print(f"Presigned URL: {presigned_url}")
