from queue import PriorityQueue
import time

class Solution:
    # 计算当前节点到目标节点的距离
    @staticmethod
    def calDistance(node, w):
        dis = 0
        for i in range(len(node)):
            if node[i] == 0:
                continue
            dis += abs(i // w - (node[i] - 1) // w) + abs(i % w - (node[i] - 1) % w)
        return dis
        # return 0 #退化为BFS算法

    # BFS + A*
    def solve(self, board):
        # global flag, pre_solve
        size = int(len(board) ** 0.5)
        start = tuple(board)
        process = []
        target = tuple([i for i in range(1, size ** 2)] + [0])

        # 优先队列，值越小，优先级越高
        pQueue = PriorityQueue()
        pQueue.put([0 + self.calDistance(start, size), start, start.index(0), 0, process])

        seen = {start}  # 已遍历过的结点

        while not pQueue.empty():
            _pri, board, pos0, depth, process = pQueue.get()

            if board == target:
                return depth, process
            for d in (-1, 1, -size, size):  # 对应的是左右上下的相邻结点
                nei = pos0 + d
                if abs(nei // size - pos0 // size) + abs(nei % size - pos0 % size) != 1:
                    continue
                if 0 <= nei < size ** 2:  # 符合边界条件的相邻结点
                    newboard = list(board)
                    newboard[pos0], newboard[nei] = newboard[nei], newboard[pos0]
                    newt = tuple(newboard)
                    if newt not in seen:  # 没有被遍历过的状态
                        seen.add(newt)
                        # pQueue.put([depth + 1 + 2 * self.calDistance(newt), newt, nei, depth + 1, process + [d]])
                        pQueue.put(
                            [depth + 1 + 0.9 * self.calDistance(newt, size), newt, nei, depth + 1, process + [d]]) # 调整启发函数的权重可以缩短时间但增加步数
                        
                        
if __name__ == '__main__':
    t0 = time.time()
    print(Solution().solve([4,13,7,6,3,5,15,12,2,9,11,14,1,8,10,0]))
    print(time.time() - t0)
    print(Solution().solve([8,3,5,7,4,1,0,2,6]))
