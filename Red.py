from socket import *
import Draw_Related
import threading
import pickle

# 当红方发起游戏的ip地址
ip_red_server = ('127.0.0.1', 8000)  # 若联机，更改此处为本机ip及端口
# 当红方参加游戏需要连接的ip地址
ip_red_client = ('127.0.0.1', 5000)  # 若联机，更改此处为对方主机ip及端口
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
        self.tg = 1
        self.chess_text = [[]]

    # 创建数据传输的类，需要本方的移动信息
    def create_mess(self, tag, chess_info):
        self.tg = tag
        self.chess_text = chess_info


# 红方类
class RedSide(Draw_Related.DrawType):
    def __init__(self):
        super(RedSide, self).__init__()

        # 表明自己为红方
        self.side = 0
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
        self.s.bind(ip_red_server)

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
            # 绑定receive_thread线程与receiver函数
            self.receive_thread = threading.Thread(target=self.receiver)
            # 启动receive线程
            self.receive_thread.start()

    def waiting(self):
        print('Waiting')
        # 等待客户端连接
        self.conn, addr = self.s.accept()
        # 连接建立，初始化棋子位置
        self.chess_info = Red_chess_init
        # 红方先行
        self.able_move = 1
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
            temp_msg.create_mess(1, Red_chess_init)
            self.send_info(temp_msg)
            self.tag = 30

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
    red = RedSide()
    red.chess_info = Red_chess_init

    # 主循环
    while True:

        # 每次事件检测前的tag
        ps_tag = red.tag

        # 窗口刷新率设为60
        red.clock.tick(60)

        # 操作信息检测
        red.tag = red.check_movement()

        # 建立连接
        # 初始为0，事件检测后为1，启动游戏；初始为0，事件检测后为2，加入游戏
        if (red.tag == 1 or red.tag == 2) and ps_tag == 0:
            red.build_connect()

        # tag由1变0，等待界面返回开始界面，停止连接等待进程
        if red.tag == 0 and ps_tag == 1:
            red.wait_thread._running = False

        # 背景绘制
        red.bg_draw()

        # 创建传输信息
        msg = Mess()
        # 游戏结束瞬间
        if ps_tag == 2 and red.tag == 30:
            msg.create_mess(1, Red_chess_init)
            # 传输棋子信息矩阵
            red.send_info(msg)
        # 游戏重启
        elif (ps_tag == 30 or ps_tag == 31 or ps_tag == 32) and red.tag == 2:
            msg.create_mess(0, Red_chess_init)
            # 传输棋子信息矩阵
            red.send_info(msg)
        # 游戏其他时间
        else:
            msg.create_mess(0, red.chess_info)

        # 若为游戏界面
        if red.tag == 2:
            # 传输棋子信息矩阵
            if red.change:
                red.send_info(msg)
                red.change = 0

            # 若己方请求和棋
            if red.tie == 1:
                msg.create_mess(3, red.chess_info)
                red.send_info(msg)
                red.tie = 3

            # 若己方接受和棋
            if red.tie == 4:
                msg.create_mess(4, Red_chess_init)
                red.send_info(msg)
                red.tag = 32
                red.tie = 0

            # 若己方认输
            if red.surrender == 1:
                msg.create_mess(2, Red_chess_init)
                red.send_info(msg)
                red.surrender = 0

            # 绘制棋子
            red.draw_chess()

            # 绘制额外图片
            red.draw_picture()

        # 显示screen内容
        red.update()


if __name__ == '__main__':
    main()
