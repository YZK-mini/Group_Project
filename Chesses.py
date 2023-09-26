import math


# 左上角(0,0)坐标的为(30,30)，格子间距离57
# Coordinate表示游戏坐标；Position表示棋子位置，左上角为(0,0)，右上角为(0,8)
# coX,coY				posX,posY


# 棋子位置转换为游戏坐标
def Pos2Co(posX, posY):
    return 57.5 * posX + 30, 57.5 * posY + 30


# 游戏坐标转换为棋子位置
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


class PlayerSideConst:
    RED = 0
    BLACK = 1


class ChessTypeConst:
    CHESS_NONE = 0

    RED_CHE = 1
    RED_HORSE = 2
    RED_XIANG = 3
    RED_SHI = 4
    RED_SHUAI = 5
    RED_PAO = 6
    RED_BING = 7

    BLACK_CHE = 11
    BLACK_HORSE = 12
    BLACK_XIANG = 13
    BLACK_SHI = 14
    BLACK_JIANG = 15
    BLACK_PAO = 16
    BLACK_ZU = 17


# 空位置
class NoneChess:
    def __init__(self, posX, posY):
        self.name = ' . '
        self.chessType = ChessTypeConst.CHESS_NONE
        self.posX = posX
        self.posY = posY

    def draw(self):
        pass

    def checkCanMove(self, posX, posY):
        return False

    def chessMove2PosXY(self, posX, posY):
        pass


noneChess = NoneChess(-1, -1)

ChessInfo = [
    # PosX→	#0			#1		#2			#3		#4			#5		#6		#7			#8	  #PosY↓
    [noneChess, noneChess, noneChess, noneChess, noneChess, noneChess, noneChess, noneChess, noneChess],  # 0
    [noneChess, noneChess, noneChess, noneChess, noneChess, noneChess, noneChess, noneChess, noneChess],  # 1
    [noneChess, noneChess, noneChess, noneChess, noneChess, noneChess, noneChess, noneChess, noneChess],  # 2
    [noneChess, noneChess, noneChess, noneChess, noneChess, noneChess, noneChess, noneChess, noneChess],  # 3
    [noneChess, noneChess, noneChess, noneChess, noneChess, noneChess, noneChess, noneChess, noneChess],  # 4
    [noneChess, noneChess, noneChess, noneChess, noneChess, noneChess, noneChess, noneChess, noneChess],  # 5
    [noneChess, noneChess, noneChess, noneChess, noneChess, noneChess, noneChess, noneChess, noneChess],  # 6
    [noneChess, noneChess, noneChess, noneChess, noneChess, noneChess, noneChess, noneChess, noneChess],  # 7
    [noneChess, noneChess, noneChess, noneChess, noneChess, noneChess, noneChess, noneChess, noneChess],  # 8
    [noneChess, noneChess, noneChess, noneChess, noneChess, noneChess, noneChess, noneChess, noneChess]  # 9
]
