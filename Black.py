from socket import *
import Draw_Related
import threading
import pickle

# 当黑方发起游戏的ip地址
ip_black_server = ('127.0.0.1', 5000)  # 若联机，更改此处为本机ip及端口
# 当黑方加入游戏需要连接的ip地址
ip_black_client = ('127.0.0.1', 8000)  # 若联机，更改此处为对方主机ip及端口
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
        self.tg = 0
        self.chess_text = [[]]

    # 创建数据传输的类，需要本方的移动信息
    def create_mess(self, tag, chess_info):
        self.tg = tag
        self.chess_text = chess_info


# 红方类
class BlackSide(Draw_Related.DrawType):
    def __init__(self):
        super(BlackSide, self).__init__()

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

        # 绑定服务器接口
        self.s.bind(ip_black_server)

        # 服务器进入监听模式
        self.s.listen(1)

    # 创建连接，两种方式
    def build_connect(self):
        # 作为服务器时
        if self.start_or_join == 1:
            # 成为服务端
            self.s_or_c = 1

            # 绑定wait_thread线程和waiting函数
            self.wait_thread = threading.Thread(target=self.waiting)
            # 启动子线程wait_thread
            self.wait_thread.start()

        # 作为客户端时
        elif self.start_or_join == 2:
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
                try:
                    msg_s = pickle.loads(self.conn.recv(buf_size))
                    self.solve_rcv(msg_s)
                except pickle.UnpicklingError:
                    pass
            else:
                try:
                    msg_c = pickle.loads(self.c.recv(buf_size))
                    self.solve_rcv(msg_c)
                except pickle.UnpicklingError:
                    pass

    # 发送
    def send_info(self, msg):
        if self.start_or_join == 1:
            self.conn.send(pickle.dumps(msg))
        else:
            self.c.send(pickle.dumps(msg))

    def solve_rcv(self, msg):
        # 当接受到游戏结束信息，该信息是胜方发给败方的，因此结合本方颜色判断结束界面
        if msg.tg == 1 and self.side == 1:
            self.tag = 30
        elif msg.tg == 1 and self.side == 0:
            self.tag = 31

        # 收到对方认输信号
        if msg.tg == 2:
            temp_msg = Mess()
            temp_msg.create_mess(1, Black_chess_init)
            self.send_info(temp_msg)
            self.tag = 31

        # 收到请求和棋的信号
        if msg.tg == 3:
            self.tie = 2

        # 收到对方接受和棋的信号
        if msg.tg == 4:
            self.tie = 0
            self.tag = 32

        rcv_data = msg.chess_text
        print(rcv_data)
        # 换方需对矩阵进行180度旋转
        for i in range(5):
            for j in range(9):
                temp = rcv_data[i][j]
                rcv_data[i][j] = rcv_data[9 - i][8 - j]
                rcv_data[9 - i][8 - j] = temp
        # 如果接收到的棋盘与已有棋盘不同，则更新棋盘
        if self.chess_info != rcv_data:
            self.chess_info = rcv_data
            # 轮到己方行动
            self.able_move = 1


def main():
    # 初始化
    black = BlackSide()
    black.chess_info = Black_chess_init

    # 主循环
    while True:

        # 每次事件检测前的tag
        ps_tag = black.tag

        # 窗口刷新率设为60
        black.clock.tick(60)

        # 操作信息检测
        black.tag = black.check_movement()

        # 建立连接
        # 初始为0，事件检测后为1，启动游戏；初始为0，事件检测后为2，加入游戏
        if (black.tag == 1 or black.tag == 2) and ps_tag == 0 and black.start_or_join != 0:
            black.build_connect()

        # tag由1变0，等待界面返回开始界面，停止连接等待进程
        if black.tag == 0 and ps_tag == 1:
            black.wait_thread._running = False

        # 背景绘制
        black.bg_draw()

        # 创建传输信息
        msg = Mess()
        # 游戏结束瞬间
        if ps_tag == 2 and black.tag == 31:
            msg.create_mess(1, Black_chess_init)
            # 传输棋子信息矩阵
            black.send_info(msg)
        # 游戏重启
        elif (ps_tag == 30 or ps_tag == 31 or ps_tag == 32) and black.tag == 2:
            msg.create_mess(0, Black_chess_init)
            # 传输棋子信息矩阵
            black.send_info(msg)
            black.able_move = 0
        # 游戏其他时间
        else:
            msg.create_mess(0, black.chess_info)

        # 若为游戏界面
        if black.tag == 2:

            # 传输棋子信息矩阵
            if black.change:
                black.send_info(msg)
                black.change = 0

            # 若己方请求和棋
            if black.tie == 1:
                msg.create_mess(3, black.chess_info)
                black.send_info(msg)
                black.tie = 3

            # 若己方接受和棋
            if black.tie == 4:
                msg.create_mess(4, Black_chess_init)
                black.send_info(msg)
                black.tag = 32
                black.tie = 0

            # 若己方认输
            if black.surrender == 1:
                msg.create_mess(2, Black_chess_init)
                black.send_info(msg)
                black.surrender = 0

            # 绘制棋子
            black.draw_chess()

            # 绘制额外图片
            black.draw_picture()

        # 显示screen内容
        black.update()


if __name__ == '__main__':
    main()
