from copy import deepcopy
import Draw_and_Sound
import pickle
from socket import *
import threading


# 颜色方类
class Side(Draw_and_Sound.DrawType):

    def __init__(self):
        super(Side, self).__init__()
        # 连接的ip地址和端口
        self.ip_client = ('127.0.0.1', 7000)

        # 创建服务器接口
        self.s = socket(AF_INET, SOCK_STREAM)
        # 服务端标记的套接字
        self.conn = socket()

        # 定义wait_thread线程
        self.wait_thread = threading.Thread()
        # 创建客户端接口
        self.c = socket(AF_INET, SOCK_STREAM)

        # 定义receive线程
        self.receive_thread = threading.Thread()

        # 标记自身是服务端还是客户端， 0表示客户端， 1表示服务端
        self.s_or_c = 0

        # 传输大小
        self.buf_size = 1024

    # 用于传送数据的类
    class Mess:
        # 传输的数据内容
        def __init__(self):
            # 标记本条信息的属性，0表示普通传输，1表示游戏结束，2表示认输信号，3表示请求和棋信号，4表示回应和棋信号
            self.tg = 0
            # 棋子信息矩阵
            self.chess_text = None

        # 创建数据传输的类，需要本方的移动信息
        def create_mess(self, tag, temp_chess_info):
            self.tg = tag
            self.chess_text = deepcopy(temp_chess_info)

    # 初步连接处理
    def server_and_client(self, ps_tag):
        # 建立连接
        # 初始为0，事件检测后为1，启动游戏；初始为0，事件检测后为2，加入游戏
        if (self.tag == 1 or self.tag == 2) and ps_tag == 0:
            self.build_connect()

        # tag由1变0，等待界面返回开始界面，停止连接等待进程
        if self.tag == 0 and ps_tag == 1:
            self.wait_thread._running = False

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
            if self.side == 0:
                self.chess_info = deepcopy(self.red_chess_init)
                self.withdraw_situation = deepcopy(self.red_chess_init)
            else:
                self.chess_info = deepcopy(self.black_chess_init)
                self.withdraw_situation = deepcopy(self.black_chess_init)

            # 红方先行,黑方后行
            if self.side == 0:
                self.able_move = 1
            else:
                self.able_move = 0

            # 连接至另一方服务器
            try:
                self.c.connect(self.ip_client)
            except ConnectionRefusedError:
                print('连接失败')
                self.tag = 0
            print('Start')
            # 绑定receive_thread线程与receiver函数
            self.receive_thread = threading.Thread(target=self.receiver)
            # 启动receive线程
            self.receive_thread.start()

    # 与waiting线程绑定的wait函数，用于等待都覅那个连接
    def waiting(self):
        print('Waiting')
        # 等待客户端连接
        self.conn, addr = self.s.accept()

        # 连接建立，初始化棋子位置
        if self.side == 0:
            self.chess_info = deepcopy(self.red_chess_init)
            self.withdraw_situation = deepcopy(self.red_chess_init)
        else:
            self.chess_info = deepcopy(self.black_chess_init)
            self.withdraw_situation = deepcopy(self.black_chess_init)

        # 红方先行,黑方后行
        if self.side == 0:
            self.able_move = 1
        else:
            self.able_move = 0

        # 连接建立，进入游戏界面
        self.tag = 2
        # 播放开始音效
        self.start_music.play()

        print('Start')
        # 绑定receive_thread线程与receiver函数
        self.receive_thread = threading.Thread(target=self.receiver)
        # 启动receive线程
        self.receive_thread.start()

    # 发送
    def send_info(self, msg):
        if self.start_or_join == 1:
            self.conn.send(pickle.dumps(msg))
        else:
            self.c.send(pickle.dumps(msg))

    # 接收对方发来的棋子信息矩阵
    def receiver(self):
        while True:
            if self.s_or_c:
                try:
                    msg_s = pickle.loads(self.conn.recv(self.buf_size))
                    if self.tag == 2:
                        self.solve_rcv(msg_s)
                except pickle.UnpicklingError:
                    pass
            else:
                try:
                    msg_c = pickle.loads(self.c.recv(self.buf_size))
                    if self.tag == 2:
                        self.solve_rcv(msg_c)
                except pickle.UnpicklingError:
                    pass

    # 处理接受的信息
    def solve_rcv(self, msg):
        # 当接受到游戏结束信息，该信息是胜方发给败方的，因此结合本方颜色判断结束界面
        if msg.tg == 1:
            self.lose = 1
            if self.side == 1:
                self.tag = 30
            else:
                self.tag = 31
            return

        # 收到对方认输信号
        elif msg.tg == 2:

            temp_msg = Side.Mess()

            if self.side == 0:
                self.tag = 30
            else:
                self.tag = 31

            temp_msg.create_mess(1, self.chess_info)
            self.send_info(temp_msg)

            return

        # 收到请求和棋的信号
        elif msg.tg == 3:
            self.tie = 2
            return

        # 收到对方接受和棋的信号
        elif msg.tg == 4:
            self.tag = 32
            return

        # 收到对方将军的信号
        elif msg.tg == 5:
            self.warn = 1
            # 将军提示音
            self.warn_music.play()
            return

        # 收到对方悔棋的信号
        elif msg.tg == 6:
            self.able_move = 0

        rcv_data = deepcopy(msg.chess_text)

        # 换方需对矩阵进行180度旋转
        for i in range(5):
            for j in range(9):
                temp = rcv_data[i][j]
                rcv_data[i][j] = rcv_data[9 - i][8 - j]
                rcv_data[9 - i][8 - j] = temp

        # 如果接收到的棋盘与已有棋盘不同，则更新棋盘
        if self.chess_info != rcv_data and self.tag == 2:
            self.chess_info = deepcopy(rcv_data)
            self.move_music.play()
            # 若本次修改不是对方悔棋的结果，则轮到己方行动
            if msg.tg != 6:
                self.able_move = 1
            # 当对方行走后，无法悔棋
            self.withdraw_situation = deepcopy(self.chess_info)

        return

    # 交互和绘制相关
    def interact_and_draw(self, ps_tag):
        # 创建信息
        msg = Side.Mess()

        # 游戏结束瞬间
        if ps_tag == 2 and (self.tag == 30 or self.tag == 31 or self.tag == 32) and self.lose != 1:

            # 发送结束信息
            msg.create_mess(1, self.chess_info)

            # 播放结束音效
            self.end_music.play()
            # 传输棋子信息矩阵
            self.send_info(msg)

        # 游戏重启
        elif (ps_tag == 30 or ps_tag == 31 or ps_tag == 32) and self.tag == 2:
            # 还原棋盘
            if self.side == 0:
                self.chess_info = deepcopy(self.red_chess_init)
                self.able_move = 1
            else:
                self.chess_info = deepcopy(self.black_chess_init)
                self.able_move = 0

            return

        # 游戏其他时间
        else:
            msg.create_mess(0, self.chess_info)

        # 若为游戏界面
        if self.tag == 2:

            # 传输棋子信息矩阵
            if self.change == 1:
                self.send_info(msg)
                self.change = 0

            # 若己方请求和棋
            if self.tie == 1:
                msg.create_mess(3, self.chess_info)
                self.send_info(msg)
                self.tie = 3

            # 若己方接受和棋
            if self.tie == 4:
                msg.create_mess(4, self.chess_info)
                self.send_info(msg)
                self.tag = 32

            # 若己方认输
            if self.surrender == 1:
                msg.create_mess(2, self.chess_info)
                self.send_info(msg)

            # 若将军
            if self.warn == 1 and self.times == 1:
                msg.create_mess(5, self.chess_info)
                self.send_info(msg)

            # 若悔棋
            if self.undo == 1:
                self.chess_info = deepcopy(self.withdraw_situation)
                self.undo = 0
                self.able_move = 1
                msg.create_mess(6, self.chess_info)
                self.send_info(msg)

            # 绘制棋子
            self.draw_chess()

            # 绘制额外图片
            self.draw_picture()
