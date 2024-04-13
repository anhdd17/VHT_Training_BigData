import boto3
import cv2
import numpy as np
import traceback
import sys
import os
config_dir = os.path.join('../', '')
sys.path.insert(0, config_dir)
from utils.logging import Logger
from settings.config import Setting


class SeaWeedClient:
    def __init__(self, endpoint_url, aws_access_key_id, aws_secret_access_key, region_name):
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=endpoint_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )

    def get_list_bucket(self):
        list_bucket = [bucket['Name'] for bucket in self.s3_client.list_buckets()["Buckets"]]
        return list_bucket
    
    def update_list_bucket(self):
        self.list_bucket = self.get_list_bucket()
        
    def get(self, path, bucket=Setting.S3_BUCKET):
        try:
            response = self.s3_client.get_object(Bucket=bucket, Key=path)
            return response["Body"].read()
        except:
            Logger.debug(traceback.format_exc())
            return False

    def put(self, buf, path, bucket=Setting.S3_BUCKET):
        try:
            self.s3_client.put_object(Bucket=bucket, Key=path, Body=buf)

        except:
            Logger.debug(traceback.format_exc())
            return False

    def copy(self, src_path, dest_path, bucket=Setting.S3_BUCKET):
        copy_source = {"Bucket": bucket, "Key": src_path}
        self.s3_client.copy_object(CopySource=copy_source, Bucket=bucket, Key=dest_path)

    def move(self, src_path, dest_path, bucket=Setting.S3_BUCKET):
        self.copy(src_path, dest_path)
        self.s3_client.delete_object(Bucket=bucket, Key=src_path)
        
    #download file from a bucket
    def download_file(self, bucket_name, name, path_store):
        try:
            Logger.info(f"download file from ceph {bucket_name} {name}")
            Logger.info(f"store in {path_store}")
            self.s3_client.download_file(bucket_name, name, path_store)
        except Exception as err:
            Logger.debug("Download file failed. Bucket:%s - Name:%s - Store:%s", bucket_name, name, path_store)
            Logger.debug(err)
            return False
        return True
    
    # === Deal with opencv image ===
    def get_opencv_img(self, path, bucket=Setting.S3_BUCKET):
        try:
            byte_data = self.get(path, bucket)
            img_as_np = np.frombuffer(byte_data, dtype=np.uint8)
            return cv2.imdecode(img_as_np, flags=cv2.IMREAD_COLOR)
        except:
            print(traceback.format_exc())
            return None

    def write_opencv_img(self, img, path, bucket=Setting.S3_BUCKET):
        _, buf = cv2.imencode(".jpg", img)
        return self.put(buf.tobytes(), path, bucket)


# SeaWeed = SeaWeedClient(
#     endpoint_url=Setting.S3_ENDPOINT_URL,
#     aws_access_key_id=Setting.S3_ACCESS_KEY_ID,
#     aws_secret_access_key=Setting.S3_SECRET_ACCESS_KEY,
#     region_name=Setting.S3_REGION_NAME,
# )


if __name__ == '__main__':
    s3_client = SeaWeedClient(endpoint_url=Setting.S3_ENDPOINT_URL,
                        aws_access_key_id=Setting.S3_ACCESS_KEY_ID,
                        aws_secret_access_key=Setting.S3_SECRET_ACCESS_KEY,
                        region_name=Setting.S3_REGION_NAME)

    list_bucket = s3_client.get_list_bucket()
    print("List bucket: ", list_bucket)
    
    # response = s3_client.get("dataRaw/animals_od/labels.json", "datalake")
    # print('response: ', response)      
    
    # response =  s3_client.download_file(bucket_name="datalake", name="dataRaw/animals_od/labels.json", path_store="labels.json")
    # print(response)
    
    
    import deeplake
    # Low Level API
    ds = deeplake.load('s3://datalake/deeplake_datasets/animals_od', 
                    creds = {
                        'aws_access_key_id': Setting.S3_ACCESS_KEY_ID,
                        'aws_secret_access_key': Setting.S3_SECRET_ACCESS_KEY,
                        'endpoint_url': Setting.S3_ENDPOINT_URL
                        }
                        )
    print("len: ", len(ds['images']))
    