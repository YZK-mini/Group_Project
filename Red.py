from socket import *
import pickle
import Draw_Related
import threading

ip_red_server = ('127.0.0.1', 8000)  # 当红方发起游戏的ip地址
ip_red_client = ('127.0.0.1', 5000)  # 当红方参加游戏需要连接的ip地址
buf_size = 512  # 传输的尺寸限制


class Mess:  # 用于传送数据的类
    def __init__(self):
        self.beforeX = 0
        self.beforeY = 0
        self.afterX = 0
        self.afterY = 0

    def create_Mess(self, Pox, PoY, CuX, CuY):  # 创建数据传输的类，需要本方的移动信息
        self.beforeX = Pox
        self.beforeY = PoY
        self.afterX = CuX
        self.afterY = CuY


# 红方类
class Red_Side(Draw_Related.objection):
    def __init__(self):
        super(Red_Side, self).__init__()
        self.tag = 0  # 游戏进行状态标识，0表示开始界面，1表示等待界面，2表示游戏界面，3表示结束界面
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.bind(ip_red_server)
        self.s.listen(1)
        self.wait_thread = threading.Thread()
        self.c = socket(AF_INET, SOCK_STREAM)

    # 创建连接，两种方式
    def build_connect(self):
        if self.start_OR_join == 1:
            self.wait_thread = threading.Thread(target=self.waiting)
            self.wait_thread.start()
        elif self.start_OR_join == 2:
            self.c.connect(ip_red_client)

    def waiting(self):
        print('wait')
        self.s.accept()
        self.tag = 2
        print('start')


def main():
    # 初始化
    Red = Red_Side()

    # 主循环
    while True:
        ps_tag = Red.tag
        # 操作信息检测
        Red.tag = Red.check_movement()

        # 建立连接
        # 初始为0，事件检测后为1，启动游戏；初始为0，事件检测后为2，加入游戏
        if (Red.tag == 1 or Red.tag == 2) and ps_tag == 0:
            Red.build_connect()

        # tag由1变0，等待界面返回开始界面，停止连接等待进程
        if Red.tag == 0 and ps_tag == 1:
            Red.wait_thread._running = False
            print(Red.wait_thread.isAlive())

        # 背景绘制
        Red.bg_draw()

        # 显示screen内容
        Red.Update()


if __name__ == '__main__':
    main()
