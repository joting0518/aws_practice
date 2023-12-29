import json
import logging

import boto3
from botocore.exceptions import ClientError



PRIVATE_BUCKET_NAME = ""


def upload_file_obj(file_obj: bytes, bucket_name: str, object_name: str):
    """Upload a file to an S3 bucket

    :param file_obj: A file-like object to upload. At a minimum, it must implement the read method, and must return bytes.
    :param bucket_nmae: name of Bucket to upload to
    :param object_name: S3 object name
    :return: True if file was uploaded, else False
    """
    s3 = boto3.client("s3")
    try:
        s3.upload_fileobj(file_obj, bucket_name, object_name)
    except ClientError:
        logging.exception(f"Upload file to {bucket_name} Failed.")
        return False
    return True


def upload_obj(body: bytes, bucket_name: str, object_name: str):
    """Upload a file to an S3 bucket

    :param body: bytes to upload
    :param bucket_nmae: name of Bucket to upload to
    :param object_name: S3 object name
    :return: True if file was uploaded, else False
    """
    s3 = boto3.client("s3")
    try:
        s3.put_object(Body=body, Bucket=bucket_name, Key=object_name)
    except ClientError:
        logging.exception(f"Upload file to {bucket_name} Failed.")
        return False
    return True


def get_obj(bucket_name: str, object_name: str):
    """Download a file from an S3 bucket

    :param bucket_nmae: S3 Bucket name
    :param object_name: S3 object name
    :return: bytes
    """
    s3 = boto3.client("s3")
    try:
        return s3.get_object(Bucket=bucket_name, Key=object_name)
    except ClientError:
        logging.exception(f"Get file {bucket_name}/{object_name} Failed.")


def upload_user_file_obj(file_obj, object_name: str):
    return upload_file_obj(file_obj, PRIVATE_BUCKET_NAME, object_name)


def upload_user_obj(body: bytes, object_name: str):
    return upload_obj(body, PRIVATE_BUCKET_NAME, object_name)


def get_user_obj(object_name: str):
    return get_obj(PRIVATE_BUCKET_NAME, object_name)


def get_json_content(object_name: str):
    content = (
        get_obj(PRIVATE_BUCKET_NAME, object_name)["Body"]
        .read()
        .decode("utf-8")
    )
    return json.loads(content)
