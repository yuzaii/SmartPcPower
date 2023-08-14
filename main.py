import threading

from Pcmqtt import PCMQTT
from bemfa import Bemfa
from config import bf_uid, pcList

if __name__ == '__main__':
    bemfa = Bemfa(bf_uid)
    # pcList = bemfa.get_mqtt_topics()
    threads = []
    for pc in pcList:
        name = pc.get('name')
        subject = pc.get('subject')
        mac_address = pc.get('mac_address')
        ip = pc.get('ip')
        pcmqtt = PCMQTT(name, subject, mac_address, ip)
        # 定义线程
        thread = threading.Thread(target=pcmqtt.start)
        # 将线程加入线程列表
        threads.append(thread)
        # 启动线程
        thread.start()
    # 等待所有线程完成
    for thread in threads:
        thread.join()
