__doc__ = """
井字棋示例AI：简单级
随机填充棋盘
"""

import random


def play(board: dict):
    # 打印自己所得棋盘
    print('DUMB RANDOM'.center(30, '='))
    for r in range(3):
        print(*(board[r, c] for c in range(3)))

    # 获取所有可填充位置
    targets = []
    for k, v in board.items():
        if v == 'E':
            targets.append(k)

    # 随机填充
    return random.choice(targets)