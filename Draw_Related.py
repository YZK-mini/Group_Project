import pygame
import sys


# 初始化函数，供black和red调用
def init():
    global screen, start_img, wait_img, board_img, end_img, start_button1, start_button2, join_button1, join_button2, \
        retn_button1, retn_button2, red_return1, red_return2, red_exit1, red_exit2, black_return1, black_return2, \
        black_exit1, black_exit2, tag
    tag = 0

    # 初始化pygame
    pygame.init()

    # 创建窗口
    screen = pygame.display.set_mode((521, 577))

    # 背景图片
    start_img = pygame.image.load('images/开始界面.png')
    start_button1 = (128, 272)
    start_button2 = (390, 349)
    join_button1 = (126, 389)
    join_button2 = (389, 462)
    # 按钮’启动游戏‘左上（128，272）右下（390，349），
    # 按钮’加入游戏‘左上（126，389）右下（389，462）

    wait_img = pygame.image.load('images/等待界面.png')
    retn_button1 = (165, 313)
    retn_button2 = (340, 379)
    # 按钮'返回'左上（165，313）右下（340，379）

    board_img = pygame.image.load('images/棋盘.png')

    red_return1 = (115, 299)
    red_return2 = (394, 378)
    red_exit1 = (185, 435)
    red_exit2 = (331, 498)
    # 红方胜界面中，按钮’返回开始菜单‘左上（115，299）右下（394，378），
    # 按钮'退出'左上(185，435)右下（331，498）

    black_return1 = (114, 289)
    black_return2 = (377, 366)
    black_exit1 = (183, 419)
    black_exit2 = (318, 483)
    # 黑方胜界面中，按钮’返回开始菜单‘左上（114，289）右下（377，366），
    # 按钮'退出'左上(183，419)右下（318，483）


# 背景绘制，tg即tag
def bg_draw(tg):
    global start_img, wait_img, board_img, end_img

    # 背景绘制
    if tg == 0:
        # tag即tg为0时，开始界面，屏幕画上开始界面图片
        screen.blit(start_img, (0, 0))
    elif tg == 1:
        # tag即tg为1时，等待界面，屏幕画上等待界面图片
        screen.blit(wait_img, (0, 0))
    elif tg == 2:
        # tag即tg为2时，游戏界面，屏幕画上游戏界面图片
        screen.blit(board_img, (0, 0))
    elif tg == 30:
        # tag即tg为30时，红方胜界面，屏幕画上红方胜界面图片
        end_img = pygame.image.load('images/红方胜.png')
        screen.blit(end_img, (0, 0))
    elif tg == 31:
        # tag即tg为31时，黑方胜界面，屏幕画上黑方胜界面图片
        end_img = pygame.image.load('images/黑方胜.png')
        screen.blit(end_img, (0, 0))


# 当black与red建立连接后会调用此函数，将tag置为2，即双方进入游戏状态
def begin():
    global tag

    tag = 2


# 事件检测函数
def check_movement():
    global tag

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
                mouse_solve(pygame.mouse.get_pos())
                return tag
    return tag


# 鼠标事件处理函数
def mouse_solve(mouse_pos):
    global tag

    # 若处于开始界面
    if tag == 0:
        # 判断是否点击‘启动游戏’按钮
        if start_button1[0] < mouse_pos[0] < start_button2[0] and start_button1[1] < mouse_pos[1] < start_button2[1]:
            tag = 1
        # 判断是否点击‘加入游戏’按钮
        if join_button1[0] < mouse_pos[0] < join_button2[0] and join_button1[1] < mouse_pos[1] < join_button2[1]:
            tag = 2
    # 若处于等待界面
    if tag == 1:
        # 判断是否点击‘返回’按钮
        if retn_button1[0] < mouse_pos[0] < retn_button2[0] and retn_button1[1] < mouse_pos[1] < retn_button2[1]:
            tag = 0
    # 若处于结束界面
    if tag == 30:
        # 判断是否点击’返回开始界面‘按钮
        if red_return1[0] < mouse_pos[0] < red_return2[0] and red_return1[1] < mouse_pos[1] < red_return2[1]:
            tag = 0
        # 判断是否点击'退出'按钮
        if red_exit1[0] < mouse_pos[0] < red_exit2[0] and red_exit1[1] < mouse_pos[1] < red_exit2[1]:
            pygame.quit()
            sys.exit()
    if tag == 31:
        # 判断是否点击’返回开始界面‘按钮
        if black_return1[0] < mouse_pos[0] < black_return2[0] and black_return1[1] < mouse_pos[1] < black_return2[1]:
            tag = 0
        # 判断是否点击'退出'按钮
        if black_exit1[0] < mouse_pos[0] < black_exit2[0] and black_exit1[1] < mouse_pos[1] < black_exit2[1]:
            pygame.quit()
            sys.exit()


# 更新窗口内容
def Update():
    pygame.display.update()
