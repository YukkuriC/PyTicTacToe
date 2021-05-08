__doc__ = '''
井字棋基础设施扩展
包含连续比赛、记录保存等功能
'''

try:
    import ttt
except ImportError:
    from . import ttt


class GameSum15(ttt.Game):
    """
    规则套壳
    在1-9数字中双方各取1，先拿到和为15的3个数字者胜利
    """
    NUM2POS= {
        8: (0, 0), 1: (0, 1), 6: (0, 2), \
        3: (1, 0), 5: (1, 1), 7: (1, 2), \
        4: (2, 0), 9: (2, 1), 2: (2, 2),
    }

    @classmethod
    def trans_nums(cls, board):
        """ 将版面转换成对应列表 """
        res = {c: [] for c in 'SFE'}
        for num in range(1, 10):
            pos = cls.NUM2POS[num]
            grp = board[pos]
            res[grp].append(num)
        return res['E'], res['S'], res['F']

    @classmethod
    def _thread_wrap(cls, code, board, thr_output: dict):
        """
        转换层接口
        输入：board -> nums_left, nums_self, nums_other
        输出：num -> position
        """
        res = {
            "result": None,
            "error": None,
        }

        try:
            nums = cls.trans_nums(board)
            t1 = ttt.process_time()
            output = code.play(*nums)
            t2 = ttt.process_time()
            res['result'] = cls.NUM2POS.get(output, output)
        except Exception as e:
            t2 = ttt.process_time()
            res['error'] = Game._stringfy_error(e)

        res['dt'] = t2 - t1
        thr_output.update(res)


if __name__ == '__main__':
    import codes.sum15_ordered as plr1, codes.sum15_random as plr2

    game = GameSum15([plr1, plr2])
    print(game.match())
