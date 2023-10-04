def che_check(ChessInfo, cur_grid, cur_chess_num):
    curCanMove = []
    side = cur_chess_num // 10
    # 扫描当前行可移动位置
    tempY = cur_grid[1] - 1
    # 向左遍历
    offSetY = -1
    while True:
        if tempY < 0:
            tempY = cur_grid[1] + 1
            # 碰到左边界，回到原先位置右侧，调头向右
            offSetY = 1
            continue
        # 碰到右边界，退出
        elif tempY > 8:
            break
        tempChess = ChessInfo[cur_grid[0]][tempY]
        # 判断为空棋子;空棋子加入可移动列表
        if tempChess == 0:
            curCanMove.append((cur_grid[0], tempY))
        else:
            # 非空棋子为敌方，则掉头并加入可移动列表
            if side != tempChess // 10:
                curCanMove.append((cur_grid[0], tempY))

            # 已经调过头；直接退出
            if offSetY == 1:
                break

            tempY = cur_grid[1]
            # 调头
            offSetY = 1
        tempY += offSetY

    # 扫描当前列可移动的位置，逻辑类似上方
    tempX = cur_grid[0] - 1
    offSetX = -1
    while True:
        if tempX < 0:
            tempX = cur_grid[0] + 1
            offSetX = 1
            continue
        elif tempX > 9:
            break
        tempChess = ChessInfo[tempX][cur_grid[1]]
        if tempChess == 0:
            curCanMove.append((tempX, cur_grid[1]))
        else:
            if side != tempChess // 10:
                curCanMove.append((tempX, cur_grid[1]))

            if offSetX == 1:
                break

            tempX = cur_grid[0]
            offSetX = 1
        tempX += offSetX

    return curCanMove


def horse_check(ChessInfo, cur_grid, cur_chess_num):
    curCanMove = []
    side = cur_chess_num // 10
    # 向上走;没顶格，没被棋子挡住马脚
    if cur_grid[0] >= 2 and ChessInfo[cur_grid[0] - 1][cur_grid[1]] == 0:
        # 左上;向上两格，向左一格
        if cur_grid[1] >= 1:
            tempChess = ChessInfo[cur_grid[0] - 2][cur_grid[1] - 1]
            if side != tempChess // 10 or tempChess == 0:
                curCanMove.append((cur_grid[0] - 2, cur_grid[1] - 1))
        # 右上;向上两格，向右一格
        if cur_grid[1] <= 7:
            tempChess = ChessInfo[cur_grid[0] - 2][cur_grid[1] + 1]
            if side != tempChess // 10 or tempChess == 0:
                curCanMove.append((cur_grid[0] - 2, cur_grid[1] + 1))
    # 向下走
    if cur_grid[0] <= 7 and ChessInfo[cur_grid[0] + 1][cur_grid[1]] == 0:
        if cur_grid[1] >= 1:
            tempChess = ChessInfo[cur_grid[0] + 2][cur_grid[1] - 1]
            if side != tempChess // 10 or tempChess == 0:
                curCanMove.append((cur_grid[0] + 2, cur_grid[1] - 1))
        if cur_grid[1] <= 7:
            tempChess = ChessInfo[cur_grid[0] + 2][cur_grid[1] + 1]
            if side != tempChess // 10 or tempChess == 0:
                curCanMove.append((cur_grid[0] + 2, cur_grid[1] + 1))
    # 向左走
    if cur_grid[1] >= 2 and ChessInfo[cur_grid[0]][cur_grid[1] - 1] == 0:
        # 左上；向左两格，向上一格
        if cur_grid[0] >= 1:
            tempChess = ChessInfo[cur_grid[0] - 1][cur_grid[1] - 2]
            if side != tempChess // 10 or tempChess == 0:
                curCanMove.append((cur_grid[0] - 1, cur_grid[1] - 2))
        # 左下；向左两格，向下一格
        if cur_grid[0] <= 8:
            tempChess = ChessInfo[cur_grid[0] + 1][cur_grid[1] - 2]
            if side != tempChess // 10 or tempChess == 0:
                curCanMove.append((cur_grid[0] + 1, cur_grid[1] - 2))
    # 向右走
    if cur_grid[1] <= 6 and ChessInfo[cur_grid[0]][cur_grid[1] + 1] == 0:
        if cur_grid[0] >= 1:
            tempChess = ChessInfo[cur_grid[0] - 1][cur_grid[1] + 2]
            if side != tempChess // 10 or tempChess == 0:
                curCanMove.append((cur_grid[0] - 1, cur_grid[1] + 2))
        if cur_grid[0] <= 8:
            tempChess = ChessInfo[cur_grid[0] + 1][cur_grid[1] + 2]
            if side != tempChess // 10 or tempChess == 0:
                curCanMove.append((cur_grid[0] + 1, cur_grid[1] + 2))

    return curCanMove


def xiang_check(ChessInfo, cur_grid, cur_chess_num):
    curCanMove = []
    side = cur_chess_num // 10
    # 左上
    if cur_grid[1] != 0 and cur_grid[0] != 5:
        # 中间没有遮挡
        if ChessInfo[cur_grid[0] - 1][cur_grid[1] - 1] == 0:
            tempChess = ChessInfo[cur_grid[0] - 2][cur_grid[1] - 2]
            if side != tempChess // 10 or tempChess == 0:
                curCanMove.append((cur_grid[0] - 2, cur_grid[1] - 2))
    # 右上
    if cur_grid[1] != 8 and cur_grid[0] != 5:
        # 中间没有遮挡
        if ChessInfo[cur_grid[0] - 1][cur_grid[1] + 1] == 0:
            tempChess = ChessInfo[cur_grid[0] - 2][cur_grid[1] + 2]
            if side != tempChess // 10 or tempChess == 0:
                curCanMove.append((cur_grid[0] - 2, cur_grid[1] + 2))
    # 左下
    if cur_grid[1] != 0 and cur_grid[0] != 9:
        # 中间没有遮挡
        if ChessInfo[cur_grid[0] + 1][cur_grid[1] - 1] == 0:
            tempChess = ChessInfo[cur_grid[0] + 2][cur_grid[1] - 2]
            if side != tempChess // 10 or tempChess == 0:
                curCanMove.append((cur_grid[0] + 2, cur_grid[1] - 2))
    # 右下
    if cur_grid[1] != 8 and cur_grid[0] != 9:
        # 中间没有遮挡
        if ChessInfo[cur_grid[0] + 1][cur_grid[1] + 1] == 0:
            tempChess = ChessInfo[cur_grid[0] + 2][cur_grid[1] + 2]
            if side != tempChess // 10 or tempChess == 0:
                curCanMove.append((cur_grid[0] + 2, cur_grid[1] + 2))

    return curCanMove


def shi_check(ChessInfo, cur_grid, cur_chess_num):
    curCanMove = []
    side = cur_chess_num // 10
    # 左上
    if cur_grid[1] != 3 and cur_grid[0] != 7:
        tempChess = ChessInfo[cur_grid[0] - 1][cur_grid[1] - 1]
        if side != tempChess // 10 or tempChess == 0:
            curCanMove.append((cur_grid[0] - 1, cur_grid[1] - 1))
    # 右上
    if cur_grid[1] != 5 and cur_grid[0] != 7:
        tempChess = ChessInfo[cur_grid[0] + 1][cur_grid[1] - 1]
        if side != tempChess // 10 or tempChess == 0:
            curCanMove.append((cur_grid[0] + 1, cur_grid[1] - 1))
    # 左下
    if cur_grid[1] != 3 and cur_grid[0] != 9:
        tempChess = ChessInfo[cur_grid[0] - 1][cur_grid[1] + 1]
        if side != tempChess // 10 or tempChess == 0:
            curCanMove.append((cur_grid[0] - 1, cur_grid[1] + 1))
    # 右下
    if cur_grid[1] != 5 and cur_grid[0] != 9:
        tempChess = ChessInfo[cur_grid[0] + 1][cur_grid[1] + 1]
        if side != tempChess // 10 or tempChess == 0:
            curCanMove.append((cur_grid[0] + 1, cur_grid[1] + 1))

    return curCanMove


def shuai_check(ChessInfo, cur_grid, cur_chess_num):
    curCanMove = []
    side = cur_chess_num // 10
    # 上
    if cur_grid[0] != 7:
        tempChess = ChessInfo[cur_grid[0] - 1][cur_grid[1]]
        if side != tempChess // 10 or tempChess == 0:
            curCanMove.append((cur_grid[0] - 1, cur_grid[1]))
    # 下
    if cur_grid[0] != 9:
        tempChess = ChessInfo[cur_grid[0] + 1][cur_grid[1]]
        if side != tempChess // 10 or tempChess == 0:
            curCanMove.append((cur_grid[0] + 1, cur_grid[1]))
    # 左
    if cur_grid[1] != 3:
        tempChess = ChessInfo[cur_grid[0]][cur_grid[1] - 1]
        if side != tempChess // 10 or tempChess == 0:
            curCanMove.append((cur_grid[0], cur_grid[1] - 1))
    # 右
    if cur_grid[1] != 5:
        tempChess = ChessInfo[cur_grid[0]][cur_grid[1] + 1]
        if side != tempChess // 10 or tempChess == 0:
            curCanMove.append((cur_grid[0], cur_grid[1] + 1))

    return curCanMove


def pao_check(ChessInfo, cur_grid, cur_chess_num):
    curCanMove = []
    side = cur_chess_num // 10

    # 列移动
    tempY = cur_grid[1] - 1
    # 向左遍历
    offSetY = -1
    barrier = False
    while True:
        # 碰到左边界，调头向右
        if tempY < 0:
            tempY = cur_grid[1] + 1
            barrier = False
            offSetY = 1
            continue
        # 碰到右边界，退出
        elif tempY > 8:
            break
        tempChess = ChessInfo[cur_grid[0]][tempY]
        targetSide = tempChess // 10
        # 如果该方向有跳板
        if barrier:
            if tempChess != 0:
                if targetSide != side:
                    # 是敌方就加入可选列表
                    curCanMove.append((cur_grid[0], tempY))
                if offSetY == 1:
                    break
                # 向右调头
                tempY = cur_grid[1]
                barrier = False
                offSetY = 1
        # 该方向无跳板
        else:
            if tempChess == 0:
                curCanMove.append((cur_grid[0], tempY))
            else:
                barrier = True

        tempY += offSetY

    # 列移动
    tempX = cur_grid[0] - 1
    # 向上遍历
    offSetX = -1
    barrier = False
    while True:
        if tempX < 0:
            tempX = cur_grid[0] + 1
            barrier = False
            offSetX = 1
            continue
        elif tempX > 9:
            break
        tempChess = ChessInfo[tempX][cur_grid[1]]
        targetSide = tempChess // 10
        # 如果该方向有跳板
        if barrier:
            if tempChess != 0:
                if targetSide != side:
                    # 是敌方就加入可选列表
                    curCanMove.append((tempX, cur_grid[1]))
                if offSetX == 1:
                    break
                # 向右调头
                tempX = cur_grid[0]
                barrier = False
                offSetX = 1

        # 该方向无跳板
        else:
            if tempChess == 0:
                curCanMove.append((tempX, cur_grid[1]))
            else:
                barrier = True

        tempX += offSetX

    return curCanMove


def bing_check(ChessInfo, cur_grid, cur_chess_num):
    curCanMove = []
    side = cur_chess_num // 10

    if cur_grid[0] != 0:
        tempChess = ChessInfo[cur_grid[0] - 1][cur_grid[1]]
        if side != tempChess // 10 or tempChess == 0:
            # 拱卒
            curCanMove.append((cur_grid[0] - 1, cur_grid[1]))
    # 若已过河
    if cur_grid[0] <= 4:
        if cur_grid[1] != 0:
            tempChess = ChessInfo[cur_grid[0]][cur_grid[1] - 1]
            if side != tempChess // 10 or tempChess == 0:
                # 左走
                curCanMove.append((cur_grid[0], cur_grid[1] - 1))
        if cur_grid[1] != 8:
            tempChess = ChessInfo[cur_grid[0]][cur_grid[1] + 1]
            if side != tempChess // 10 or tempChess == 0:
                # 右走
                curCanMove.append((cur_grid[0], cur_grid[1] + 1))

    return curCanMove


check_function = {1: che_check,
                  2: horse_check,
                  3: xiang_check,
                  4: shi_check,
                  5: shuai_check,
                  6: pao_check,
                  7: bing_check}


# 查找可以该棋子可走的位置
def where_can_move(chess_info: list[list[int]], choice: tuple):
    cur_chess = chess_info[choice[0]][choice[1]]
    print(f'当前选择棋子:{choice}')
    temp = check_function.get(cur_chess % 10)(chess_info, choice, cur_chess)
    return temp
