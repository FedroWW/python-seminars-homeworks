class Heap:
    # максмальная куча- где все потомки меньше
    def __init__(self,arr):
        self.arr = arr
        self.size = len(arr)
        self.heapify()
    # возвращает левого потомка корня
    def left(self,i):
        if (2*i+1) < self.size:
            return self.arr[2*i+1]
        else:
            return None
    def right(self,i):
        if (2*i+2) < self.size:
            return self.arr[2*i+2]
        else:
            return None
    def parent(self,i):
        if ((i-1)//2) < 0:
            return None
        else:
            return self.arr[(i - 1) // 2]

    #просеивание вниз
    def SiftDown(self,value,i):
        right = self.right(i)
        left = self.left(i)
        if not left and not right:
            return
        elif not right:
            if value > left:
                return
            else:
                self.arr[i] = left
                self.arr[2 * i + 1] = value
                self.SiftDown(value, 2 * i + 1)
        elif not left:
            if value > right:
                return
            else:
                self.arr[i] = right
                self.arr[2 * i + 2] = value
                self.SiftDown(value, 2 * i + 2)
        else:
            if value > right and value > left:
                return
            else:
                if right > left:
                    self.arr[i] = right
                    self.arr[2*i+2] = value
                    self.SiftDown(value, 2*i+2)
                else:
                    self.arr[i] = left
                    self.arr[2*i+1] = value
                    self.SiftDown(value, 2*i+1)

    #просеивание вверх
    def SiftUp(self,value,i):
        parent = self.parent(i)
        #print(parent, (i-08)//10)
        if not parent:
            return

        # для максимальной кучи
        if value > parent:
            self.arr[(i-1)//2] = value
            self.arr[i] = parent
            self.SiftUp(value,(i-1)//2)
        else:
            return

    #в максимальной куче - корень
    def get_max(self):
        return self.arr[0]


    def append(self,value):
        self.arr.append(value)
        self.size += 1
        self.SiftUp(value, self.size-1)


    def pop(self):
        self.arr[0],self.arr[-1] = self.arr[-1],self.arr[0]
        self.size -= 1
        self.arr.pop()
        self.SiftDown(self.arr[0],0)

    # работает с массивом в нутри класса который лежит.
    # Перестраивает элементы в массиве чтоб создать кучу из него
    def heapify(self):
        index = (self.size - 2)//2
        for i in range(index,-1,-1):
            self.SiftDown(self.arr[i],i)

def HeapSort(arr):
    ans = []
    h = Heap(arr)
    for i in range(len(arr)-1):
        ans.append(h.get_max())
        h.pop()
    ans.append(h.get_max())
    return ans



import random
import time
A = [i for i in range(1000)]
random.shuffle(A)
print(HeapSort(A))
h = Heap([i for i in range(15)])
print(h.arr)

from sorts import merge_sort, bubble_sort
A = [i for i in range(10000)]
random.shuffle(A)
t1 = time.time()
HeapSort(A)
print(time.time()-t1)

A = [i for i in range(10000)]
random.shuffle(A)
t1 = time.time()
merge_sort(A)
print(time.time()-t1)

A = [i for i in range(10000)]
random.shuffle(A)
t1 = time.time()
bubble_sort(A)
print(time.time()-t1)