import pygame
import sys
import time


# 初始化函数，供black和red调用
def init():
    global screen, start_img, wait_img, board_img, end_img

    # 初始化pygame
    pygame.init()
    # 创建窗口
    screen = pygame.display.set_mode((521, 577))
    # 背景图片
    start_img = pygame.image.load('images/开始界面.png')
    # 按钮’启动游戏‘左上（128，272）右下（390，349），按钮’加入游戏‘左上（126，380）右下（389，457）
    wait_img = pygame.image.load('images/等待界面.png')
    board_img = pygame.image.load('images/棋盘.png')
    # 红方胜界面中，按钮’返回开始菜单‘左上（115，299）右下（394，378），按钮'退出'左上(185，435)右下（331，498）
    end_img = pygame.image.load('images/红方胜.png')
    # 黑方胜界面中，按钮’返回开始菜单‘左上（114，289）右下（377，366），按钮'退出'左上(183，419)右下（318，483）


# 背景绘制
def bg_draw():
    global tag
    # 背景绘制
    if tag == 0:
        screen.blit(start_img, (0, 0))
    elif tag == 1:
        screen.blit(wait_img, (0, 0))
    elif tag == 2:
        screen.blit(board_img, (0, 0))
    elif tag == 3:
        screen.blit(end_img, (0, 0))


# 更新窗口内容
def Update():
    pygame.display.update()

