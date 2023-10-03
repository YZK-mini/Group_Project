def che_check(ChessInfo, cur_grid, cur_chess_num):
    curCanMove = []
    side = cur_chess_num // 10
    # 扫描当前行可移动位置
    tempPosX = cur_grid[0] - 1
    offSetX = -1  # 向左遍历
    while True:
        if tempPosX < 0:
            tempPosX = cur_grid[1] + 1
            offSetX = 1  # 碰到左边界，回到原先位置右侧，调头向右
            continue
        elif tempPosX > 8:  # 碰到右边界，退出
            break
        tempChess = ChessInfo[cur_grid[0]][tempPosX]
        # 判断为空棋子;空棋子加入可移动列表
        if tempChess == 0:
            curCanMove.append((tempPosX, cur_grid[1]))
        else:
            # 非空棋子且为地方则掉头并加入可移动列表
            if side != tempChess // 10:
                curCanMove.append(tempChess)
            # 已经调过头；直接退出
            if offSetX == 1:
                break
            tempPosX = cur_grid[0]
            offSetX = 1  # 调头
        tempPosX += offSetX

    # 扫描当前列可移动的位置，逻辑类似上方
    tempPosY = cur_grid[1] - 1
    offSetY = -1
    while True:
        if tempPosY < 0:
            tempPosY = cur_grid[1] + 1
            offSetY = 1
            continue
        elif tempPosY > 9:
            break
        tempChess = ChessInfo[tempPosY][cur_grid[0]]
        if tempChess == 0:
            curCanMove.append((cur_grid[0], tempPosY))
        else:
            # 非空棋子且为地方则掉头并加入可移动列表
            if side != tempChess // 10:
                curCanMove.append(tempChess)
            if offSetY == 1:
                break
            tempPosY = cur_grid[1]
            offSetY = 1
        tempPosY += offSetY
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
    return check_function.get(cur_chess % 10)(chess_info, choice, cur_chess)
