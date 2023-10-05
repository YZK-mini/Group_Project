import math
import pygame
import sys
import Chess

# 棋子及其对应数字标识
chess_number = {
    1: 'images/红车.png',
    2: 'images/红马.png',
    3: 'images/红相.png',
    4: 'images/红仕.png',
    5: 'images/红帅.png',
    6: 'images/红炮.png',
    7: 'images/红兵.png',

    11: 'images/黑车.png',
    12: 'images/黑马.png',
    13: 'images/黑象.png',
    14: 'images/黑士.png',
    15: 'images/黑将.png',
    16: 'images/黑炮.png',
    17: 'images/黑卒.png',
}
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


# 将网格位置转化为窗口坐标
def grid_to_pos(pos_x, pos_y):
    # 每个格子距离57.5，为了实际显示效果作了2.5的偏移
    return 57.5 * pos_y + 2.5, 57.5 * pos_x + 2.5


# 点击坐标转换为网格位置
def pos_to_grid(co_x, co_y):
    x = co_x // 57.5
    x = x if x >= 0 else 0
    x = x if x <= 8 else 8
    x = math.floor(x)

    y = co_y // 57.5
    y = y if y >= 0 else 0
    y = y if y <= 9 else 9
    y = math.floor(y)

    return y, x


class DrawType:
    # 初始化函数
    def __init__(self):
        # 红方或黑方标志，0表示红方，1表示黑方
        self.side = 0
        # 游戏进行状态标识，0表示开始界面，1表示等待界面，2表示游戏界面，3表示结束界面
        self.tag = 0
        # 开始界面按钮标识，0表示未选，1表示选择‘启动游戏’，2表示选择‘加入游戏’
        self.start_or_join = 0

        # 选中的位置
        self.choice = (-1, -1)
        # 当前选中位置
        self.cur = (-1, -1)
        # 后选中位置
        self.choice_ready = (-1, -1)
        # 行动标志，0 表示不可行动，1 表示可行动
        self.able_move = 0
        # 选中棋子图片标志
        self.image_selected = None

        # 初始化pygame
        pygame.init()
        # 控制帧率
        self.clock = pygame.time.Clock()
        # 修改游戏窗口标题
        pygame.display.set_caption('中国象棋')
        # 修改游戏窗口图标
        icon = pygame.image.load("images/图标.png")
        pygame.display.set_icon(icon)
        # 创建窗口
        self.screen = pygame.display.set_mode((521, 640))

        # 背景图片
        self.start_img = pygame.image.load('images/开始界面.png')
        self.start_button1 = (128, 272)
        self.start_button2 = (390, 349)
        self.join_button1 = (126, 389)
        self.join_button2 = (389, 462)
        # 按钮’启动游戏‘左上（128，272）右下（390，349），按钮’加入游戏‘左上（126，389）右下（389，462）

        self.wait_img = pygame.image.load('images/等待界面.png')
        self.return_button1 = (165, 313)
        self.return_button2 = (340, 379)
        # 按钮'返回'左上（165，313）右下（340，379）

        # 棋盘界面图片
        self.board_img = pygame.image.load('images/棋盘.png')

        self.surrender_button1 = (385, 586)
        self.surrender_button2 = (510, 633)
        # 按钮‘认输’左上(385，586)，右下(510,633)
        self.tie_button1 = (243, 586)
        self.tie_button2 = (370, 633)
        # 按钮‘和棋’左上（243，586），右下（370，633）

        # 结束界面图片
        self.end_img = None

        self.red_return1 = (115, 299)
        self.red_return2 = (394, 378)
        self.red_exit1 = (185, 435)
        self.red_exit2 = (331, 498)
        # 红方胜界面中，按钮’返回开始菜单‘左上（115，299）右下（394，378），按钮'退出'左上(185，435)右下（331，498）
        self.black_return1 = (114, 289)
        self.black_return2 = (377, 366)
        self.black_exit1 = (183, 419)
        self.black_exit2 = (318, 483)
        # 黑方胜界面中，按钮’返回开始菜单‘左上（114，289）右下（377，366），按钮'退出'左上(183，419)右下（318，483）

        # 选中棋子显示的标志
        self.block_image = pygame.image.load('images/四方形标志.png')

        # 走棋提示
        self.tip_image = pygame.image.load('images/提示.png')

        # 当前选中棋子可移动位置
        self.can_moves = []

        # 棋子初始坐标
        self.chess_info = None

        # 棋子移动标识
        self.change = 0

        # 求和标识
        self.tie = 0
        # 和棋提示
        self.surrender_image = pygame.image.load('images/求和提示.png')
        self.surrender_pos = (18, 590)

        # 认输标识
        self.surrender = 0

    # 背景绘制
    def bg_draw(self):
        # 背景绘制
        if self.tag == 0:
            # tag为0时，开始界面，屏幕画上开始界面图片
            self.screen.blit(self.start_img, (0, 0))
        elif self.tag == 1:
            # tag为1时，等待界面，屏幕画上等待界面图片
            self.screen.blit(self.wait_img, (0, 0))
        elif self.tag == 2:
            # tag为2时，游戏界面，屏幕画上游戏界面图片
            self.screen.blit(self.board_img, (0, 0))
        elif self.tag == 30:
            # tag为30时，红方胜界面，屏幕画上红方胜界面图片
            self.end_img = pygame.image.load('images/红方胜.png')
            self.screen.blit(self.end_img, (0, 0))
        elif self.tag == 31:
            # tag为31时，黑方胜界面，屏幕画上黑方胜界面图片
            self.end_img = pygame.image.load('images/黑方胜.png')
            self.screen.blit(self.end_img, (0, 0))

    # 事件检测函数
    def check_movement(self):

        # 事件检测
        for event in pygame.event.get():
            # 退出事件
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # 鼠标点击事件
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 获取鼠标点击坐标
                mouse_presses = pygame.mouse.get_pressed()
                if mouse_presses[0]:
                    # 调用鼠标事件处理函数，传入鼠标坐标
                    self.mouse_solve(pygame.mouse.get_pos())
                    return self.tag

        return self.tag

    # 鼠标事件处理函数
    def mouse_solve(self, mouse_pos):

        # 若处于开始界面
        if self.tag == 0:
            # 判断是否点击‘启动游戏’按钮
            if (self.start_button1[0] < mouse_pos[0] < self.start_button2[0]) and (
                    self.start_button1[1] < mouse_pos[1] < self.start_button2[1]):
                # 修改标识符
                self.tag = 1
                self.start_or_join = 1
                return
            # 判断是否点击‘加入游戏’按钮
            if (self.join_button1[0] < mouse_pos[0] < self.join_button2[0]) and (
                    self.join_button1[1] < mouse_pos[1] < self.join_button2[1]):
                # 修改标识符
                self.start_or_join = 2
                self.tag = 2
                return

        # 若处于等待界面
        if self.tag == 1:
            # 判断是否点击‘返回’按钮
            if (self.return_button1[0] < mouse_pos[0] < self.return_button2[0]) and (
                    self.return_button1[1] < mouse_pos[1] < self.return_button2[1]):
                # 修改标识符
                self.tag = 0
                return

        # 若处于游戏界面
        if self.tag == 2:
            # 判断点击的是哪一个格子
            self.cur = pos_to_grid(mouse_pos[0], mouse_pos[1])

            # 若点击'和棋'按钮
            if (self.tie_button1[0] < mouse_pos[0] < self.tie_button2[0]) and (
                    self.tie_button1[1] < mouse_pos[1] < self.tie_button2[1]):
                self.tie = 1

            # 若点击'认输'按钮
            if (self.surrender_button1[0] < mouse_pos[0] < self.surrender_button2[0]) and (
                    self.surrender_button1[1] < mouse_pos[1] < self.surrender_button2[1]):
                self.surrender = 1

            # 若未轮到本方
            if self.able_move == 0:
                print('请等待对方下棋')
                pass

            # 若为空处
            elif self.chess_info[self.cur[0]][self.cur[1]] == 0:
                # 若已选中本方棋子，则移动
                if self.image_selected:
                    self.move_chess()
                # 若没有选中图片，则无反应
                else:
                    print('空白处')
                    pass

            # 若选中对方棋子
            elif self.side != self.chess_info[self.cur[0]][self.cur[1]] // 10:
                # 若已选中本方棋子，则移动吞并
                if self.image_selected:
                    self.move_chess()
                # 若之前未选中本方棋子，则无反应
                else:
                    print('不是你的棋子')
                    pass

            # 若为己方棋子，且未选中，且轮到本方下棋则显示选中
            else:
                self.choice = grid_to_pos(self.cur[0], self.cur[1])
                self.choice_ready = self.cur  # 用于保存已经选择的棋子信息
                self.image_selected = True  # 是否选中图片的标志

        # 若处于结束界面
        if self.tag == 30:
            # 判断是否点击’再来一局‘按钮
            if (self.red_return1[0] < mouse_pos[0] < self.red_return2[0]) and (
                    self.red_return1[1] < mouse_pos[1] < self.red_return2[1]):
                # 修改标识符
                self.tag = 2
                # 还原棋盘
                if self.side == 0:
                    self.chess_info = Red_chess_init
                    self.able_move = 1
                else:
                    self.chess_info = Black_chess_init
                    self.able_move = 0
                self.choice = (-1, -1)
                self.image_selected = False
                return

            # 判断是否点击'退出'按钮
            if (self.red_exit1[0] < mouse_pos[0] < self.red_exit2[0]) and (
                    self.red_exit1[1] < mouse_pos[1] < self.red_exit2[1]):
                pygame.quit()
                sys.exit()

        if self.tag == 31:
            # 判断是否点击’返回开始界面‘按钮
            if (self.black_return1[0] < mouse_pos[0] < self.black_return2[0]) and (
                    self.black_return1[1] < mouse_pos[1] < self.black_return2[1]):
                # 修改标识符
                self.tag = 2
                # 还原棋盘
                if self.side == 0:
                    self.chess_info = Red_chess_init
                    self.able_move = 1
                else:
                    self.chess_info = Black_chess_init
                    self.able_move = 0
                self.choice = (-1, -1)
                self.image_selected = False
                return

            # 判断是否点击'退出'按钮
            if (self.black_exit1[0] < mouse_pos[0] < self.black_exit2[0]) and (
                    self.black_exit1[1] < mouse_pos[1] < self.black_exit2[1]):
                pygame.quit()
                sys.exit()

    # 绘制棋子
    def draw_chess(self):
        # 根据棋子信息矩阵绘制每一个棋子
        for i in range(10):
            for j in range(9):
                # 该位置为空，跳过
                if self.chess_info[i][j] == 0:
                    continue
                # 该位置不为空，在chess_number字典中查找该棋子对应图片的文件名，并绘制
                else:
                    temp_image = pygame.image.load(chess_number.get(self.chess_info[i][j]))
                    self.screen.blit(temp_image, grid_to_pos(i, j))
        # 正确选择的位置出现蓝色四方形框
        if self.choice != (-1, -1):
            self.screen.blit(self.block_image, self.choice)

        if self.image_selected:
            # 已选中的棋子位置
            cur_pos = (self.choice_ready[0], self.choice_ready[1])
            # 可以移动的位置列表
            self.can_moves = Chess.where_can_move(self.chess_info, cur_pos)
            # 绘制移动提示
            for grid in self.can_moves:
                position = grid_to_pos(grid[0], grid[1])
                self.screen.blit(self.tip_image, (position[0] + 17.5, position[1] + 17.5))

    # 移动棋子到对应位置
    def move_chess(self):

        # 想要移动的位置
        next_pos = (self.cur[0], self.cur[1])

        print(f'可以移动的位置:{self.can_moves}')
        print(f'选择移动的位置:{self.cur}')

        # 判断能否走子
        if next_pos in self.can_moves:
            # 判断是否将或帅被吃
            if self.chess_info[next_pos[0]][next_pos[1]] == 5:
                print('帅已死')
                self.tag = 31
            if self.chess_info[next_pos[0]][next_pos[1]] == 15:
                print('将已死')
                self.tag = 30

            # 若想要移动的位置在可以移动的位置列表内，则执行吃子或移动
            chess = self.chess_info[self.choice_ready[0]][self.choice_ready[1]]
            self.chess_info[self.choice_ready[0]][self.choice_ready[1]] = 0
            self.chess_info[self.cur[0]][self.cur[1]] = chess

            # 走完后，当前无选中位置
            self.change = 1
            self.image_selected = False
            self.choice = (-1, -1)
            # 轮到对方行动
            self.able_move = 0

        else:
            # 想要移动的位置不在可以移动的位置列表内，则无反应
            print('不能移动到此处')
            pass

    # 更新窗口内容
    @staticmethod
    def update():
        pygame.display.update()
