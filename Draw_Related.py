import pygame
import sys


class objection:
    # 初始化函数，供black和red调用
    def __init__(self):

        self.tag = 0
        self.start_OR_join = 0

        # 初始化pygame
        pygame.init()
        # 修改游戏窗口标题
        pygame.display.set_caption('中国象棋')
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
                self.tag = 1
                self.start_OR_join = 1
                return
            # 判断是否点击‘加入游戏’按钮
            if (self.join_button1[0] < mouse_pos[0] < self.join_button2[0]) and (
                    self.join_button1[1] < mouse_pos[1] < self.join_button2[1]):
                self.tag = 2
                self.start_OR_join = 2
                return

        # 若处于等待界面
        if self.tag == 1:
            # 判断是否点击‘返回’按钮
            if (self.return_button1[0] < mouse_pos[0] < self.return_button2[0]) and (
                    self.return_button1[1] < mouse_pos[1] < self.return_button2[1]):
                self.tag = 0
                return

        # 若处于结束界面
        if self.tag == 30:
            # 判断是否点击’返回开始界面‘按钮
            if (self.red_return1[0] < mouse_pos[0] < self.red_return2[0]) and (
                    self.red_return1[1] < mouse_pos[1] < self.red_return2[1]):
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
                self.tag = 0
                self.start_OR_join = 0
                return
            # 判断是否点击'退出'按钮
            if (self.black_exit1[0] < mouse_pos[0] < self.black_exit2[0]) and (
                    self.black_exit1[1] < mouse_pos[1] < self.black_exit2[1]):
                pygame.quit()
                sys.exit()

    # 更新窗口内容
    @staticmethod
    def Update():
        pygame.display.update()
