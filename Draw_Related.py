import pygame
import sys
import math

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


# 将网格位置转化为窗口坐标
def Pos2load(posX, posY):
    return 57.5 * posX + 2.5, 57.5 * posY + 2.5


# 点击坐标转换为棋子位置
def Co2Pos(coX, coY):
    x = coX // 57.5
    x = x if x >= 0 else 0
    x = x if x <= 8 else 8
    x = math.floor(x)
    y = coY // 57.5
    y = y if y >= 0 else 0
    y = y if y <= 9 else 9
    y = math.floor(y)
    return x, y


class objection:
    # 初始化函数，供black和red调用
    def __init__(self):
        # 红方或黑方标志，0表示红方，1表示黑方
        self.side = 0
        # 游戏进行状态标识，0表示开始界面，1表示等待界面，2表示游戏界面，3表示结束界面
        self.tag = 0
        # 开始界面按钮标识，0表示未选，1表示选择‘启动游戏’，2表示选择‘加入游戏’
        self.start_OR_join = 0
        # 选中的位置
        self.choice = (-1, -1)
        # 当前选中位置
        self.cur = (-1, -1)
        # 后选中位置
        self.choice2 = (-1, -1)
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
        self.screen = pygame.display.set_mode((521, 577))

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

        self.board_img = pygame.image.load('images/棋盘.png')

        self.end_img = 0

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

        self.block_image = pygame.image.load('images/四方形标志.png')

        # 棋子初始坐标
        self.chess_info = None

    # 背景绘制，tg即tag
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
                self.start_OR_join = 1
                return
            # 判断是否点击‘加入游戏’按钮
            if (self.join_button1[0] < mouse_pos[0] < self.join_button2[0]) and (
                    self.join_button1[1] < mouse_pos[1] < self.join_button2[1]):
                # 修改标识符
                self.start_OR_join = 2
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
            # 判断点击的是哪一个棋子
            self.cur = Co2Pos(mouse_pos[0], mouse_pos[1])
            # 若为空处并且没有选中图片无反应；若为空处并且已经选中则移动图片
            if self.chess_info[self.cur[1]][self.cur[0]] == 0 and self.image_selected is False:
                print('?')
                pass
            elif self.chess_info[self.cur[1]][self.cur[0]] == 0 and self.image_selected is True:
                self.move_chess()
            # 若为对方棋子，或未到本方下棋，则无反应
            elif self.side != math.floor(self.chess_info[self.cur[1]][self.cur[0]] / 10):
                print('no')
                pass
            elif self.able_move == 0:
                print('wait')
                pass
            # 若为己方棋子，且轮到本方下棋则显示选中
            else:
                self.choice = Pos2load(self.cur[0], self.cur[1])
                self.choice2 = self.cur  # 用于保存已经选择的棋子信息
                self.image_selected = True  # 是否选中图片的标志

        # 若处于结束界面
        if self.tag == 30:
            # 判断是否点击’返回开始界面‘按钮
            if (self.red_return1[0] < mouse_pos[0] < self.red_return2[0]) and (
                    self.red_return1[1] < mouse_pos[1] < self.red_return2[1]):
                # 修改标识符
                self.tag = 0
                self.start_OR_join = 0
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
                self.tag = 0
                self.start_OR_join = 0
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
                    self.screen.blit(temp_image, Pos2load(j, i))
        # 正确选择的位置出现蓝色四方形框
        if self.choice != (-1, -1):
            self.screen.blit(self.block_image, self.choice)

    # 移动棋子到对应位置
    def move_chess(self):
        # 交换棋子信息矩阵中前后位置的值，实现移动（此处应有判断能否进行的条件，在Chesses中实现，再import）
        chess = self.chess_info[self.choice2[1]][self.choice2[0]]
        self.chess_info[self.choice2[1]][self.choice2[0]] = 0
        self.chess_info[self.cur[1]][self.cur[0]] = chess
        # 轮到对方行动
        self.able_move = 0
        # 走完后，当前无选中位置
        self.image_selected = False
        self.choice = (-1, -1)

    # 更新窗口内容
    @staticmethod
    def Update():
        pygame.display.update()
