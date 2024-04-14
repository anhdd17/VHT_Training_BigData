from kafka import KafkaConsumer
import json
from helpers.logging import Logger
from database.database import Database2


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
            message_after = message["after"]
            #message_after = message
            print("Message: ", message_after)
            print("bbox: ", message_after["bbox"])
            res_insert = Database2.insert(
                table = "event",
                column = ("si_id", "group_id", "user_id", "source_id","label", "object_id", "bbox", 
                        "confidence", "bucket", "image_path", "time_stamp"),
                values = (message_after["si_id"], message_after["group_id"], message_after["user_id"], message_after["source_id"], message_after["label"],
                          message_after["object_id"], (message_after["bbox"]), str(message_after["confidence"]),
                          message_after["bucket"], message_after["image_path"], message_after["time_stamp"]))
            print("Res insert:", res_insert)
            Logger.info("Message informations: %s, %s, %s, %s", message_after["si_id"], message_after["group_id"], message_after["user_id"], message_after["source_id"])
            Logger.info("Res insert: %s", res_insert)
            