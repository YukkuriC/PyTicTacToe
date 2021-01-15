if 'enums':
    OK = 0  # 游戏继续
    ENDGAME = 1  # 形成三连
    DRAW = 2  # 棋盘已满平局
    INVALID = -1  # 非法返回值（类型错误/出界）
    CONFILCT = -2  # 冲突落子（下于已有棋子位置）
    ERROR = -3  # 代码报错
    TIMEOUT = -4  # 代码超时


class Board:
    """
    基础棋盘类，用于计算局面情形+发放双方玩家所用局面
    使用数字1、2分别代表不同方玩家落子
    """

    def __init__(self):
        self.pool = {}  # 仅填充1/2的字典

    def get_board(self, plr: int):
        """
        为指定玩家编号返回其局面字典
        字典键为2长度元组，每位数字（0，1，2）分别代表行号与列号
        返回对象中包含3*3棋盘位置，对应值均为字符串，含义如下：
            "O": 我方落子
            "X": 对方落子
            "E": 空
        """
        res = {}
        for x in range(3):
            for y in range(3):
                if (x, y) in self.pool:
                    res[x, y] = 'O' if self.pool[x, y] == plr else 'X'
                else:
                    res[x, y] = 'E'
        return res

    def drop(self, plr, pos):
        """
        指定玩家编号plr在指定位置pos落子
        返回落子结果
        """
        if _drop_data_check(pos):  # 非法落子检查
            return INVALID
        if pos in self.pool:  # 冲突落子检查
            return CONFILCT
        self.pool[pos] = plr  # 落子，检查游戏结束状态
        return self._check_endgame()

    def _drop_data_check(self, pos):
        """
        检验落子位置对象是否符合要求
        要求：
            * 必须为列表或元组
            * 长度必须为2
            * 每位均为int，取值只可为0,1,2
        """
        if not isinstance(pos, (list, tuple)):
            return INVALID
        if len(pos) != 2:
            return INVALID
        for i in pos:
            if not (isinstance(i, int) and 0 <= i <= 2):
                return INVALID
        return OK

    def _check_endgame(self):
        """ 检查游戏状态是否结束 """
        for x in range(3):
            if self._3_equal(
                    self.pool.get((x, i)) for i in range(3)):  # axis 0
                return ENDGAME
            if self._3_equal(
                    self.pool.get((i, x)) for i in range(3)):  # axis 1
                return ENDGAME
        if self._3_equal(self.pool.get((i, i)) for i in range(3)):  # 正对角线
            return ENDGAME
        if self._3_equal(self.pool.get((i, 2 - i)) for i in range(3)):  # 反对角线
            return ENDGAME
        return OK if len(self.pool) < 9 else DRAW

    def _3_equal(self, row):
        """ 辅助函数：检查一行3数（非空）相等状态 """
        row = iter(row)
        n1 = next(row)
        if not n1:
            return False
        for n in row:
            if n != n1:
                return False
        return True
