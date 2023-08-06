from core.mqtt import MQTTSubscribe
from core.woker_pool import message_thread_pool


def start():
    mqtt_subscribe = MQTTSubscribe()
    message_thread_pool.start_task()
    mqtt_subscribe.server_connect()


if __name__ == '__main__':
    start()
