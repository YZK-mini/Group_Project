from socket import *
import Draw_Related
import threading
import pickle

# 当黑方发起游戏的ip地址
ip_black_server = ('127.0.0.1', 5000)
# 当黑方加入游戏需要连接的ip地址
ip_black_client = ('127.0.0.1', 8000)
# 传输的尺寸限制
buf_size = 512
# 黑方初始棋子位置
Black_chess_init = [
    [1, 2, 3, 4, 5, 4, 3, 2, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 6, 0, 0, 0, 0, 0, 6, 0],
    [7, 0, 7, 0, 7, 0, 7, 0, 7],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [17, 0, 17, 0, 17, 0, 17, 0, 17],
    [0, 16, 0, 0, 0, 0, 0, 16, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [11, 12, 13, 14, 15, 14, 13, 12, 11],
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
class Black_Side(Draw_Related.objection):
    def __init__(self):
        super(Black_Side, self).__init__()
        # 表明自己为黑方
        self.side = 1
        # 创建服务器接口
        self.s = socket(AF_INET, SOCK_STREAM)
        self.conn = socket()

        # 定义wait_thread线程
        self.wait_thread = threading.Thread()
        # 创建客户端接口
        self.c = socket(AF_INET, SOCK_STREAM)

        # 定义receive线程
        self.receive_thread = threading.Thread()

        # 标记自身是服务端还是客户端， 0表示客户端， 1表示服务端
        self.s_or_c = 0

    # 创建连接，两种方式
    def build_connect(self):
        # 作为服务器时
        if self.start_OR_join == 1:
            # 成为服务端
            self.s_or_c = 1
            # 绑定服务器接口
            self.s.bind(ip_black_server)
            # 服务器进入监听模式
            self.s.listen(1)
            # 绑定wait_thread线程和waiting函数
            self.wait_thread = threading.Thread(target=self.waiting)
            # 启动子线程wait_thread
            self.wait_thread.start()

        # 作为客户端时
        elif self.start_OR_join == 2:
            # 成为客户端
            self.s_or_c = 0
            # 初始化棋子位置
            self.chess_info = Black_chess_init
            # 黑方后行
            self.able_move = 0
            # 连接至另一方服务器
            try:
                self.c.connect(ip_black_client)
            except ConnectionRefusedError:
                print('连接失败')
                self.tag = 0
            print('Start')
            # 绑定receive_thread线程与receiver函数
            self.receive_thread = threading.Thread(target=self.receiver)
            # 启动receive线程
            self.receive_thread.start()

    def waiting(self):
        print('Waiting')
        # 等待客户端连接
        self.conn, addr = self.s.accept()
        # 连接建立，初始化棋子位置
        self.chess_info = Black_chess_init
        # 黑方后行
        self.able_move = 0
        # 连接建立，进入游戏界面
        self.tag = 2

        print('Start')
        # 绑定receive_thread线程与receiver函数
        self.receive_thread = threading.Thread(target=self.receiver)
        # 启动receive线程
        self.receive_thread.start()

    # 接收对方发来的棋子信息矩阵，并做简单处理
    def receiver(self):
        while True:
            # 接收信息存入rcv_data
            if self.s_or_c:
                rcv_data: list[list[int]] = pickle.loads(self.conn.recv(buf_size))
            else:
                rcv_data: list[list[int]] = pickle.loads(self.c.recv(buf_size))
            # 换方需对矩阵进行180度旋转
            for i in range(5):
                for j in range(9):
                    temp = rcv_data[i][j]
                    rcv_data[i][j] = rcv_data[9 - i][8 - j]
                    rcv_data[9 - i][8 - j] = temp
            if self.chess_info != rcv_data:
                self.chess_info = rcv_data
                # 轮到己方行动
                self.able_move = 1


def main():
    # 初始化
    Black = Black_Side()

    # 主循环
    while True:

        ps_tag = Black.tag
        Black.clock.tick(60)

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

        # 若为游戏界面
        if Black.tag == 2:

            # 传输棋子信息矩阵
            if Black.s_or_c:
                Black.conn.sendall(pickle.dumps(Black.chess_info))
            else:
                Black.c.sendall(pickle.dumps(Black.chess_info))

            # 绘制棋子
            Black.draw_chess()

        # 显示screen内容
        Black.Update()


if __name__ == '__main__':
    main()
