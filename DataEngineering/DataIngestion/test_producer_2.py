from faker import Faker
import random
from kafka import KafkaProducer
import json
from time import sleep
import time
import os
from datetime import datetime
from settings.config import Setting
from storage.s3_minio import S3Ceph

# Define the directory where your annotations, images are located
annotation_dir = '/home/anhdd/Downloads/VHT_Training_BigData/DataEngineering/DataIngestion/data/anotations' 
image_dir = '/home/anhdd/Downloads/VHT_Training_BigData/DataEngineering/DataIngestion/data/images'

# Initialize a list to store the retrieved data from all annotation files
all_annotations = {}

# Iterate through each annotation file in the directory
for filename in os.listdir(annotation_dir):
    annotation_file_path = os.path.join(annotation_dir, filename)
    image_filename = os.path.splitext(filename)[0] + '.jpg'
    image_file_path = os.path.join(image_dir, image_filename)
        
    # Initialize a dictionary to store the annotation data
    data = {}

    # Open and read the JSON annotation file
    with open(annotation_file_path, 'r') as json_file:
        data = json.load(json_file)
    # Add the annotation data to the dictionary, with the image path as the key
    all_annotations[image_file_path] = data



def fake_data():
    fake = Faker()

    # Tạo danh sách các nhãn
    labels = ['face', 'human']
    # Tạo danh sách các nhóm tìm kiếm
    search_groups = ['group1', 'group2', 'group3']

    # Tạo danh sách các user id
    user_ids = list(range(1, 101))

    # Tạo danh sách các tọa độ xyxy và khoảng cách so khớp
    bbox = []
    distances = []
    for i in range(100):
        x1 = random.randint(0, 100)
        y1 = random.randint(0, 100)
        x2 = random.randint(101, 200)
        y2 = random.randint(101, 200)
        bbox.append({'x1':x1,'y1':y1,'x2':x2,'y2':y2})
        distances.append(random.uniform(0, 1))

    # Tạo danh sách các track id
    track_ids = [fake.uuid4() for _ in range(100)]

    # Tạo danh sách các ảnh/video event
    event_links = [fake.url() for _ in range(100)]

    # Tạo danh sách các face với thông tin ngẫu nhiên
    faces = []
    for i in range(100):
        face = {
            'bbox': bbox[i],
            'distance': distances[i],
            'label': random.choice(labels),
            'track_id': track_ids[i],
            'user_id': random.choice(user_ids),
            'search_group': random.choice(search_groups),
            'event_link': event_links[i]
        }
        faces.append(face)
    return faces
  
def fake_data_vss():
    fake = Faker()
    
    si_ids = ["si_id_1", "si_id_2", "si_id_3", "si_id_4"]
    group_ids = ["group_id_1", "group_id_2", "group_id_3", "group_id_4"]
    user_ids = ["user_id_1", "user_id_2", "user_id_3", "user_id_4"]
    source_ids = ["source_id_1", "source_id_2", "source_id_3", "source_id_4"]
    object_ids = ["object_id_1", "object_id_id_2", "object_id_id_3", "object_id_id_4"]

    x1 = random.randint(0, 100)
    y1 = random.randint(0, 100)
    x2 = random.randint(101, 200)
    y2 = random.randint(101, 200)
    bbox = [x1, y1, x2, y2]
    confidence = random.uniform(0, 1)

    locals = ["Asian", "White", "Black"]
    gengers = ["Male", "Female"]
    ages = ["10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80-100"]
    person_ids = ["person_id_1", "person_id_2", "person_id_3", "person_id_4"]

    fair_face = [random.choice(locals), random.choice(gengers), random.choice(ages)]
    person_id = [random.choice(person_ids), random.choice(person_ids), random.choice(person_ids), random.choice(person_ids), random.choice(person_ids),]
    distance = random.uniform(0.5, 1)
    dict_distance = [distance, distance-0.05, distance-0.1, distance-0.15, distance-0.2]
    
    message = {"si_id": random.choice(si_ids), 
                "group_id": random.choice(group_ids), 
                "user_id": random.choice(user_ids), 
                "source_id": random.choice(source_ids),
                "object_id": random.choice(object_ids), 
                "bbox": bbox, 
                "confidence": confidence, 
                "image_path": fake.url(), 
                "time_stamp": int(time.time()*1000), 
                "fair_face": fair_face, 
                "person_id": person_id, 
                "dict": dict_distance}
    return message

def fake_event_data():
    fake = Faker()
    
    si_ids = ["si_1", "si_2"]
    # Tạo danh sách các nhãn
    labels = ['face', 'human']
    # Tạo danh sách các nhóm tìm kiếm
    group_ids = ['group_1', 'group_2',]

    # Tạo danh sách các user id
    user_ids = ["user_1", "user_2"]
    source_ids = ["cam_1", "cam_2"]

    # Tạo danh sách các tọa độ xyxy và khoảng cách so khớp
    # bbox = []
    # confidences = []
    # for i in range(100):
    #     x1 = random.randint(0, 100)
    #     y1 = random.randint(0, 100)
    #     x2 = random.randint(101, 200)
    #     y2 = random.randint(101, 200)
    #     bbox.append([x1, y1, x2, y2])
    #     confidences.append(random.uniform(0, 1))

    # Tạo danh sách các face với thông tin ngẫu nhiên
    events = []
    list_path_images = []
    for image_path, annotation in all_annotations.items():
        name_file = image_path.split("/")[-1]
        date_event = datetime.now().strftime("%d%m%Y")
        path_image_minio = f"/events/{date_event}/{name_file}"
        event = {
            "si_id": random.choice(si_ids),
            "group_id": random.choice(group_ids),
            "user_id": random.choice(user_ids),
            "source_id": random.choice(source_ids),
            # "label": random.choice(labels),
            # "object_id": fake.uuid4(),
            # "bbox": bbox[i],
            # "confidence": confidences[i],
            "label": annotation["label"],
            "object_id": annotation["object_id"],
            "bbox": annotation["box"],
            "confidence": annotation["confidence"],
            "bucket": "bucket-2",
            "image_path": path_image_minio,
            "time_stamp":int(time.time()*1000)
        }  
        events.append(event)
        list_path_images.append(image_path)
    return events, list_path_images




if __name__=="__main__":
    
    # s3_client = S3Ceph(aws_access_key_id=Setting.S3_ACCESS_KEY_ID,
    #                 aws_secret_access_key=Setting.S3_SECRET_ACCESS_KEY,
    #                 endpoint_url=Setting.S3_ENDPOINT_URL)

    producer = KafkaProducer(
        bootstrap_servers=[f"{Setting.KAFKA_HOST}:{Setting.KAFKA_PORT}", f"{Setting.KAFKA_HOST_2}:{Setting.KAFKA_PORT_2}"], 
        # Encode all values as JSON
        value_serializer=lambda value: json.dumps(value).encode(),
    )

    
    # for i in range(100):
    #     message = fake_data_vss()
    #     producer.send('testing', value=message)
    #     print("==============================================================")
    #     print(str(message)+ '\nTimestamp:' + time.ctime(time.time()))  # DEBUG
    #     sleep(1)
    
    # faces = fake_data()
    # for i in faces:
    #     print("Message: ", i)
    #     producer.send('testing', value=i)
    #     print('--------------------------------------------------')
    #     print(str(i)+ '\nTimestamp:' + time.ctime(time.time()))  # DEBUG
    #     sleep(1)
    
        
    events, list_path_images = fake_event_data()
    for i, event in enumerate(events):
        print("Message: ", event)
        #s3_client.upload_file(path=list_path_images[i], bucket_name=event["bucket"], name=event["image_path"])
        producer.send('event_topic_2', value=event)
        print('--------------------------------------------------')
        print(str(i)+ '\nTimestamp:' + time.ctime(time.time()))  # DEBUG
        sleep(1)
