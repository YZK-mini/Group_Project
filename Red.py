from socket import *
import pickle
import time
import Draw_Related

ip_red_server = ('127.0.0.1', 8000)  # 当红方发起游戏的ip地址
ip_red_client = ('127.0.0.1', 5000)  # 当红方参加游戏需要连接的端口
buf_size = 512  # 传输的尺寸限制
tag = 0  # 游戏进行状态标识，0表示开始界面，1表示等待界面，2表示游戏界面，3表示结束界面
button_start = 0  # 按下’创建房间‘按钮置为1
button_join = 0  # 按下’加入房间‘按钮置为1
board_choice = 1  # 棋盘选择标志


class Mess:  # 用于传送数据的类
    def __init__(self):
        self.beforeX = 0
        self.beforeY = 0
        self.afterX = 0
        self.afterY = 0


def create_Mess(msg, Pox, PoY, CuX, CuY):  # 创建数据传输的类，需要本方的移动信息
    msg.beforeX = Pox
    msg.beforeY = PoY
    msg.afterX = CuX
    msg.afterY = CuY


# 创建连接，两种方式
def build_connect(start, join):
    if start:
        s = socket(AF_INET, SOCK_STREAM)
        s.bind(ip_red_server)
    elif join:
        c = socket(AF_INET, SOCK_STREAM)
        c.connect(ip_red_client)


def main():
    global tag, button_start, button_join, board_choice

    # 初始化
    Draw_Related.init()

    # 主循环
    while True:
        global tag, button_start, button_join, board_choice

        # 背景绘制
        Draw_Related.bg_draw(tag)

        # 建立连接
        if tag == 0:
            build_connect(button_start, button_join)

        time.sleep(0.1)

        # 显示screen内容
        Draw_Related.Update()


if __name__ == '__main__':
    main()
