from socket import *
import Connect_and_Side
import threading

# 当红方发起游戏的ip地址
ip_red_server = ('127.0.0.1', 5000)  # 若联机，更改此处为本机ip及端口
# 当红方参加游戏需要连接的ip地址
ip_red_client = ('127.0.0.1', 8000)  # 若联机，更改此处为对方主机ip及端口


# 红方类
class RedSide(Connect_and_Side.Side):
    def __init__(self):
        super(RedSide, self).__init__()

        # 表明自己为红方
        self.side = 0

        # 重新赋值要连接的ip和端口
        self.ip_client = ip_red_client

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


def main():
    # 初始化
    red = RedSide()
    red.chess_info = red.Red_chess_init

    # 主循环
    while True:
        # 每次事件检测前的tag
        ps_tag = red.tag

        # 窗口刷新率设为60
        red.clock.tick(60)

        # 操作信息检测
        red.tag = red.check_movement()

        # 联机功能
        red.server_and_client(ps_tag)

        # 背景绘制
        red.bg_draw()

        # 游戏全过程的交互和实体绘制
        red.interact_and_draw(ps_tag)

        # 显示screen内容
        red.update()


if __name__ == '__main__':
    main()
