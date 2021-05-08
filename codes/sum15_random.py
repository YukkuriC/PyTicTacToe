__doc__ = """
井字棋示例AI：简单级
随机填充棋盘
"""

import random


def play(nums_left, nums_self, nums_other):
    return random.choice(nums_left)