from socket import *
import pickle
import Draw_Related
import threading

ip_red_server = ('127.0.0.1', 8000)  # 当红方发起游戏的ip地址
ip_red_client = ('127.0.0.1', 5000)  # 当红方参加游戏需要连接的ip地址
buf_size = 512  # 传输的尺寸限制
tag = 0  # 游戏进行状态标识，0表示开始界面，1表示等待界面，2表示游戏界面，3表示结束界面
s = socket(AF_INET, SOCK_STREAM)
s.bind(ip_red_server)
s.listen(1)


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
def build_connect(startORjoin):
    global tag, s, wait_thread

    if not startORjoin:
        wait_thread = threading.Thread(target=waiting)
        wait_thread.start()
    else:
        c = socket(AF_INET, SOCK_STREAM)
        c.connect(ip_red_client)


def waiting():
    global s, tag

    s.accept()
    Draw_Related.begin()


def main():
    global tag, s

    # 初始化
    Draw_Related.init()

    # 主循环
    while True:
        ps_tag = tag
        # 操作信息检测
        tag = Draw_Related.check_movement()

        # 建立连接
        # 初始为0，事件检测后为1，启动游戏；初始为0，事件检测后为2，加入游戏
        if (tag == 1 or tag == 2) and ps_tag == 0:
            build_connect(tag - 1)
        # tag由1变0，等待界面返回开始界面，停止连接等待进程
        if tag == 0 and ps_tag == 1:
            wait_thread._running = False

        # 背景绘制
        Draw_Related.bg_draw(tag)

        # 显示screen内容
        Draw_Related.Update()


if __name__ == '__main__':
    main()
