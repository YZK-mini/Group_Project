from socket import *
import Draw_Related
import threading

# 当红方发起游戏的ip地址
ip_red_server = ('127.0.0.1', 8000)
# 当红方参加游戏需要连接的ip地址
ip_red_client = ('127.0.0.1', 5000)
# 传输的尺寸限制
buf_size = 512
# 红方初始棋子位置
Red_chess_init = [
    [11, 12, 13, 14, 15, 14, 13, 12, 11],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 16, 0, 0, 0, 0, 0, 16, 0],
    [17, 0, 17, 0, 17, 0, 17, 0, 17],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [7, 0, 7, 0, 7, 0, 7, 0, 7],
    [0, 6, 0, 0, 0, 0, 0, 6, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 2, 3, 4, 5, 4, 3, 2, 1],
]


# 用于传送数据的类
class Mess:
    def __init__(self):
        self.beforeX = 0
        self.beforeY = 0
        self.afterX = 0
        self.afterY = 0

    # 创建数据传输的类，需要本方的移动信息
    def create_Mess(self, Pox, PoY, CuX, CuY):
        self.beforeX = Pox
        self.beforeY = PoY
        self.afterX = CuX
        self.afterY = CuY


# 红方类
class Red_Side(Draw_Related.objection):
    def __init__(self):
        super(Red_Side, self).__init__()
        # 表明自己为红方
        self.side = 0
        # 创建服务器接口
        self.s = socket(AF_INET, SOCK_STREAM)

        # 定义wait_thread线程
        self.wait_thread = threading.Thread()
        # 创建客户端接口
        self.c = socket(AF_INET, SOCK_STREAM)

    # 创建连接，两种方式
    def build_connect(self):
        # 作为服务器时
        if self.start_OR_join == 1:
            # 绑定服务器接口
            self.s.bind(ip_red_server)
            # 服务器进入监听模式
            self.s.listen(1)
            # 绑定wait_thread线程和waiting函数
            self.wait_thread = threading.Thread(target=self.waiting)
            # 启动子线程wait_thread
            self.wait_thread.start()

        # 作为客户端时
        elif self.start_OR_join == 2:
            # 初始化棋子位置
            self.chess_info = Red_chess_init
            # 红方先行
            self.able_move = 1
            # 连接至另一方服务器
            try:
                self.c.connect(ip_red_client)
            except ConnectionRefusedError:
                print('连接失败')
                self.tag = 0
            print('Start')

    def waiting(self):
        print('Waiting')
        # 等待客户端连接
        self.s.accept()
        # 连接建立，初始化棋子位置
        self.chess_info = Red_chess_init
        # 红方先行
        self.able_move = 1
        # 连接建立，进入游戏界面
        self.tag = 2

        print('Start')


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

        # 背景绘制
        Red.bg_draw()

        # 若为游戏界面
        if Red.tag == 2:
            # 绘制棋子
            Red.draw_chess()

        # 显示screen内容
        Red.Update()


if __name__ == '__main__':
    main()
