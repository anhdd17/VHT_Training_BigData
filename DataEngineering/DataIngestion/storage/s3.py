import boto3
import cv2
import numpy as np
import traceback
from common.config import Setting
from common.logging import Logger


class S3Client:
    def __init__(self, endpoint_url: str, aws_access_key_id: str, aws_secret_access_key: str, region_name: str):
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=endpoint_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )

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

    # === Deal with opencv image ===
    def get_opencv_img(self, path, bucket=Setting.S3_BUCKET):
        try:
            byte_data = self.get(path, bucket)
            # print(len(byte_data))
            img_as_np = np.frombuffer(byte_data, dtype=np.uint8)
            return cv2.imdecode(img_as_np, flags=cv2.IMREAD_COLOR)
        except:
            print(traceback.format_exc())
            return None

    def write_opencv_img(self, img, path, bucket=Setting.S3_BUCKET):
        _, buf = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 90])
        return self.put(buf.tobytes(), path, bucket)