from queue import PriorityQueue
import time
# import pyautogui as auto

h, w = 4, 4


class Solution:
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

    @staticmethod
    def finish(target, board):
        for i in range(15):
            if target[i] == -1:
                continue
            if target[i] != board[i]:
                return False
        return True

    # BFS + A*
    def solve(self, board0, n=w):
        bound = []
        if n == 3:
            board = board0
            bound = [i -1 for i in range(1, 16) if (i - 1) // 4 == 0 or (i - 1) % 4 == 0]
        else:
            board = []
            i_n = [i for i in range(1, 16) if (i - 1) // 4 == 0 or (i - 1) % 4 == 0]
            for i in board0:
                if i in i_n:
                    board.append(i)
                elif i == 0:
                    board.append(0)
                else:
                    board.append(-1)

        start = tuple(board)
        process = []
        if n == 3:
            target = tuple([*range(1, 4 * 4)] + [0])
        else:
            target = (1, 2, 3, 4, 5, -1, -1, -1, 9, -1, -1, -1, 13, -1, -1, -1)

        # 优先队列，值越小，优先级越高
        pQueue = PriorityQueue()
        pQueue.put([0 + self.calDistance(start), start, start.index(0), 0, process, board0])

        seen = {start}  # 已遍历过的结点

        while not pQueue.empty():
            _pri, board, pos0, depth, process, board0 = pQueue.get()
            if self.finish(target, board):
                if n == 3:
                    return process
                return process + self.solve(board0, n-1)
            for d in (-1, 1, -w, w):  # 对应的是左右上下的相邻结点
                nei = pos0 + d
                if abs(nei // w - pos0 // w) + abs(nei % w - pos0 % w) != 1:
                    continue
                if 0 <= nei < w * h and nei not in bound:  # 符合边界条件的相邻结点
                    newboard = list(board)
                    newboard[pos0], newboard[nei] = newboard[nei], newboard[pos0]
                    newboard0 = list(board0)
                    newboard0[pos0], newboard0[nei] = newboard0[nei], newboard0[pos0]
                    newt = tuple(newboard)
                    if newt not in seen:  # 没有被遍历过的结点
                        seen.add(newt)
                        pQueue.put([depth + 1 + self.calDistance(newt), newt, nei, depth + 1, process + [d], newboard0])


b = [7, 9, 4, 14,
     8, 2, 0, 5,
     13, 11, 15, 10,
     1, 3, 6, 12
     ]
t_solve = time.time()
process = Solution().solve(b, 4)
print("总步数{},计算用时{}".format(len(process), time.time() - t_solve))
print(process)
