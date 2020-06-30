from queue import PriorityQueue
import time
# from eract4 import eract
import pyautogui as auto

h, w = 4, 4
auto.PAUSE = 0.1


class Solution:
    # BFS + A*
    def solve(self, board):
        pro1 = self.solve_first_line(board)
        pro2 = self.solve_first_column(pro1[2])
        pro3 = self.solve_last_8(pro2[2])

        return sum([pro1[0], pro2[0], pro3[0]]), pro1[1] + pro2[1] + pro3[1]

    # 计算当前节点到目标节点的距离
    @staticmethod
    def calDistance(node):
        dis = 0
        for i in range(len(node)):
            if node[i] == 0 | node[i] == -1:
                continue
            dis += abs(i // w - (node[i] - 1) // w) + abs(i % w - (node[i] - 1) % w)
        return dis
        # return 0 #退化为BFS算法

    def solve_first_line(self, board0):
        i_n = [1, 2, 3, 4]
        board = []
        for i in board0:
            if i in i_n:
                board.append(i)
            elif i == 0:
                board.append(0)
            else:
                board.append(-1)
        start = tuple(board)
        process = []
        target = (1, 2, 3, 4, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1)

        # 优先队列，值越小，优先级越高
        pQueue = PriorityQueue()
        pQueue.put([0 + self.calDistance(start), start, start.index(0), 0, process, board0])

        seen = {start}  # 已遍历过的结点

        while not pQueue.empty():
            _pri, board, pos0, depth, process, board0 = pQueue.get()
            if board == target:
                return depth, process, board0
            for d in (-1, 1, -w, w):  # 对应的是左右上下的相邻结点
                nei = pos0 + d
                if abs(nei // w - pos0 // w) + abs(nei % w - pos0 % w) != 1:
                    continue
                if 0 <= nei < w * h:  # 符合边界条件的相邻结点
                    newboard = list(board)
                    newboard[pos0], newboard[nei] = newboard[nei], newboard[pos0]
                    newboard0 = list(board0)
                    newboard0[pos0], newboard0[nei] = newboard0[nei], newboard0[pos0]
                    newt = tuple(newboard)
                    if newt not in seen:  # 没有被遍历过的结点
                        seen.add(newt)
                        pQueue.put([depth + 1 + self.calDistance(newt), newt, nei, depth + 1, process + [d], newboard0])

    def solve_first_column(self, board0):
        i_n = [1, 2, 3, 4, 5, 9, 13]
        board = []
        for i in board0:
            if i in i_n:
                board.append(i)
            elif i == 0:
                board.append(0)
            else:
                board.append(-1)
        start = tuple(board)
        process = []
        target = (1, 2, 3, 4, 5, 0, -1, -1, 9, -1, -1, -1, 13, -1, -1, -1)

        # 优先队列，值越小，优先级越高
        pQueue = PriorityQueue()
        pQueue.put([0 + self.calDistance(start), start, start.index(0), 0, process, board0])

        seen = {start}  # 已遍历过的结点

        while not pQueue.empty():
            _pri, board, pos0, depth, process, board0 = pQueue.get()
            if board == target:
                return depth, process, board0
            for d in (-1, 1, -w, w):  # 对应的是左右上下的相邻结点
                nei = pos0 + d
                if abs(nei // w - pos0 // w) + abs(nei % w - pos0 % w) != 1:
                    continue
                if 4 <= nei < w * h:  # 符合边界条件的相邻结点
                    newboard = list(board)
                    newboard[pos0], newboard[nei] = newboard[nei], newboard[pos0]
                    newboard0 = list(board0)
                    newboard0[pos0], newboard0[nei] = newboard0[nei], newboard0[pos0]
                    newt = tuple(newboard)
                    if newt not in seen:  # 没有被遍历过的结点
                        seen.add(newt)
                        pQueue.put([depth + 1 + self.calDistance(newt), newt, nei, depth + 1, process + [d], newboard0])

    def solve_last_8(self, board):
        start = tuple(board)
        process = []
        target = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0)

        # 优先队列，值越小，优先级越高
        pQueue = PriorityQueue()
        pQueue.put([0 + self.calDistance(start), start, start.index(0), 0, process])

        seen = {start}  # 已遍历过的结点

        while not pQueue.empty():
            _pri, board, pos0, depth, process = pQueue.get()
            if board == target:  # 如果已经为目标结点，直接返回depth
                return depth, process
            for d in (-1, 1, -w, w):  # 对应的是左右上下的相邻结点
                nei = pos0 + d
                if abs(nei // w - pos0 // w) + abs(nei % w - pos0 % w) != 1:
                    continue
                if 4 <= nei < w * h and nei != 8 and nei != 12:  # 符合边界条件的相邻结点
                    newboard = list(board)
                    newboard[pos0], newboard[nei] = newboard[nei], newboard[pos0]
                    newt = tuple(newboard)
                    if newt not in seen:  # 没有被遍历过的结点
                        seen.add(newt)
                        pQueue.put([depth + 1 + self.calDistance(newt), newt, nei, depth + 1, process + [d]])


def auto_click4(b):
    t_solve = time.time()
    step_num, process = Solution().solve(b)
    print("总步数{},计算用时{}".format(step_num, time.time() - t_solve))

    first_x = 1025 # 这里的坐标是左上角的位置，根据自己屏幕调的
    first_y = 330
    width = 120
    zero_pos = (first_x + b.index(0) % 4 * width, first_y + b.index(0) // 4 * width)
    auto.moveTo(zero_pos)

    t_move = time.time()
    for i in process:
        if i == 1:
            auto.moveRel(width, None)
        elif i == -1:
            auto.moveRel(-width, None)
        elif i == -4:
            auto.moveRel(None, -width)
        else:
            auto.moveRel(None, width)
        auto.click()
    print("执行用时{}".format(time.time() - t_move))
