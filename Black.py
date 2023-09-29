from socket import *
import pickle
import Draw_Related
import threading

ip_black_server = ('127.0.0.1', 5000)  # 当黑方发起游戏的ip地址
ip_black_client = ('127.0.0.1', 8000)  # 当黑方加入游戏需要连接的ip地址
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
class Black_Side(Draw_Related.objection):
    def __init__(self):
        super(Black_Side, self).__init__()
        self.tag = 0  # 游戏进行状态标识，0表示开始界面，1表示等待界面，2表示游戏界面，3表示结束界面
        self.s = socket(AF_INET, SOCK_STREAM)  # 创建服务器接口
        self.s.bind(ip_black_server)  # 绑定服务器接口
        self.s.listen(1) # 服务器进入监听模式
        self.wait_thread = threading.Thread()  # 定义wait_thread线程
        self.c = socket(AF_INET, SOCK_STREAM)  # 创建客户端接口

    # 创建连接，两种方式
    def build_connect(self):
        if self.start_OR_join == 1:  # 作为服务器时
            self.wait_thread = threading.Thread(target=self.waiting)  # 绑定wait_thread线程和waiting函数
            self.wait_thread.start()  # 启动子线程wait_thread
        elif self.start_OR_join == 2:  # 作为客户端时
            self.c.connect(ip_black_client)  # 连接至另一方服务器

    def waiting(self):
        print('Waiting')
        self.s.accept()  # 等待客户端连接
        # 修改标识符
        self.tag = 2  # 连接建立，进入游戏界面
        print('Start')


def main():

    # 初始化
    Black = Black_Side()

    # 主循环
    while True:

        ps_tag = Black.tag

        # 操作信息检测
        Black.tag = Black.check_movement()

        # 建立连接
        # 初始为0，事件检测后为1，启动游戏；初始为0，事件检测后为2，加入游戏
        if (Black.tag == 1 or Black.tag == 2) and ps_tag == 0:
            Black.build_connect()

        # tag由1变0，等待界面返回开始界面，停止连接等待进程
        if Black.tag == 0 and ps_tag == 1:
            Black.wait_thread._running = False

        # 背景绘制
        Black.bg_draw()

        # 显示screen内容
        Black.Update()


if __name__ == '__main__':
    main()
