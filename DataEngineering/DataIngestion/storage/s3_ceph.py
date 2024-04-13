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
        logging.basicConfig(level=logging.INFO)
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
            self.logger.info("An exception: %s", err)
            raise err
        
        # Show all Bucket
        self.list_bucket = self.get_list_bucket()
        # self.logger.info("list_bucket: %s", self.list_bucket)
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

    def check_create_bucket(self, bucket_name):
        if bucket_name in self.list_bucket:
            self.logger.info("Bucket %s is existed", bucket_name)
            return True
        return self.create_bucket(bucket_name)

    # upload file to bucket or dir of bucket
    def upload_file(self, path, bucket_name, name):
        try:
            self.s3_client.upload_file(path, bucket_name, name)
            return True
        except Exception as err:
            self.logger.error("Upload file failed. File:%s - Bucket:%s - Name:%s", path, bucket_name, name)
            self.logger.error(err)
            return False
    
    def upload_multi_file(self, path, bucket_name, name):
        try:
            self.s3_client.upload_file(path, bucket_name, name)
            return True
        except Exception as err:
            self.logger.error("Upload file failed. File:%s - Bucket:%s - Name:%s", path, bucket_name, name)
            self.logger.error(err)
            return False
    
    #download file from a bucket
    def download_file(self, bucket_name, name, path_store):
        try:
            # self.logger.info(f"download file from ceph {bucket_name} {name}")
            # self.logger.info(f"store in {path_store}")
            self.s3_client.download_file(bucket_name, name, path_store)
        except Exception as err:
            self.logger.error("Download file failed. Bucket:%s - Name:%s - Store:%s", bucket_name, name, path_store)
            self.logger.error(err)
            return False
        return True

    def delete_file(self, bucket_name, name):
        try:
            self.logger.info(f"delete file ceph {bucket_name} {name}")
            self.s3_client.delete_object(Bucket=bucket_name, Key=name)
        except Exception as err:
            self.logger.error("Delete file failed. Bucket:%s - Name:%s ", bucket_name, name)
            self.logger.error(err)
            return False
        return True
    
    def getPreSignedUrl(self,bucket_name, file_name):
        url = self.s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': bucket_name, 'Key': file_name},
            ExpiresIn=(60*60*24),
        )
        return url

    def processUploadViaS3(self, file_path, bucket_name, file_name):
        file_size = os.path.getsize(file_path)
        filename, file_extension = os.path.splitext(file_path)
        file_checksum = hashlib.md5(file_path.encode('utf-8')).hexdigest()
        res= self.upload_file(file_path, bucket_name, file_name)
        url = self.getPreSignedUrl(bucket_name, file_name)
        if res:
            self.logger.info(f"Susscessfully upload {bucket_name} file {file_name} to ceph")
        else:
            self.logger.info(f"Fail to upload {bucket_name} file {file_name} to ceph")

        status = FileStatus.UPLOADED.value

        expired_date = getExpirationDateFromCurrentTime(1, TimeUnit.DAYS)

        s3_file_description = S3FileDescription(
            status = status,
            bucket_name = bucket_name,
            file_name = file_name,
            file_size = file_size,
            file_extension = file_extension,
            file_url = url,
            file_url_expiration_date = expired_date,
            file_check_sum = file_checksum
        )
        return res, s3_file_description


# from configs.envs.env_s3_ceph_config import ConfigS3Ceph
# S3Ceph_Obj = S3Ceph(aws_access_key_id=ConfigS3Ceph.aws_access_key_id,
#                     aws_secret_access_key=ConfigS3Ceph.aws_secret_access_key,
#                     endpoint_url=ConfigS3Ceph.endpoint_url)


if __name__ == '__main__':
    import sys
    import os
    config_dir = os.path.join('../', '')
    sys.path.insert(0, config_dir)

    from configs.envs.env_s3_ceph_config import ConfigS3Ceph

    s3_client = S3Ceph(aws_access_key_id=ConfigS3Ceph.aws_access_key_id,
                        aws_secret_access_key=ConfigS3Ceph.aws_secret_access_key,
                        endpoint_url=ConfigS3Ceph.endpoint_url)

    list_bucket = s3_client.get_list_bucket()
    print("List bucket: ", list_bucket)

    # bucket_name = "datbt5-bucket9"
    # response = s3_client.check_create_bucket(bucket_name) 
    # print('response: ', response)
    
    response = s3_client.download_file( "aisample", "fffce9641de311ed9b9b5e0fb1534142_240660_cropFace_0", "test.jpg")
    print('response: ', response)                                   
                                       
    # response = s3_client.upload_file("/home/ai_server_multi_search/data/images/images.jpeg", "datbt5-bucket", "test2.jpg") #upload file
    # print('response: ', response)

    # print(s3_client.getPreSignedUrl("datbt5-bucket","test.jpg"))

    # s3_client.processUploadViaS3("test.jpg","/home/ai_server/abc.jpg","datbt5-bucket")





    


