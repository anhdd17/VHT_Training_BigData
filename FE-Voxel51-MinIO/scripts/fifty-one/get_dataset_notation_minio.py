import fiftyone as fo
import boto3
from dotenv import load_dotenv
import os

load_dotenv()


ACCESS_KEY = os.getenv('S3_ACCESS_KEY_ID')
SECRET_KEY = os.getenv('S3_SECRET_ACCESS_KEY')
ENDPOINT_URL = os.getenv('S3_ENDPOINT_URL')

class FiftyOneDatasetManager:
    def __init__(self, bucket_name, dataset_name):
        self.s3 = boto3.client(
            's3',
            endpoint_url=ENDPOINT_URL,
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
            region_name='us-east-1',
            use_ssl=False
        )
        self.bucket_name = bucket_name
        self.dataset_name = dataset_name
        self.dataset = None

    def create_dataset(self):
        if self.dataset_name in fo.list_datasets():
            self.dataset = fo.load_dataset(self.dataset_name)
            print(f"Loaded existing dataset: {self.dataset_name}")
        else:
            self.dataset = fo.Dataset(name=self.dataset_name)
            print(f"Created new dataset: {self.dataset_name}")
        try:
            response = self.s3.list_objects_v2(Bucket=self.bucket_name)
            if 'Contents' in response:
                samples = []
                for obj in response['Contents']:
                    object_key = obj['Key']
                    url = self.s3.generate_presigned_url('get_object',
                                                         Params={'Bucket': self.bucket_name,
                                                                 'Key': object_key},
                                                         ExpiresIn=30)                 
                    sample = fo.Sample(filepath=url)
                    sample['filepath'] = url
                    samples.append(sample)
                    print(f"Added sample: {sample}")                   
                self.dataset.add_samples(samples)
            else:
                print(f"No objects found in bucket '{self.bucket_name}'.")
        except Exception as e:
            print(f"An error occurred: {e}")
        self.dataset.persistent = True
        self.dataset.reload()

    def update_dataset(self):
        self.dataset = fo.load_dataset(self.dataset_name)

        try:
            if self.dataset is None:
                print("Dataset is not loaded. Please create or load the dataset first.")
                return
            
            all_samples = self.dataset.select_fields(["id"]).values("id")  
            self.dataset.delete_samples(all_samples) 
            print(f"Deleted {len(all_samples)} samples from the dataset '{self.dataset_name}'")

            response = self.s3.list_objects_v2(Bucket=self.bucket_name)
            if 'Contents' in response:
                samples = []
                for obj in response['Contents']:
                    object_key = obj['Key']
                    url = self.s3.generate_presigned_url('get_object',
                                                        Params={'Bucket': self.bucket_name,
                                                                'Key': object_key},
                                                        ExpiresIn=3600)
                    sample = fo.Sample(filepath=url)
                    sample['filepath'] = url
                    samples.append(sample)
                    print(f"Added new sample with URL: {url}")
                
                self.dataset.add_samples(samples)
                print(f"Added {len(samples)} new samples to the dataset")
            else:
                print(f"No objects found in bucket '{self.bucket_name}'.")

        except Exception as e:
            print(f"An error occurred during dataset update: {e}")


    def delete_dataset(self):
        try:
            fo.delete_dataset(self.dataset_name)
            print(f"Dataset {self.dataset_name} deleted successfully.")
        except Exception as e:
            print(f"An error occurred while deleting the dataset: {e}")

    def launch_app(self):
        session = fo.launch_app(self.dataset, port=5151)
        session.wait()

def main():
    bucket_name = 'coco-2017'
    dataset_name = "unique-dataset-name"
    manager = FiftyOneDatasetManager(bucket_name, dataset_name)
    manager.delete_dataset()
    manager.create_dataset()
    manager.update_dataset()
    manager.launch_app()

if __name__ == "__main__":
    main()
