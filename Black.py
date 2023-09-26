from socket import *
import pickle

ip_black_server = ('127.0.0.1', 5000)  # 当黑方发起游戏的ip地址
ip_black_client = ('127.0.0.1', 8000)  # 当黑方加入游戏需要连接的ip地址
buf_size = 512  # 传输的尺寸限制
tag = 0  # 游戏进行状态标识，0表示开始界面，1表示等待界面，2表示游戏界面，3表示结束界面


class Mess:  # 用于传送数据的类
    def __init__(self):
        self.beforeX = 0
        self.beforeY = 0
        self.afterX = 0
        self.afterY = 0


def create_Mess(msg, PoX, PoY, CuX, CuY):  # 创建数据传输的类，需要本方的移动信息
    msg.beforeX = PoX
    msg.beforeY = PoY
    msg.afterX = CuX
    msg.afterY = CuY
