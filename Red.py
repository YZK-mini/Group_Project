import Connect_and_Side

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

        # 绑定服务器接口
        self.s.bind(ip_red_server)

        # 服务器进入监听模式
        self.s.listen(1)


def main():
    # 初始化
    red = RedSide()

    # 主循环
    while True:
        # 每次事件检测前的tag
        ps_tag = red.tag

        # 窗口刷新率设为60
        red.clock.tick(red.FPS)

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
