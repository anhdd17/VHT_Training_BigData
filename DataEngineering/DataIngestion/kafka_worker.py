
from settings.config import Setting
from worker.consumer import Consumer


print(Setting.KAFKA_HOST)

if __name__=="__main__":
    consumer = Consumer(host=Setting.KAFKA_HOST, port=Setting.KAFKA_PORT, host2=Setting.KAFKA_HOST_2, port2=Setting.KAFKA_PORT_2,topic=Setting.KAFKA_TOPIC, group_id="group_3")
    consumer()