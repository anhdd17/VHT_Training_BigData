from kafka import KafkaConsumer
import json
from helpers.logging import Logger
from database.database import Database


class Consumer():
    def __init__(self, host, port, host2, port2, topic, group_id) -> None:
        # init consumer instane
        print("Infor: ", host, port, topic, group_id)
        Logger.info("Infor: %s, %s, %s, %s", host, port, topic, group_id)
        self.consumer = KafkaConsumer(
            topic,
            group_id=group_id,
            bootstrap_servers=[f"{host}:{port}", f"{host2}:{port2}"], 
            # bootstrap_servers= [f"{host2}:{port2}"], 
            value_deserializer=lambda m: json.loads(m.decode('utf-8')))
        print("Infor: ", host, port, topic, group_id)
    def __call__(self):
        Logger.info("Staring call function")
        for message in self.consumer:
            Logger.info("Get Message")
            message = message.value
            print("Message: ", message)
            print("bbox: ", message["bbox"])
            res_insert = Database.insert(
                table = "event",
                column = ("si_id", "group_id", "user_id", "source_id","label", "object_id", "bbox", 
                        "confidence", "bucket", "image_path", "time_stamp"),
                values = (message["si_id"], message["group_id"], message["user_id"], message["source_id"], message["label"],
                          message["object_id"], (message["bbox"]), str(message["confidence"]),
                          message["bucket"], message["image_path"], message["time_stamp"]))
            print("Res insert:", res_insert)
            Logger.info("Message informations: %s, %s, %s, %s", message["si_id"], message["group_id"], message["user_id"], message["source_id"])
            Logger.info("Res insert: %s", res_insert)
            
        
            
            
            
            


