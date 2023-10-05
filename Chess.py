def che_check(chess_info, cur_grid, cur_chess_num):
    cur_can_move = []
    side = cur_chess_num // 10
    # 扫描当前行可移动位置
    temp_y = cur_grid[1] - 1
    # 向左遍历
    off_set_y = -1
    while True:
        if temp_y < 0:
            temp_y = cur_grid[1] + 1
            # 碰到左边界，回到原先位置右侧，调头向右
            off_set_y = 1
            continue
        # 碰到右边界，退出
        elif temp_y > 8:
            break
        temp_chess = chess_info[cur_grid[0]][temp_y]
        # 判断为空棋子;空棋子加入可移动列表
        if temp_chess == 0:
            cur_can_move.append((cur_grid[0], temp_y))
        else:
            # 非空棋子为敌方，则掉头并加入可移动列表
            if side != temp_chess // 10:
                cur_can_move.append((cur_grid[0], temp_y))

            # 已经调过头；直接退出
            if off_set_y == 1:
                break

            temp_y = cur_grid[1]
            # 调头
            off_set_y = 1
        temp_y += off_set_y

    # 扫描当前列可移动的位置，逻辑类似上方
    temp_x = cur_grid[0] - 1
    off_set_x = -1
    while True:
        if temp_x < 0:
            temp_x = cur_grid[0] + 1
            off_set_x = 1
            continue
        elif temp_x > 9:
            break
        temp_chess = chess_info[temp_x][cur_grid[1]]
        if temp_chess == 0:
            cur_can_move.append((temp_x, cur_grid[1]))
        else:
            if side != temp_chess // 10:
                cur_can_move.append((temp_x, cur_grid[1]))

            if off_set_x == 1:
                break

            temp_x = cur_grid[0]
            off_set_x = 1
        temp_x += off_set_x

    return cur_can_move


def horse_check(chess_info, cur_grid, cur_chess_num):
    cur_can_move = []
    side = cur_chess_num // 10
    # 向上走;没顶格，没被棋子挡住马脚
    if cur_grid[0] >= 2 and chess_info[cur_grid[0] - 1][cur_grid[1]] == 0:
        # 左上;向上两格，向左一格
        if cur_grid[1] >= 1:
            temp_chess = chess_info[cur_grid[0] - 2][cur_grid[1] - 1]
            if side != temp_chess // 10 or temp_chess == 0:
                cur_can_move.append((cur_grid[0] - 2, cur_grid[1] - 1))
        # 右上;向上两格，向右一格
        if cur_grid[1] <= 7:
            temp_chess = chess_info[cur_grid[0] - 2][cur_grid[1] + 1]
            if side != temp_chess // 10 or temp_chess == 0:
                cur_can_move.append((cur_grid[0] - 2, cur_grid[1] + 1))
    # 向下走
    if cur_grid[0] <= 7 and chess_info[cur_grid[0] + 1][cur_grid[1]] == 0:
        if cur_grid[1] >= 1:
            temp_chess = chess_info[cur_grid[0] + 2][cur_grid[1] - 1]
            if side != temp_chess // 10 or temp_chess == 0:
                cur_can_move.append((cur_grid[0] + 2, cur_grid[1] - 1))
        if cur_grid[1] <= 7:
            temp_chess = chess_info[cur_grid[0] + 2][cur_grid[1] + 1]
            if side != temp_chess // 10 or temp_chess == 0:
                cur_can_move.append((cur_grid[0] + 2, cur_grid[1] + 1))
    # 向左走
    if cur_grid[1] >= 2 and chess_info[cur_grid[0]][cur_grid[1] - 1] == 0:
        # 左上；向左两格，向上一格
        if cur_grid[0] >= 1:
            temp_chess = chess_info[cur_grid[0] - 1][cur_grid[1] - 2]
            if side != temp_chess // 10 or temp_chess == 0:
                cur_can_move.append((cur_grid[0] - 1, cur_grid[1] - 2))
        # 左下；向左两格，向下一格
        if cur_grid[0] <= 8:
            temp_chess = chess_info[cur_grid[0] + 1][cur_grid[1] - 2]
            if side != temp_chess // 10 or temp_chess == 0:
                cur_can_move.append((cur_grid[0] + 1, cur_grid[1] - 2))
    # 向右走
    if cur_grid[1] <= 6 and chess_info[cur_grid[0]][cur_grid[1] + 1] == 0:
        if cur_grid[0] >= 1:
            temp_chess = chess_info[cur_grid[0] - 1][cur_grid[1] + 2]
            if side != temp_chess // 10 or temp_chess == 0:
                cur_can_move.append((cur_grid[0] - 1, cur_grid[1] + 2))
        if cur_grid[0] <= 8:
            temp_chess = chess_info[cur_grid[0] + 1][cur_grid[1] + 2]
            if side != temp_chess // 10 or temp_chess == 0:
                cur_can_move.append((cur_grid[0] + 1, cur_grid[1] + 2))

    return cur_can_move


def xiang_check(chess_info, cur_grid, cur_chess_num):
    cur_can_move = []
    side = cur_chess_num // 10
    # 左上
    if cur_grid[1] != 0 and cur_grid[0] != 5:
        # 中间没有遮挡
        if chess_info[cur_grid[0] - 1][cur_grid[1] - 1] == 0:
            temp_chess = chess_info[cur_grid[0] - 2][cur_grid[1] - 2]
            if side != temp_chess // 10 or temp_chess == 0:
                cur_can_move.append((cur_grid[0] - 2, cur_grid[1] - 2))
    # 右上
    if cur_grid[1] != 8 and cur_grid[0] != 5:
        # 中间没有遮挡
        if chess_info[cur_grid[0] - 1][cur_grid[1] + 1] == 0:
            temp_chess = chess_info[cur_grid[0] - 2][cur_grid[1] + 2]
            if side != temp_chess // 10 or temp_chess == 0:
                cur_can_move.append((cur_grid[0] - 2, cur_grid[1] + 2))
    # 左下
    if cur_grid[1] != 0 and cur_grid[0] != 9:
        # 中间没有遮挡
        if chess_info[cur_grid[0] + 1][cur_grid[1] - 1] == 0:
            temp_chess = chess_info[cur_grid[0] + 2][cur_grid[1] - 2]
            if side != temp_chess // 10 or temp_chess == 0:
                cur_can_move.append((cur_grid[0] + 2, cur_grid[1] - 2))
    # 右下
    if cur_grid[1] != 8 and cur_grid[0] != 9:
        # 中间没有遮挡
        if chess_info[cur_grid[0] + 1][cur_grid[1] + 1] == 0:
            temp_chess = chess_info[cur_grid[0] + 2][cur_grid[1] + 2]
            if side != temp_chess // 10 or temp_chess == 0:
                cur_can_move.append((cur_grid[0] + 2, cur_grid[1] + 2))

    return cur_can_move


def shi_check(chess_info, cur_grid, cur_chess_num):
    cur_can_move = []
    side = cur_chess_num // 10
    # 左上
    if cur_grid[1] != 3 and cur_grid[0] != 7:
        temp_chess = chess_info[cur_grid[0] - 1][cur_grid[1] - 1]
        if side != temp_chess // 10 or temp_chess == 0:
            cur_can_move.append((cur_grid[0] - 1, cur_grid[1] - 1))
    # 右上
    if cur_grid[1] != 5 and cur_grid[0] != 7:
        temp_chess = chess_info[cur_grid[0] - 1][cur_grid[1] + 1]
        if side != temp_chess // 10 or temp_chess == 0:
            cur_can_move.append((cur_grid[0] - 1, cur_grid[1] + 1))
    # 左下
    if cur_grid[1] != 3 and cur_grid[0] != 9:
        temp_chess = chess_info[cur_grid[0] + 1][cur_grid[1] - 1]
        if side != temp_chess // 10 or temp_chess == 0:
            cur_can_move.append((cur_grid[0] + 1, cur_grid[1] - 1))
    # 右下
    if cur_grid[1] != 5 and cur_grid[0] != 9:
        temp_chess = chess_info[cur_grid[0] + 1][cur_grid[1] + 1]
        if side != temp_chess // 10 or temp_chess == 0:
            cur_can_move.append((cur_grid[0] + 1, cur_grid[1] + 1))

    return cur_can_move


def shuai_check(chess_info, cur_grid, cur_chess_num):
    cur_can_move = []
    side = cur_chess_num // 10
    # 上
    if cur_grid[0] != 7:
        temp_chess = chess_info[cur_grid[0] - 1][cur_grid[1]]
        if side != temp_chess // 10 or temp_chess == 0:
            cur_can_move.append((cur_grid[0] - 1, cur_grid[1]))
    # 下
    if cur_grid[0] != 9:
        temp_chess = chess_info[cur_grid[0] + 1][cur_grid[1]]
        if side != temp_chess // 10 or temp_chess == 0:
            cur_can_move.append((cur_grid[0] + 1, cur_grid[1]))
    # 左
    if cur_grid[1] != 3:
        temp_chess = chess_info[cur_grid[0]][cur_grid[1] - 1]
        if side != temp_chess // 10 or temp_chess == 0:
            cur_can_move.append((cur_grid[0], cur_grid[1] - 1))
    # 右
    if cur_grid[1] != 5:
        temp_chess = chess_info[cur_grid[0]][cur_grid[1] + 1]
        if side != temp_chess // 10 or temp_chess == 0:
            cur_can_move.append((cur_grid[0], cur_grid[1] + 1))

    return cur_can_move


def pao_check(chess_info, cur_grid, cur_chess_num):
    cur_can_move = []
    side = cur_chess_num // 10

    # 列移动
    temp_y = cur_grid[1] - 1
    # 向左遍历
    off_set_y = -1
    barrier = False
    while True:
        # 碰到左边界，调头向右
        if temp_y < 0:
            temp_y = cur_grid[1] + 1
            barrier = False
            off_set_y = 1
            continue
        # 碰到右边界，退出
        elif temp_y > 8:
            break
        temp_chess = chess_info[cur_grid[0]][temp_y]
        target_side = temp_chess // 10
        # 如果该方向有跳板
        if barrier:
            if temp_chess != 0:
                if target_side != side:
                    # 是敌方就加入可选列表
                    cur_can_move.append((cur_grid[0], temp_y))
                if off_set_y == 1:
                    break
                # 向右调头
                temp_y = cur_grid[1]
                barrier = False
                off_set_y = 1
        # 该方向无跳板
        else:
            if temp_chess == 0:
                cur_can_move.append((cur_grid[0], temp_y))
            else:
                barrier = True

        temp_y += off_set_y

    # 列移动
    temp_x = cur_grid[0] - 1
    # 向上遍历
    off_set_x = -1
    barrier = False
    while True:
        if temp_x < 0:
            temp_x = cur_grid[0] + 1
            barrier = False
            off_set_x = 1
            continue
        elif temp_x > 9:
            break
        temp_chess = chess_info[temp_x][cur_grid[1]]
        target_side = temp_chess // 10
        # 如果该方向有跳板
        if barrier:
            if temp_chess != 0:
                if target_side != side:
                    # 是敌方就加入可选列表
                    cur_can_move.append((temp_x, cur_grid[1]))
                if off_set_x == 1:
                    break
                # 向右调头
                temp_x = cur_grid[0]
                barrier = False
                off_set_x = 1

        # 该方向无跳板
        else:
            if temp_chess == 0:
                cur_can_move.append((temp_x, cur_grid[1]))
            else:
                barrier = True

        temp_x += off_set_x

    return cur_can_move


def bing_check(chess_info, cur_grid, cur_chess_num):
    cur_can_move = []
    side = cur_chess_num // 10

    if cur_grid[0] != 0:
        temp_chess = chess_info[cur_grid[0] - 1][cur_grid[1]]
        if side != temp_chess // 10 or temp_chess == 0:
            # 拱卒
            cur_can_move.append((cur_grid[0] - 1, cur_grid[1]))
    # 若已过河
    if cur_grid[0] <= 4:
        if cur_grid[1] != 0:
            temp_chess = chess_info[cur_grid[0]][cur_grid[1] - 1]
            if side != temp_chess // 10 or temp_chess == 0:
                # 左走
                cur_can_move.append((cur_grid[0], cur_grid[1] - 1))
        if cur_grid[1] != 8:
            temp_chess = chess_info[cur_grid[0]][cur_grid[1] + 1]
            if side != temp_chess // 10 or temp_chess == 0:
                # 右走
                cur_can_move.append((cur_grid[0], cur_grid[1] + 1))

    return cur_can_move


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
    temp = check_function.get(cur_chess % 10)(chess_info, choice, cur_chess)
    return temp
