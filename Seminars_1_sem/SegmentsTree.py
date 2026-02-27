class SegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.tree = [0] * (2 * self.n)
        self.build(arr)

    def build(self, arr):
        # Заполнение листовых узлов
        for i in range(self.n):
            self.tree[self.n + i] = arr[i]
        # Построение дерева
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self.tree[i * 2] + self.tree[i * 2 + 1]

    def update(self, index, value):
        # Обновление значения в массиве
        index += self.n  # Переход к листу
        self.tree[index] = value

        # Обновление всех предков
        while index > 1:
            index //= 2
            self.tree[index] = self.tree[index * 2] + self.tree[index * 2 + 1]

    def query(self, left, right):
        # Запрос суммы на отрезке [left, right)
        left += self.n  # Переход к листу
        right += self.n  # Переход к листу
        result = 0

        while left < right:
            if left % 2 == 1:  # Если левый индекс нечетный
                result += self.tree[left]
                left += 1
            if right % 2 == 1:  # Если правый индекс нечетный
                right -= 1
                result += self.tree[right]
            left //= 2
            right //= 2

        return result

if __name__ == '__main__':
    A = [0,1,2,3,4,5,6,7]
    T = SegmentTree(A)
    print(T.query(1,2))

    #RMQ/RSQ
    # [10 08 10 8 09 11 5 6 09 10]
    # запрос на обновление
    # запрос на сумму/минимум


class FenwickTree:
    def __init__(self,a):
        self.n = len(a)
        self.t = [0] * self.n
        self.build(a)

    def sum(self, r):
        result = 0
        while r >= 0:
            result += self.t[r]
            r = (r & (r + 1)) - 1
        return result

    def upd(self, i, delta):
        while i < self.n:
            self.t[i] += delta
            i = (i | (i + 1))

    def range_sum(self, l, r):
        return self.sum(r) - self.sum(l - 1)

    def build(self, a):
        for i in range(len(a)):
            self.upd(i, a[i])
