# upload_images.py
from minio_uploader import MinIOUploader
from dotenv import load_dotenv
import os

load_dotenv()

ACCESS_KEY = os.getenv('S3_ACCESS_KEY_ID')
SECRET_KEY = os.getenv('S3_SECRET_ACCESS_KEY')
ENDPOINT_URL = os.getenv('S3_ENDPOINT_URL')
BUCKET_NAME = 'coco-2017'

IMAGE_DIRECTORY = '/home/anhdd/Downloads/VHT_Training_BigData/FE-Voxel51-MinIO/coco-2017/train2017/img'

uploader = MinIOUploader(ACCESS_KEY, SECRET_KEY, ENDPOINT_URL, BUCKET_NAME)
uploader.upload_files(IMAGE_DIRECTORY)