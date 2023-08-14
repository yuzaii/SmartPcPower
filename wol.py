import socket


class Wol:
    def __init__(self, mac_address, ip):
        """
        Wol的配置
        :param mac_address:mac地址
        :param broadcast_ip: 广播地址
        """
        self.mac_address = mac_address
        self.ip = ip
        self.broadcast_ip = None

    def get_broadcast_ip(self):
        """
        获取广播地址
        :return:
        """
        ip_split = self.ip.split('.')
        ip_split[-1] = '255'
        self.broadcast_ip = '.'.join(ip_split)

    def wake(self):
        """
        开机
        :return:
        """
        # 获取广播地址
        self.get_broadcast_ip()
        # 处理mac地址
        self.mac_address = self.mac_address.replace('-', '').replace(':', '')
        ethernet_address = bytes.fromhex(self.mac_address)
        assert (len(ethernet_address) == 6)
        # 构建幻数据包
        magic_packet = b'\xff' * 6 + ethernet_address * 16
        # 发送幻数据包
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # 发送数据 端口号为9
        s.sendto(magic_packet, (self.broadcast_ip, 9))
        s.close()


if __name__ == '__main__':
    mac_address_to_wake = '2A:24:6F:02:10:5B'
    broadcast_ip = '192.168.10.9'
    wol = Wol(mac_address_to_wake, broadcast_ip)
    wol.wake()
