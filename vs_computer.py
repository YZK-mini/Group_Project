# 人机AI #
from copy import deepcopy


class AI:
    def __init__(self, data):
        self.data = data

    def search(self, side, depth, data=[]):
        if depth == 0 or len(data) == 1:
            from pprint import pprint;
            pprint(data[0])
            return data[0]

        side = 'Black' if side == 'Red' else 'Red'

        if data == []:
            tree = []
            lis = self.data
            for i in range(10):
                for j in range(9):
                    if 0 <= lis[i][j] <= 15:
                        for x in range(10):
                            for y in range(9):
                                if self.Isstep(lis, 'Black', i, j, x, y):
                                    temp = deepcopy(lis)
                                    temp[x][y] = -1
                                    temp[x][y], temp[i][j] = temp[i][j], temp[x][y]
                                    tree.append([i, j, x, y, temp, self.scores(temp)])

            data = tree

        else:
            for ind, l in enumerate(data):
                lis = l[4]
                scorelist = []

                for i in range(10):
                    for j in range(9):
                        if (side == 'Red' and 16 <= lis[i][j] <= 31) or (side == 'Black' and 0 <= lis[i][j] <= 15):
                            for x in range(10):
                                for y in range(9):
                                    if self.Isstep(lis, side, i, j, x, y):
                                        temp = deepcopy(lis)
                                        temp[x][y] = -1
                                        temp[x][y], temp[i][j] = temp[i][j], temp[x][y]
                                        scorelist.append(self.scores(temp))

                tot, length = 0, 0
                for i in scorelist:
                    if i != 0:
                        tot += i
                        length += 1

                if length:
                    data[ind][-1] += tot / length
                else:
                    data[ind][-1] += 0
                '''
                k = 1 if side == 'Black' else -1
                scorelist = [k*i for i in scorelist]
                key = abs(min(scorelist))
                tot = 0
                for i in scorelist:
                    tot += (i+key)**2

                ans = 0
                for i in scorelist:
                    try:
                        ans += i*((i+key)**2/tot)
                    except:
                        continue
                data[ind][-1] += ans*k
                '''

        return self.search(side, depth - 1,
                           sorted(data, key=lambda x: -x[-1])[0:round(0.618 * len(data))])  # [1:round(0.618*len(data))]

    def scores(self, data):  # 计算棋面得分
        lib = (99999, 1500, 1500, 1000, 1000, 4000, 4000, 6000, 6000, 4000, 4000, 100, 300, 500, 300, 100)
        Black, Red = 0, 0

        for i in data:
            for j in i:
                if 0 <= j <= 15:
                    Black += lib[j]
                if 16 <= j <= 31:
                    Red += lib[j - 16]

        # return Black-Red

        if Black - Red > 0:
            return Black - Red * 0.618
        else:
            return 0.618 * Black - Red