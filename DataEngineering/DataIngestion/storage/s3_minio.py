import boto3
import logging
import hashlib
import time
import os
import enum
import datetime


class FileStatus(enum.Enum):
    NEW = 0
    UPLOADED = 1
    REJECTED = 2

class TimeUnit(enum.Enum):
    DAYS = 60*60*24
    HOURS = 60*60
    MINUTES = 60
    SECONDS = 1

class S3FileDescription:
    def __init__(self, status, bucket_name, file_name, file_size, file_extension, file_url, file_url_expiration_date, file_check_sum):
        self.status = status
        self.bucketName = bucket_name
        self.fileName = file_name
        self.fileSize = file_size
        self.fileExtension = file_extension
        self.fileURL = file_url
        self.fileUrlExpriationDate = file_url_expiration_date
        self.fileCheckSum = file_check_sum

    def toString(self):
        return f"status : {self.status} - bucketName : {self.bucketName} - fileName : {self.fileName} \
         -  fileSize : {self.fileSize}  - fileExtension : {self.fileExtension} \
         - fileURL : {self.fileURL} \
         - fileUrlExpriationDate : {self.fileUrlExpriationDate} - fileCheckSum {self.fileCheckSum} "

def current_milli_time():
    return round(time.time() * 1000)

def getExpirationDateFromCurrentTime(expired_duration, time_unit):
    current =  current_milli_time()
    # print(current)
    expired_time = current + (expired_duration * time_unit.value * 1000)
    # print(expired_time)

    expired_date = datetime.datetime.fromtimestamp(expired_time/1000)
    return expired_date

class S3Ceph():
    def __init__(self, aws_access_key_id, aws_secret_access_key, endpoint_url):
        # Set up our logger
        logging.basicConfig(filename='s3ceph_log.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
        self.logger = logging.getLogger()

        try:
            session = boto3.session.Session()
            self.s3_client = session.client(
                service_name='s3',
                aws_access_key_id= aws_access_key_id,
                aws_secret_access_key= aws_secret_access_key,
                endpoint_url= endpoint_url
            )
        except Exception as err:
            self.logger.exception("An exception: %s", err)
            raise err
        
        self.logger.info("Server Conneted to Ceph: %s", endpoint_url)
            
    def get_list_bucket(self):
        list_bucket = [bucket['Name'] for bucket in self.s3_client.list_buckets()["Buckets"]]
        return list_bucket
    
    def update_list_bucket(self):
        self.list_bucket = self.get_list_bucket()

    def create_bucket(self, bucket_name):
        try:
            self.s3_client.create_bucket(Bucket=bucket_name)
            self.update_list_bucket()
        except Exception as  err:
            self.logger.error("Create Bucket %s Error: %s", bucket_name, err)
            return False
        return True
    
    def check_path_exist(self, path):
        # example: "s3://vss/pq/ls" split -> ['s3:', '', 'vss', 'pq', 'ls'] -> bucket name = vss
        bucket_name = path.split("/")[2]
        prefix = None
        
        if f"s3://{bucket_name}" in path:
            prefix = path.replace(f"s3://{bucket_name}",'')
        count = self.s3_client.list_objects(Bucket=bucket_name,
                                          Prefix=prefix)
        
        if 'Contents' in count.keys():
            return True
        else:
            return False
        
    def delete_folder(self, path):
        # example: "s3://vss/pq/ls" split -> ['s3:', '', 'vss', 'pq', 'ls'] -> bucket name = vss
        bucket_name = path.split("/")[2]
        prefix = None
        
        if f"s3://{bucket_name}" in path:
            prefix = path.replace(f"s3://{bucket_name}",'')
            
        if not self.check_path_exist(path=path):
            self.logger.info("Delete folder path not existed: %s", path)
            return True
        try:
            # Delete using "remove_object"
            objects_to_delete = self.s3_client.list_objects(bucket_name, prefix=prefix, recursive=True)
            for obj in objects_to_delete:
                self.s3_client.remove_object(bucket_name, obj.object_name)
            return True
        except Exception as  err:
            self.logger.error("Delete folder %s Error: %s", path, err)
            return False
        
    def update_path(self, path, path_update):
        # example: "s3://vss/pq/ls" split -> ['s3:', '', 'vss', 'pq', 'ls'] -> bucket name = vss
        bucket_name = path.split("/")[2]
        prefix = None
        
        if f"s3://{bucket_name}" in path:
            prefix = path.replace(f"s3://{bucket_name}",'')
            
        if not self.check_path_exist(path=path):
            self.logger.info("Folder path not existed: %s", path)
            return False
        
        return True
        
    def upload_file(self, path, bucket_name, name):
        try:
            self.s3_client.upload_file(path, bucket_name, name)
            return True
        except Exception as err:
            self.logger.error("Upload file failed. File:%s - Bucket:%s - Name:%s", path, bucket_name, name)
            self.logger.error(err)
            return False




if __name__ == '__main__':
    import sys
    import os
    config_dir = os.path.join('../', '')
    sys.path.insert(0, config_dir)

    from settings.config import Setting

    s3_client = S3Ceph(aws_access_key_id=Setting.S3_ACCESS_KEY_ID,
                        aws_secret_access_key=Setting.S3_SECRET_ACCESS_KEY,
                        endpoint_url=Setting.S3_ENDPOINT_URL)
    #Create bucket
    # bucket_2 = s3_client.create_bucket("bucket-2")

    list_bucket = s3_client.get_list_bucket()
    print("List bucket: ", list_bucket)

    #check path
    is_path_exist = s3_client.check_path_exist("s3://bucket-1/Screenshot from 2023-10-16 22-37-22.png")
    print(is_path_exist)

    # #upload object
    s3_client.upload_file('/home/anhdd/Pictures/Screenshot from 2023-10-16 21-43-27.png', 'bucket-2', 'test image 2004.jpeg' )

    # s3_client.share_objects('bucket-1', 'bucket-2','test image.jpeg', 'image share2.jpeg')

    #credentials = s3_client.generate_minio_user_credentials(3)

    # print(s3_client.delete_folder("s3://bucket-1"))

    # list_bucket = s3_client.get_list_bucket()
    # print("List bucket: ", list_bucket)

    # response = s3_client.download_file( "datalake", "dataRaw", "dataRaw")
    # print('response: ', response)                                   
                                       






    


