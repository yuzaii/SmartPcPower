import json

import requests

from config import bf_uid


class Bemfa:
    def __init__(self, uid):
        self.uid = uid

    def get_mqtt_topics(self):
        """
        获取所有主题
        :return:
        """
        url = "https://apis.bemfa.com/va/alltopic"
        params = {
            "uid": self.uid,
            "type": 1
        }
        res = requests.get(url=url, params=params)
        res_json = res.json()
        # print(res_json)
        # 获取data
        data = res_json.get("data")
        pcList = []
        for item in data:
            pcList.append(item)
        return pcList

    def close_pc(self, subject):
        """
        关闭电脑
        :param subject: 主题
        :return:
        """
        url = "https://apis.bemfa.com/va/postmsg"
        data = {
            "uid": self.uid,
            "topic": subject,
            "type": 1,
            "msg": "off",
        }
        requests.post(url=url, data=data)


if __name__ == '__main__':
    bemfa = Bemfa(bf_uid)
    # pcList = bemfa.get_mqtt_topics()
    # print(pcList)
    bemfa.close_pc("PC1006")
