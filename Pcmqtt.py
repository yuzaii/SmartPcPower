import time

import paho.mqtt.client as mqtt

from config import bf_uid
from wol import Wol


class PCMQTT:
    def __init__(self, name, subject, mac_address, ip):
        """
        巴法云mqtt协议电脑开关机的配置
        :param subject:
        :param client_id:
        """
        self.HOST = "bemfa.com"
        self.PORT = 9501
        self.name = name
        self.subject = subject
        self.client_id = bf_uid
        self.mac_address = mac_address
        self.ip = ip

    # 连接并订阅
    def on_connect(self, client, userdata, flags, rc):
        print(f"{self.name}:Connected with result code " + str(rc))
        client.subscribe(self.subject)  # 订阅消息

    # 消息接收
    def on_message(self, client, userdata, msg):
        topic = msg.topic
        message = str(msg.payload.decode('utf-8'))
        print(f"{self.name}:主题:" + topic + " 消息:" + message)
        if message == 'on':
            # 开机
            print(f"{self.name}:开机")
            wol = Wol(self.mac_address, self.ip)
            wol.wake()

    # 订阅成功
    def on_subscribe(self, client, userdata, mid, granted_qos):
        print(f"{self.name}:订阅成功,On Subscribed: qos = %d" % granted_qos)

    # 失去连接
    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            print(f"{self.name}:Unexpected disconnection %s" % rc)

    # 启动连接
    def start(self):
        print(f"{self.name}:开始连接")
        client = mqtt.Client(self.client_id)
        # client.username_pw_set("username", "passwd")
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.on_subscribe = self.on_subscribe
        client.on_disconnect = self.on_disconnect
        client.connect(self.HOST, self.PORT, 60)
        client.loop_forever()


if __name__ == '__main__':
    pcmqtt = PCMQTT("主电脑", "PC1001", "24-4B-FE-45-A0-C7", "192.168.10.10")
    pcmqtt.start()
