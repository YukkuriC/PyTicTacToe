__doc__ = """
井字棋示例AI：简单级
按顺序逐行逐列填充棋盘
"""


def play(board: dict):
    # 打印自己所得棋盘
    print('DUMB ORDERED'.center(30, '='))
    for r in range(3):
        print(*(board[r, c] for c in range(3)))

    # 按顺序遍历寻找空位置
    for k, v in board.items():
        if v == 'E':
            return k