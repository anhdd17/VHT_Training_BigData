# minio_uploader.py
import boto3
import os

class MinIOUploader:
    def __init__(self, access_key, secret_key, endpoint_url, bucket_name):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            endpoint_url=endpoint_url,
            region_name='us-east-1'
        )
        self.bucket_name = bucket_name

    def upload_files(self, directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                self.s3_client.upload_file(file_path, self.bucket_name, filename)
                print(f'Uploaded {filename} to bucket {self.bucket_name}')
