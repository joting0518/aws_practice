import pandas as pd
import boto3
import os

s3 = boto3.client('s3')

def upload_folder_to_s3(local_folder_path, bucket_name):
    for file in os.listdir(local_folder_path):
        if file == '.DS_Store' or not os.path.isfile(os.path.join(local_folder_path, file)):
            continue

        local_file_path = os.path.join(local_folder_path, file)

        file_extension = os.path.splitext(file)[1].lower()
        if file_extension in ['.jpg', '.jpeg']:
            s3_folder = 'jpg'
        elif file_extension == '.png':
            s3_folder = 'png'
        elif file_extension == '.tiff':
            s3_folder = 'tiff'
        else:
            continue 

        s3_key = os.path.join(s3_folder, file)

        s3.upload_file(local_file_path, bucket_name, s3_key)
        print(f"Uploaded {local_file_path} to s3://{bucket_name}/{s3_key}")


upload_folder_to_s3('/Users/chenruoting/Desktop/kyc_github/s3_pratice/element', 'newsortbucket')